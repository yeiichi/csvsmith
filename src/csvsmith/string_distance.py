from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto


class Relation(Enum):
    EXACT_MATCH = auto()
    CASE_INSENSITIVE_MATCH = auto()
    WHITESPACE_TRIMMED_MATCH = auto()
    NORMALIZED_SPACE_MATCH = auto()
    NO_STRUCTURAL_MATCH = auto()


@dataclass
class Result:
    classification: Relation
    damerau_levenshtein_distance: int
    jaro_winkler_score: float
    similarity_percentage: float

    def get_relation_string(self) -> str:
        if self.classification is Relation.EXACT_MATCH:
            return "Identical"
        if self.classification is Relation.CASE_INSENSITIVE_MATCH:
            return "Case-Insensitive Match"
        if self.classification is Relation.WHITESPACE_TRIMMED_MATCH:
            return "Similar (Trimmed)"
        if self.classification is Relation.NORMALIZED_SPACE_MATCH:
            return "Synonymous (No Spaces)"
        return "Different"


class StringDistance:
    """
    Provides functionality for calculating string distances and relationships between
    two strings based on various algorithms.

    This class includes methods for analyzing string similarities and relationships,
    including exact matches, case-insensitive comparisons, and whitespace normalization.
    It also implements Damerau-Levenshtein and Jaro-Winkler distance calculations.

    :return classification: Possible relationship classification between two strings.
    :return damerau_levenshtein_distance: Integer distance calculated using the Damerau-Levenshtein algorithm.
    :return jaro_winkler_score: A float score indicating similarity using the Jaro-Winkler algorithm.
    :return similarity_percentage: A percentage similarity score between two strings.
    """
    @staticmethod
    def analyze(a: str, b: str, ignore_case: bool = False) -> Result:
        sa = str(a)
        sb = str(b)

        relation = StringDistance.classify(sa, sb)

        if ignore_case:
            sa = sa.lower()
            sb = sb.lower()

        d_dist = StringDistance.calculate_damerau_levenshtein(sa, sb)
        jw_score = StringDistance.calculate_jaro_winkler(sa, sb)

        max_len = max(len(sa), len(sb))
        similarity = 100.0 if max_len == 0 else (1.0 - d_dist / max_len) * 100.0

        return Result(
            classification=relation,
            damerau_levenshtein_distance=d_dist,
            jaro_winkler_score=jw_score,
            similarity_percentage=similarity,
        )

    @staticmethod
    def trim(s: str) -> str:
        return s.strip()

    @staticmethod
    def strip_all(s: str) -> str:
        return "".join(ch for ch in s if not ch.isspace())

    @staticmethod
    def equals_ignore_case(a: str, b: str) -> bool:
        return a.lower() == b.lower()

    @staticmethod
    def classify(a: str, b: str) -> Relation:
        if a == b:
            return Relation.EXACT_MATCH
        if StringDistance.equals_ignore_case(a, b):
            return Relation.CASE_INSENSITIVE_MATCH
        if StringDistance.trim(a) == StringDistance.trim(b):
            return Relation.WHITESPACE_TRIMMED_MATCH
        if StringDistance.strip_all(a) == StringDistance.strip_all(b):
            return Relation.NORMALIZED_SPACE_MATCH
        return Relation.NO_STRUCTURAL_MATCH

    @staticmethod
    def calculate_damerau_levenshtein(s1: str, s2: str) -> int:
        """
        Restricted Damerau-Levenshtein distance:
        insertion, deletion, substitution, adjacent transposition.
        """
        m = len(s1)
        n = len(s2)

        d = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(m + 1):
            d[i][0] = i
        for j in range(n + 1):
            d[0][j] = j

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                cost = 0 if s1[i - 1] == s2[j - 1] else 1

                d[i][j] = min(
                    d[i - 1][j] + 1,        # deletion
                    d[i][j - 1] + 1,        # insertion
                    d[i - 1][j - 1] + cost, # substitution
                )

                if (
                    i > 1
                    and j > 1
                    and s1[i - 1] == s2[j - 2]
                    and s1[i - 2] == s2[j - 1]
                ):
                    d[i][j] = min(d[i][j], d[i - 2][j - 2] + cost)

        return d[m][n]

    @staticmethod
    def calculate_jaro_winkler(s1: str, s2: str) -> float:
        len1 = len(s1)
        len2 = len(s2)

        if len1 == 0 and len2 == 0:
            return 1.0
        if len1 == 0 or len2 == 0:
            return 0.0

        match_distance = max(len1, len2) // 2 - 1
        if match_distance < 0:
            match_distance = 0

        s1_matches = [False] * len1
        s2_matches = [False] * len2

        matches = 0
        for i in range(len1):
            start = max(0, i - match_distance)
            end = min(i + match_distance + 1, len2)

            for j in range(start, end):
                if not s2_matches[j] and s1[i] == s2[j]:
                    s1_matches[i] = True
                    s2_matches[j] = True
                    matches += 1
                    break

        if matches == 0:
            return 0.0

        transpositions = 0
        k = 0
        for i in range(len1):
            if s1_matches[i]:
                while not s2_matches[k]:
                    k += 1
                if s1[i] != s2[k]:
                    transpositions += 1
                k += 1

        jaro = (
            matches / len1
            + matches / len2
            + (matches - transpositions / 2.0) / matches
        ) / 3.0

        p = 0.1
        max_l = 4
        l = 0
        while l < min(len1, len2, max_l) and s1[l] == s2[l]:
            l += 1

        return jaro + (l * p * (1.0 - jaro))


def analyze_pair(a: str, b: str, ignore_case: bool = False) -> Result:
    return StringDistance.analyze(a, b, ignore_case)