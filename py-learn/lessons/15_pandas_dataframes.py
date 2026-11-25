"""第 15 课：数据处理（pandas）。

C++ 里处理表格是 `std::vector<Row>` + 手写循环聚合；
pandas 的 DataFrame 是「带列名的列式容器 + 向量化运算」，
同样的聚合一行就能表达，而且不用自己管索引和类型。

本课覆盖：构造、读 CSV、选取与过滤、派生列、groupby 聚合、
排序、merge、缺失值、describe。

运行：uv run python lessons/15_pandas_dataframes.py
"""

from __future__ import annotations

import tempfile
from pathlib import Path

import pandas as pd


def build_frame() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "gadget": ["讲解卡", "抽奖转盘", "讲解卡", "集卡", "抽奖转盘"],
            "date": ["2026-11-20", "2026-11-20", "2026-11-21", "2026-11-21", "2026-11-22"],
            "exposure": [12000, 8000, 15000, 5000, 9000],
            "click": [600, 320, 900, 150, 270],
            "gmv": [12000.0, 4800.0, 18000.0, 2400.0, 5400.0],
        }
    )


def basics() -> None:
    df = build_frame()
    print(f"形状 {df.shape}，列 {list(df.columns)}")
    print(f"每列类型：{dict(df.dtypes.astype(str))}")
    print(df.head(3).to_string(index=False))


def columns_and_filter() -> None:
    df = build_frame()
    df["ctr"] = (df["click"] / df["exposure"]).round(3)  # 派生列，向量化
    picked = df.loc[df["exposure"] > 8000, ["gadget", "date", "exposure", "ctr"]]
    print(picked.to_string(index=False))


def group_and_sort() -> None:
    df = build_frame()
    summary = (
        df.groupby("gadget", as_index=False)
        .agg(exposure=("exposure", "sum"), click=("click", "sum"), gmv=("gmv", "sum"))
        .assign(ctr=lambda frame: (frame["click"] / frame["exposure"]).round(3))
        .sort_values("ctr", ascending=False)
    )
    print(summary.to_string(index=False))


def merge_dimension() -> None:
    df = build_frame()
    dim = pd.DataFrame(
        {"gadget": ["讲解卡", "抽奖转盘", "集卡"], "owner": ["电商", "运营", "增长"]}
    )
    merged = df.merge(dim, on="gadget", how="left")
    print(merged[["gadget", "owner", "gmv"]].drop_duplicates().to_string(index=False))


def missing_values() -> None:
    df = build_frame()
    df.loc[1, "gmv"] = None  # 模拟上游漏数据
    print(f"缺失数量：{int(df['gmv'].isna().sum())}，类型变成 {df['gmv'].dtype}")
    filled = df.assign(gmv=df["gmv"].fillna(0.0))
    print(f"填充后总额 {filled['gmv'].sum():.0f}")
    print(f"数值列统计：\n{filled[['exposure', 'click', 'gmv']].describe().round(1)}")


def roundtrip_csv() -> None:
    """读写 CSV：pandas 最常用的落地方式。"""
    df = build_frame()
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "metrics.csv"
        df.to_csv(path, index=False, encoding="utf-8")
        back = pd.read_csv(path)
        print(f"写盘 {path.name}（{path.stat().st_size} 字节），读回形状 {back.shape}")
        print(f"读回后 ctr 均值 {(back['click'] / back['exposure']).mean():.3f}")


def main() -> None:
    for section in (
        basics,
        columns_and_filter,
        group_and_sort,
        merge_dimension,
        missing_values,
        roundtrip_csv,
    ):
        print(f"\n== {section.__name__} ==")
        section()


if __name__ == "__main__":
    main()


# ===== 练习 =====
# 1. 按 date 聚合出每日总曝光和总 GMV，并按日期排序。
# 2. 算出每个挂件的「点击成本 = gmv / click」，找出最高和最低的各一个。
# 3. 用 pandas 读一个 10 万行 CSV，对比 chunksize=10000 逐块处理的内存占用。
