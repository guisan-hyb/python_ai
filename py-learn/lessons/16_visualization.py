"""第 16 课：数据可视化（matplotlib）。

C++ 没有「画图」的标准库，Python 里 matplotlib 是最底层的绘图库，
pandas 的 plot、seaborn、Streamlit 展示都建立在它之上。

本课覆盖：Agg 后端（无界面环境也能出图）、折线/柱状、保存 PNG、
pandas 直接画图、中文字体的坑。

运行：uv run python lessons/16_visualization.py
"""

from __future__ import annotations

import tempfile
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # 必须在 pyplot 之前设置：不弹窗口，只保存文件

import matplotlib.pyplot as plt  # noqa: E402 - 后端必须先设置
import pandas as pd  # noqa: E402


def line_chart(output: Path) -> Path:
    days = ["11-20", "11-21", "11-22", "11-23"]
    exposure = [12, 15, 9, 18]
    clicks = [0.6, 0.9, 0.27, 1.1]

    fig, ax = plt.subplots(figsize=(6, 3), dpi=120)
    ax.plot(days, exposure, marker="o", color="#2f6fed", label="Exposure (k)")
    ax.set_title("Gadget exposure trend")
    ax.set_ylabel("Exposure (thousand)")
    ax.grid(alpha=0.3)
    ax.legend()
    path = save(fig, output, "line")
    print(f"  曝光量 {exposure}，点击数 {clicks}")
    return path


def bar_chart(output: Path) -> Path:
    frame = pd.DataFrame(
        {"gadget": ["ExplainCard", "LuckyWheel", "CardSet"], "ctr": [0.05, 0.04, 0.03]}
    )
    fig, ax = plt.subplots(figsize=(6, 3), dpi=120)
    ax.bar(frame["gadget"], frame["ctr"], color=["#2f6fed", "#f6a821", "#39b979"])
    ax.set_title("CTR by gadget")
    ax.set_ylabel("CTR")
    ax.bar_label(ax.containers[0], fmt="%.3f")
    return save(fig, output, "bar")


def pandas_plot(output: Path) -> Path:
    frame = pd.DataFrame(
        {"date": ["11-20", "11-21", "11-22"], "gmv": [12000, 18000, 5400]}
    ).set_index("date")
    ax = frame.plot(kind="line", marker="s", title="Daily GMV")
    return save(ax.figure, output, "pandas")


def save(fig: plt.Figure, output: Path, name: str) -> Path:
    path = output / f"{name}.png"
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)
    print(f"  {name}.png {path.stat().st_size // 1024} KB -> {path}")
    return path


def cjk_pitfall() -> None:
    print("中文标签默认会显示成方框（缺中文字体）。三种解法：")
    print("  1. 图表里用英文标签（本课的写法，最省事）")
    print("  2. 设置 rcParams['font.sans-serif'] = ['PingFang SC']")
    print("     再设 rcParams['axes.unicode_minus'] = False，负号才不会变方框")
    print("  3. 只在图里放数字，中文交给标题/说明文字")


def main() -> None:
    output = Path(tempfile.mkdtemp(prefix="py_learn_charts_"))
    print(f"图片输出目录：{output}")
    for section in (line_chart, bar_chart, pandas_plot):
        print(f"\n== {section.__name__} ==")
        section(output)
    print("\n== cjk_pitfall ==")
    cjk_pitfall()
    print("\n在 Streamlit 里直接 st.pyplot(fig) 即可显示；保存后用 open 命令也能看")


if __name__ == "__main__":
    main()


# ===== 练习 =====
# 1. 把第 15 课的 groupby 结果画成横向柱状图，按 CTR 排序。
# 2. 画一张双 Y 轴图：左轴曝光量、右轴 CTR，验证两者是否同向。
# 3. 设置中文字体后重画一遍，对比不带设置的乱码效果。
