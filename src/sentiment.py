from __future__ import annotations

from typing import Literal

import pandas as pd
from textblob import TextBlob


def compute_textblob_sentiment(
    df: pd.DataFrame,
    text_col: str = "headline",
    polarity_col: str = "sentiment_polarity",
    subjectivity_col: str = "sentiment_subjectivity",
    aggregate_by: Literal["none", "date", "date_stock"] = "none",
    date_col: str = "date",
    stock_col: str = "stock",
) -> pd.DataFrame:
    """
    Compute TextBlob sentiment scores for a text column.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame with at least `text_col` present.
    text_col : str
        Column containing the text to score.
    polarity_col : str
        Name of the polarity output column.
    subjectivity_col : str
        Name of the subjectivity output column.
    aggregate_by : {"none", "date", "date_stock"}
        - "none": return row-level scores.
        - "date": average scores per calendar date.
        - "date_stock": average scores per (date, stock) pair.
    date_col : str
        Date column used for aggregation.
    stock_col : str
        Stock symbol column used for aggregation by stock.
    """
    if text_col not in df.columns:
        raise KeyError(f"Column '{text_col}' not found in DataFrame.")

    out = df.copy()

    def _score(text: str) -> tuple[float, float]:
        blob = TextBlob(str(text))
        sentiment = blob.sentiment
        return float(sentiment.polarity), float(sentiment.subjectivity)

    scores = out[text_col].apply(_score)
    out[polarity_col] = scores.apply(lambda t: t[0])
    out[subjectivity_col] = scores.apply(lambda t: t[1])

    if aggregate_by == "none":
        return out

    if aggregate_by == "date":
        if date_col not in out.columns:
            raise KeyError(f"Column '{date_col}' not found for date aggregation.")
        grouped = (
            out.groupby(out[date_col].dt.date)[[polarity_col, subjectivity_col]]
            .mean()
            .reset_index()
            .rename(columns={date_col: "date"})
        )
        return grouped

    if aggregate_by == "date_stock":
        missing = [c for c in (date_col, stock_col) if c not in out.columns]
        if missing:
            raise KeyError(f"Missing columns for date_stock aggregation: {missing}")

        grouped = (
            out.groupby([out[date_col].dt.date, stock_col])[[polarity_col, subjectivity_col]]
            .mean()
            .reset_index()
            .rename(columns={date_col: "date"})
        )
        return grouped

    raise ValueError(f"Unsupported aggregate_by value: {aggregate_by}")


