from __future__ import annotations

from typing import Tuple

import numpy as np
import pandas as pd
from scipy.stats import pearsonr


def compute_daily_returns(
    prices: pd.DataFrame,
    close_col: str = "Close",
    date_col: str = "Date",
) -> pd.DataFrame:
    """
    Compute daily percentage returns from close prices.
    """
    if close_col not in prices.columns:
        raise KeyError(f"Column '{close_col}' not found in price data.")

    out = prices.copy()
    out[date_col] = pd.to_datetime(out[date_col], errors="coerce")
    out = out.sort_values(date_col)
    out["daily_return"] = out[close_col].pct_change()
    return out


def aggregate_daily_sentiment(
    news: pd.DataFrame,
    date_col: str = "date",
    sentiment_col: str = "sentiment_polarity",
    stock_col: str | None = "stock",
) -> pd.DataFrame:
    """
    Aggregate sentiment scores to daily level (optionally per stock).
    """
    if date_col not in news.columns or sentiment_col not in news.columns:
        raise KeyError("News data must contain date and sentiment columns.")

    tmp = news.copy()
    tmp[date_col] = pd.to_datetime(tmp[date_col], errors="coerce")

    if stock_col and stock_col in tmp.columns:
        grouped = (
            tmp.groupby([tmp[date_col].dt.date, stock_col])[sentiment_col]
            .mean()
            .reset_index()
            .rename(columns={date_col: "date", sentiment_col: "avg_sentiment"})
        )
    else:
        grouped = (
            tmp.groupby(tmp[date_col].dt.date)[sentiment_col]
            .mean()
            .reset_index()
            .rename(columns={date_col: "date", sentiment_col: "avg_sentiment"})
        )
    return grouped


def merge_sentiment_and_returns(
    sentiment: pd.DataFrame,
    returns: pd.DataFrame,
    date_col_sent: str = "date",
    date_col_ret: str = "Date",
) -> pd.DataFrame:
    """
    Merge daily sentiment and returns on calendar date.
    """
    s = sentiment.copy()
    r = returns.copy()

    s[date_col_sent] = pd.to_datetime(s[date_col_sent]).dt.date
    r[date_col_ret] = pd.to_datetime(r[date_col_ret]).dt.date

    merged = pd.merge(
        s,
        r,
        left_on=date_col_sent,
        right_on=date_col_ret,
        how="inner",
    )
    return merged


def pearson_correlation(
    df: pd.DataFrame,
    sentiment_col: str = "avg_sentiment",
    returns_col: str = "daily_return",
) -> Tuple[float, float]:
    """
    Compute Pearson correlation between sentiment and returns.

    Returns
    -------
    (corr, p_value)
    """
    for col in (sentiment_col, returns_col):
        if col not in df.columns:
            raise KeyError(f"Column '{col}' not found for correlation.")

    valid = df[[sentiment_col, returns_col]].dropna()
    if len(valid) < 3:
        raise ValueError("Not enough data points to compute correlation (need >= 3).")

    corr, p_val = pearsonr(valid[sentiment_col], valid[returns_col])
    return float(corr), float(p_val)


