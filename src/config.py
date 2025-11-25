from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
INTERIM_DATA_DIR = DATA_DIR / "interim"
PROCESSED_DATA_DIR = DATA_DIR / "processed"


def ensure_data_dirs() -> None:
    """
    Ensure that the standard data subdirectories exist.
    This is safe to call from notebooks or scripts before reading/writing data.
    """
    for d in (RAW_DATA_DIR, INTERIM_DATA_DIR, PROCESSED_DATA_DIR):
        d.mkdir(parents=True, exist_ok=True)


