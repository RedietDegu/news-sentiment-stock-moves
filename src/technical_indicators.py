from __future__ import annotations

from typing import Iterable, Optional

import numpy as np
import pandas as pd

try:
    import talib
except ImportError:  # pragma: no cover - depends on system libs
    talib = None  # type: ignore[assignment]


def _require_talib() -> None:
    if talib is None:
        raise ImportError(
            "TA-Lib is not installed or could not be imported. "
            "Install system libs (e.g. `brew install ta-lib`) and then `pip install TA-Lib`."
        )


def add_moving_averages(
    df: pd.DataFrame,
    close_col: str = "Close",
    windows: Iterable[int] = (5, 20, 50),
) -> pd.DataFrame:
    """
    Add simple moving averages to the DataFrame for the given windows.
    """
    _require_talib()
    out = df.copy()
    close = out[close_col].to_numpy(dtype=float)
    for w in windows:
        out[f"SMA_{w}"] = talib.SMA(close, timeperiod=w)
    return out


def add_rsi(
    df: pd.DataFrame,
    close_col: str = "Close",
    period: int = 14,
    col_name: Optional[str] = None,
) -> pd.DataFrame:
    """
    Add Relative Strength Index (RSI) to the DataFrame.
    """
    _require_talib()
    out = df.copy()
    close = out[close_col].to_numpy(dtype=float)
    rsi = talib.RSI(close, timeperiod=period)
    out[col_name or f"RSI_{period}"] = rsi
    return out


def add_macd(
    df: pd.DataFrame,
    close_col: str = "Close",
    fastperiod: int = 12,
    slowperiod: int = 26,
    signalperiod: int = 9,
    prefix: str = "MACD",
) -> pd.DataFrame:
    """
    Add MACD (Moving Average Convergence Divergence) indicators to the DataFrame.
    """
    _require_talib()
    out = df.copy()
    close = out[close_col].to_numpy(dtype=float)
    macd, macd_signal, macd_hist = talib.MACD(
        close,
        fastperiod=fastperiod,
        slowperiod=slowperiod,
        signalperiod=signalperiod,
    )
    out[f"{prefix}"] = macd
    out[f"{prefix}_signal"] = macd_signal
    out[f"{prefix}_hist"] = macd_hist
    return out


