from __future__ import annotations

from pathlib import Path
from typing import Optional

import pandas as pd

from .config import RAW_DATA_DIR


def load_news_csv(
    filename: str | Path,
    date_col: str = "date",
    parse_dates: bool = True,
    tz: Optional[str] = "UTC",
) -> pd.DataFrame:
    """
    Load the FNSPID-style news CSV.

    Expected minimal columns:
        - headline
        - url
        - publisher
        - date (UTC-4 in source; you can localize/convert as needed)
        - stock
    """
    path = Path(filename)
    if not path.is_absolute():
        path = RAW_DATA_DIR / path

    df = pd.read_csv(path)

    if parse_dates and date_col in df.columns:
        df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
        if tz is not None:
            # Localize if naive, otherwise convert
            if df[date_col].dt.tz is None:
                df[date_col] = df[date_col].dt.tz_localize(tz)
            else:
                df[date_col] = df[date_col].dt.tz_convert(tz)
    return df


def load_prices_csv(
    filename: str | Path,
    date_col: str = "Date",
    parse_dates: bool = True,
) -> pd.DataFrame:
    """
    Load OHLCV price data from CSV for Task 2 / Task 3.

    Expected columns: Open, High, Low, Close, Volume, and a date column.
    """
    path = Path(filename)
    if not path.is_absolute():
        path = RAW_DATA_DIR / path

    df = pd.read_csv(path)
    if parse_dates and date_col in df.columns:
        df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
        df = df.sort_values(date_col)
    return df


