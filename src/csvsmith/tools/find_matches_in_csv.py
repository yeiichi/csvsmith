import csv

from ..utils.normalize import normalize

def find_matches_in_csv(file_path, target_key, stringency=1.0, **kwargs):
    """
    Scans a CSV for a key and returns coordinates and neighbor data.
    """
    # Merge defaults with user overrides
    cfg = {
        'ignore_case': kwargs.get('ignore_case', True),
        'ignore_whitespace': kwargs.get('ignore_whitespace', True),
        'nfkc': kwargs.get('nfkc', True)
    }
    
    clean_target = normalize(target_key, **cfg)
    results = []
    
    # encoding='utf-8-sig' + dialect='excel' is the 'Anti-BOOM' shield
    with open(file_path, mode='r', encoding='utf-8-sig', newline='') as f:
        reader = csv.reader(f, dialect='excel')

        header = next(reader, None)
        if header is None:
            return results

        for r_idx, row in enumerate(reader):
            for c_idx, cell in enumerate(row):
                if normalize(cell, **cfg) == clean_target:
                    # Key found! Map all non-empty values in this row
                    associated = {
                        f"col_{i}": val.strip()
                        for i, val in enumerate(row)
                        if val.strip() and i != c_idx
                    }

                    results.append({
                        "match": cell,
                        "coords": (r_idx, c_idx),
                        "data": associated
                    })

    return results