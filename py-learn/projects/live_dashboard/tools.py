"""把分析函数包成 Agent 工具：模型只负责选工具和填参数。"""

from __future__ import annotations

from typing import Any

from agent.tools import Tool

from .analysis import by_gadget, daily, load, overview

_DF = load()


def _overview_text() -> str:
    data = overview(_DF)
    return (
        f"覆盖 {data['days']} 天、{data['gadgets']} 个挂件："
        f"曝光 {data['exposure']}，点击 {data['click']}，"
        f"CTR {data['ctr']:.2%}，CVR {data['cvr']:.2%}，GMV {data['gmv']:.0f}"
    )


def _top_text(metric: str = "ctr", top: int = 3) -> str:
    frame = by_gadget(_DF, metric=metric, top=top)
    key = metric if metric in {"ctr", "cvr", "gmv", "exposure"} else "ctr"
    parts = [f"{row['gadget']}={row[key]:.4f}" for _, row in frame.iterrows()]
    return f"按 {key} 排名前 {top}：" + "，".join(parts)


def _trend_text(gadget: str | None = None) -> str:
    frame = daily(_DF, gadget=gadget)
    if frame.empty:
        return f"没有找到挂件 {gadget} 的数据"
    points = [f"{row['date']:%m-%d}={row['ctr']:.2%}" for _, row in frame.iterrows()]
    scope = gadget or "全部挂件"
    return f"{scope} 的 CTR 走势：" + "，".join(points)


def _tool(name: str, description: str, properties: dict[str, Any], func: Any) -> Tool:
    return Tool(
        name=name,
        description=description,
        parameters={"type": "object", "properties": properties, "required": []},
        func=func,
    )


PROJECT_TOOLS: dict[str, Tool] = {
    "overview": _tool(
        "overview",
        "查看全部挂件的整体指标汇总（曝光、点击、CTR、CVR、GMV）。",
        {},
        _overview_text,
    ),
    "top_gadgets": _tool(
        "top_gadgets",
        "按某个指标给挂件排名，metric 可选 ctr/cvr/gmv/exposure。",
        {
            "metric": {"type": "string", "enum": ["ctr", "cvr", "gmv", "exposure"]},
            "top": {"type": "integer", "minimum": 1, "maximum": 10},
        },
        _top_text,
    ),
    "daily_trend": _tool(
        "daily_trend",
        "查看 CTR 按天走势，可指定 gadget 只看单个挂件。",
        {"gadget": {"type": "string", "description": "挂件名，如 讲解卡"}},
        _trend_text,
    ),
}
