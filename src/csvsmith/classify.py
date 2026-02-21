# src/csvsmith/classify.py

from __future__ import annotations

import csv
import hashlib
import json
import re
import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional


@dataclass(frozen=True)
class HeaderKey:
    """
    Hashable header signature.

    mode="strict"  -> ordered tuple (column order matters)
    mode="relaxed" -> sorted unique tuple (column order does NOT matter)
    """
    mode: str
    cols: tuple[str, ...]


class CSVClassifier:
    """
    Classifies CSV files into folders based on header signatures.

    Two orthogonal controls:
      - mode:  "strict" | "relaxed"
      - match: "exact"  | "contains"   (contains is your legacy behavior)

    signatures:
      dict[str, list[str]]
        - category -> expected columns
        - interpretation depends on match:
            exact:    expected columns must match the file header exactly
            contains: expected columns must be a subset of the file header
    """

    def __init__(
        self,
        source_dir: str | Path,
        dest_dir: str | Path,
        signatures: Optional[dict[str, list[str]]] = None,
        *,
        mode: str = "strict",   # "strict" or "relaxed"
        match: str = "exact",   # "exact" or "contains"
        auto: bool = False,
        dry_run: bool = False,
        report_only: bool = False,
        encoding: str = "utf-8-sig",
        strip: bool = True,
        casefold: bool = False,
        drop_empty: bool = True,
    ) -> None:
        self.source = Path(source_dir)
        self.dest = Path(dest_dir)

        self.signatures = signatures or {}
        self.mode = mode
        self.match = match

        self.auto = auto
        self.dry_run = dry_run
        self.report_only = report_only

        self.encoding = encoding
        self.strip = strip
        self.casefold = casefold
        self.drop_empty = drop_empty

        self.manifest = {
            "source_path": str(self.source.absolute()),
            "timestamp": datetime.now().isoformat(),
            "mode": self.mode,
            "match": self.match,
            "report_only": self.report_only,
            "operations": [],
        }

        if self.mode not in ("strict", "relaxed"):
            raise ValueError("mode must be 'strict' or 'relaxed'")
        if self.match not in ("exact", "contains"):
            raise ValueError("match must be 'exact' or 'contains'")

        # Precompute signature keys for exact matching.
        self._signature_keys: dict[str, HeaderKey] = {}
        if self.match == "exact":
            for cat, cols in self.signatures.items():
                norm = self._normalize_header(cols, mode=self.mode)
                self._signature_keys[cat] = self._header_key(norm, mode=self.mode)

    # -------------------------
    # Header extraction & keys
    # -------------------------

    def _read_header_row(self, file_path: Path) -> Optional[list[str]]:
        """Read the first row as header; return None if empty or invalid CSV."""
        if file_path.suffix.lower() != ".csv":
            return None

        try:
            with file_path.open("r", encoding=self.encoding, newline="") as f:
                reader = csv.reader(f)
                header = next(reader, None)
        except (UnicodeDecodeError, csv.Error):
            return None

        if not header:
            return None

        # Rule (kept from your original): if the first row is purely numeric,
        # treat it as data, not a header.
        # Note: this is heuristic; keep/remove depending on your corpus.
        if self._is_purely_numeric_row(header):
            return None

        return header

    @staticmethod
    def _is_purely_numeric_row(row: list[str]) -> bool:
        cells = [str(c).strip() for c in row if str(c).strip()]
        if not cells:
            return False

        def is_num(s: str) -> bool:
            # simple, stable heuristic (no float('nan') surprises)
            s = s.replace(".", "", 1)
            return s.isdigit()

        return all(is_num(c) for c in cells)

    def _normalize_header(self, header: list[str], *, mode: str) -> list[str]:
        out: list[str] = []
        for s in header:
            s = str(s)
            if self.strip:
                s = s.strip()
            if self.casefold:
                s = s.casefold()
            if self.drop_empty and s == "":
                continue
            out.append(s)

        # mode only affects keying, not normalization list itself
        if mode not in ("strict", "relaxed"):
            raise ValueError("mode must be 'strict' or 'relaxed'")
        return out

    @staticmethod
    def _header_key(header: list[str], *, mode: str) -> HeaderKey:
        if mode == "strict":
            return HeaderKey(mode="strict", cols=tuple(header))
        # relaxed: order-insensitive; de-duplicate
        return HeaderKey(mode="relaxed", cols=tuple(sorted(set(header))))

    # -------------------------
    # Matching / classification
    # -------------------------

    def _match_category(self, header_norm: list[str]) -> Optional[str]:
        """
        Return the first matching category, or None if no match.
        """
        if not self.signatures:
            return None

        if self.match == "contains":
            header_set = set(header_norm)
            for cat, required_cols in self.signatures.items():
                required_norm = self._normalize_header(required_cols, mode=self.mode)
                if all(col in header_set for col in required_norm):
                    return cat
            return None

        # exact
        key = self._header_key(header_norm, mode=self.mode)
        for cat, sig_key in self._signature_keys.items():
            if key == sig_key:
                return cat
        return None

    def _auto_category(self, header_norm: list[str]) -> str:
        key = self._header_key(header_norm, mode=self.mode)

        # Human hint (limited), but sanitized and stable
        hint = "__".join(key.cols[:6])  # first N columns as hint
        hint = hint[:60]  # cap length
        hint = re.sub(r"[^A-Za-z0-9._-]+", "_", hint).strip("_") or "empty"

        # Collision-resistant suffix from the *entire* signature
        payload = "\x1f".join(key.cols).encode("utf-8")
        digest = hashlib.sha256(payload).hexdigest()[:10]  # 10 hex chars is plenty

        return f"cluster_{hint}__h{digest}"

    # -------------------------
    # File ops + manifest
    # -------------------------

    def _move_file(self, file_path: Path, category: str, headers_norm: list[str]) -> None:
        target_dir = self.dest / category
        dest_file = target_dir / file_path.name

        # Base operation record (always written)
        op = {
            "original_path": str(file_path.absolute()),
            "planned_to": str(dest_file.absolute()),
            "category": category,
            "headers": headers_norm,
            "status": "pending",
        }

        # REPORT-ONLY: do not touch filesystem, just write plan
        if self.report_only:
            op["status"] = "planned"
            self.manifest["operations"].append(op)
            return

        # DRY-RUN: no move, but show what would happen
        if self.dry_run:
            print(f"[DRY RUN] Would move: {file_path.name} -> {category}/")
            op["status"] = "simulated"
            self.manifest["operations"].append(op)
            return

        # APPLY: real move
        try:
            target_dir.mkdir(parents=True, exist_ok=True)

            # collision handling at apply-time
            if dest_file.exists():
                ts = datetime.now().strftime("%Y%m%d%H%M%S")
                dest_file = target_dir / f"{file_path.stem}_{ts}{file_path.suffix}"
                op["planned_to"] = str(dest_file.absolute())

            shutil.move(str(file_path), str(dest_file))
            print(f"Moved: {file_path.name} -> {category}/")
            op["status"] = "success"
            op["moved_to"] = str(dest_file.absolute())
        except Exception as e:
            print(f"Failed to move {file_path.name}: {e}")
            op["status"] = "failed"

        self.manifest["operations"].append(op)

    def _save_manifest(self) -> None:
        if not self.manifest["operations"]:
            return
        if self.dry_run:
            return  # keep current behavior: no manifest for dry-run

        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        manifest_path = self.dest / f"manifest_{ts}.json"
        self.dest.mkdir(parents=True, exist_ok=True)
        with manifest_path.open("w", encoding="utf-8") as f:
            json.dump(self.manifest, f, indent=4)
        print(f"\nManifest saved: {manifest_path}")

    def rollback(self, manifest_path: str | Path) -> None:
        m_path = Path(manifest_path)
        if not m_path.exists():
            print(f"Error: Manifest {manifest_path} not found.")
            return

        with m_path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        print(f"Starting rollback for session: {data.get('timestamp')}")
        for op in data.get("operations", []):
            if op.get("status") != "success":
                continue

            moved_to = op.get("moved_to") or op.get("planned_to")
            if not moved_to:
                print("Warning: manifest op missing moved_to/planned_to; skipping")
                continue

            current_loc = Path(moved_to)
            original_loc = Path(op["original_path"])

            if not current_loc.exists():
                print(f"Warning: Could not find file to restore: {current_loc}")
                continue

            if self.dry_run:
                print(f"[DRY RUN] Would restore: {current_loc.name} -> {original_loc}")
                continue

            original_loc.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(current_loc), str(original_loc))
            print(f"Restored: {current_loc.name}")

    # -------------------------
    # Main
    # -------------------------

    def run(self) -> None:
        if not self.source.is_dir():
            print(f"Error: Source directory {self.source} does not exist.")
            return

        seen: set[HeaderKey] = set()

        for file_path in self.source.glob("*.csv"):
            header_raw = self._read_header_row(file_path)

            if not header_raw:
                self._move_file(file_path, "unclassified", [])
                continue

            header_norm = self._normalize_header(header_raw, mode=self.mode)
            key = self._header_key(header_norm, mode=self.mode)
            seen.add(key)

            category = self._match_category(header_norm)
            if category is None:
                category = self._auto_category(header_norm) if self.auto else "unclassified"

            self._move_file(file_path, category, header_norm)

        self._save_manifest()