"""项目自带的规则模型：按关键词决定调哪个工具。

它和 agent.llm.MockLLM 同构，只是知识换成了挂件指标。
将来换成真实模型时，把 AnalystLLM 换成 OpenAICompatibleLLM 即可，工具层不动。
"""

from __future__ import annotations

from typing import Any

from agent.llm import Reply, ToolCall

METRIC_KEYWORDS = {
    "gmv": ("gmv", "成交", "销售额"),
    "cvr": ("cvr", "转化"),
    "exposure": ("曝光", "展现"),
    "ctr": ("ctr", "点击率"),
}


def _pick_metric(text: str) -> str:
    lowered = text.lower()
    for metric, keywords in METRIC_KEYWORDS.items():
        if any(keyword in lowered for keyword in keywords):
            return metric
    return "ctr"


class AnalystLLM:
    def chat(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
    ) -> Reply:
        last = messages[-1]
        if last["role"] == "tool":
            return Reply(content=str(last["content"]))

        text = str(last["content"])
        if "趋势" in text or "走势" in text:
            gadget = next(
                (name for name in ("讲解卡", "抽奖转盘", "集卡") if name in text),
                None,
            )
            arguments = {"gadget": gadget} if gadget else {}
            return Reply(tool_calls=(ToolCall("daily_trend", arguments),))

        if "整体" in text or "总览" in text or "汇总" in text or "概览" in text:
            return Reply(tool_calls=(ToolCall("overview", {}),))

        if any(word in text for word in ("最高", "最好", "最强", "排名", "top", "TOP")):
            return Reply(
                tool_calls=(ToolCall("top_gadgets", {"metric": _pick_metric(text), "top": 3}),)
            )

        return Reply(
            content=(
                "我可以回答：整体汇总、哪个挂件 CTR/成交最高、某个挂件的走势。"
                "试试「整体情况怎么样」"
            )
        )
