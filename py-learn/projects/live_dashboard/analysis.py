"""指标分析层：只做纯计算，不碰 UI 和网络，方便测试与复用。"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

DATA_PATH = Path(__file__).resolve().parent / "data" / "metrics.csv"
METRICS = ("ctr", "cvr", "gmv", "exposure")


def load(path: Path | None = None) -> pd.DataFrame:
    """读原始明细，顺手算出派生指标。"""
    df = pd.read_csv(path or DATA_PATH, parse_dates=["date"])
    df["ctr"] = (df["click"] / df["exposure"]).round(4)
    df["cvr"] = (df["order_cnt"] / df["click"]).round(4)
    return df


def overview(df: pd.DataFrame) -> dict[str, float | int]:
    exposure = int(df["exposure"].sum())
    click = int(df["click"].sum())
    orders = int(df["order_cnt"].sum())
    return {
        "days": int(df["date"].nunique()),
        "gadgets": int(df["gadget"].nunique()),
        "exposure": exposure,
        "click": click,
        "orders": orders,
        "gmv": round(float(df["gmv"].sum()), 2),
        "ctr": round(click / exposure, 4) if exposure else 0.0,
        "cvr": round(orders / click, 4) if click else 0.0,
    }


def by_gadget(df: pd.DataFrame, metric: str = "ctr", top: int = 3) -> pd.DataFrame:
    """按挂件聚合，再按指定指标排序取前 top 个。"""
    grouped = df.groupby("gadget", as_index=False).agg(
        exposure=("exposure", "sum"),
        click=("click", "sum"),
        orders=("order_cnt", "sum"),
        gmv=("gmv", "sum"),
    )
    grouped["ctr"] = (grouped["click"] / grouped["exposure"]).round(4)
    grouped["cvr"] = (grouped["orders"] / grouped["click"]).round(4)
    sort_key = metric if metric in METRICS else "ctr"
    return grouped.sort_values(sort_key, ascending=False).head(top)


def daily(df: pd.DataFrame, gadget: str | None = None) -> pd.DataFrame:
    """按天汇总；传 gadget 就看单个挂件的走势。"""
    target = df if gadget is None else df[df["gadget"] == gadget]
    if target.empty:
        return pd.DataFrame(columns=["date", "exposure", "click", "gmv", "ctr"])
    return (
        target.groupby("date", as_index=False)
        .agg(exposure=("exposure", "sum"), click=("click", "sum"), gmv=("gmv", "sum"))
        .assign(ctr=lambda frame: (frame["click"] / frame["exposure"]).round(4))
        .sort_values("date")
    )
