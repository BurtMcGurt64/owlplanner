"""
Load all the data when the app starts.
"""

import csv

_courses_cache = []
_csv_path = None

def load_courses_from_csv(filepath: str) -> list[dict]:
    """
    Load course_data.csv into in-memory cache, returns number of rows loaded.
    So we don't need to repeatedly load data.
    """
    # create a global variable to access it externally
    global _courses_cache, _csv_path
    _csv_path = filepath
    rows = []
    with open(filepath, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            rows.append(row)
    _courses_cache = rows
    return len(_courses_cache)

def get_courses() -> list[dict]:
    """
    Return the cached list of courses
    """
    return _courses_cache

def refresh_courses() -> int:
    """
    Reload using the last CSV path, after scraping.
    """
    if not _csv_path:
        raise RuntimeError("CSV path not set. Call load_courses_from_csv() first.")
    return load_courses_from_csv(_csv_path)