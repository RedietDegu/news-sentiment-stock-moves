from __future__ import annotations

import pandas as pd


def add_headline_length(df: pd.DataFrame, headline_col: str = "headline") -> pd.DataFrame:
    """
    Add simple length features for headlines:
    - headline_len_chars
    - headline_len_words
    """
    out = df.copy()
    if headline_col not in out.columns:
        raise KeyError(f"Column '{headline_col}' not found in DataFrame.")

    out["headline_len_chars"] = out[headline_col].astype(str).str.len()
    out["headline_len_words"] = out[headline_col].astype(str).str.split().str.len()
    return out


def publisher_counts(df: pd.DataFrame, publisher_col: str = "publisher") -> pd.Series:
    """
    Count number of articles per publisher.
    """
    if publisher_col not in df.columns:
        raise KeyError(f"Column '{publisher_col}' not found in DataFrame.")
    return df[publisher_col].value_counts()


def articles_over_time(
    df: pd.DataFrame,
    date_col: str = "date",
    freq: str = "D",
) -> pd.Series:
    """
    Aggregate article counts over time at a given frequency (default: daily).
    """
    if date_col not in df.columns:
        raise KeyError(f"Column '{date_col}' not found in DataFrame.")

    tmp = df.dropna(subset=[date_col]).copy()
    tmp[date_col] = pd.to_datetime(tmp[date_col], errors="coerce")
    tmp = tmp.set_index(date_col)
    return tmp["headline"].resample(freq).size()


