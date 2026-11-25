"""ReAct 循环：思考 -> 调工具 -> 观察结果 -> 再思考，直到给出最终答案。

两个入口：
    run_agent(task, llm)            一问一答，最简单
    run_conversation(messages, llm) 在已有上下文上继续，供多轮对话使用
"""

from __future__ import annotations

import json
import logging
from typing import Any

from agent.llm import LLM
from agent.tools import TOOL_REGISTRY, Tool, execute_tool, openai_tool_schemas

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = (
    "你是一个会用工具的助手。需要外部信息时调用工具，拿到结果后再回答。"
    "不要编造工具没有返回过的数据。"
)


def run_conversation(
    messages: list[dict[str, Any]],
    llm: LLM,
    max_steps: int = 6,
    registry: dict[str, Tool] | None = None,
) -> tuple[str, list[dict[str, Any]]]:
    """在已有消息列表上继续跑，消息会原地追加。

    返回 (最终答案, 追加后的消息)，调用方可以把它存进会话记忆。
    registry 用来替换工具表，不传就使用全局的 TOOL_REGISTRY。
    """
    tools = TOOL_REGISTRY if registry is None else registry
    for step in range(1, max_steps + 1):
        reply = llm.chat(messages, tools=openai_tool_schemas(tools))
        logger.info("step=%s tool_calls=%s", step, [c.name for c in reply.tool_calls])

        if not reply.tool_calls:
            if reply.content:
                # 最终回答也要进历史，否则下一轮对话模型看不到自己上句说过什么
                messages.append({"role": "assistant", "content": reply.content})
            return reply.content, messages

        messages.append(
            {
                "role": "assistant",
                "content": reply.content,
                "tool_calls": [
                    {
                        "id": call.id,
                        "type": "function",
                        "function": {
                            "name": call.name,
                            "arguments": json.dumps(call.arguments, ensure_ascii=False),
                        },
                    }
                    for call in reply.tool_calls
                ],
            }
        )
        for call in reply.tool_calls:
            result = execute_tool(call.name, call.arguments, tools)
            messages.append(
                {"role": "tool", "tool_call_id": call.id, "name": call.name, "content": result}
            )

    fallback = f"达到最大步数 {max_steps}，仍未得到最终答案。"
    return fallback, messages


def run_agent(
    task: str,
    llm: LLM,
    max_steps: int = 6,
    registry: dict[str, Tool] | None = None,
) -> str:
    """一问一答：新开一段对话，跑完返回答案。"""
    messages: list[dict[str, Any]] = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": task},
    ]
    answer, _ = run_conversation(messages, llm, max_steps=max_steps, registry=registry)
    return answer
