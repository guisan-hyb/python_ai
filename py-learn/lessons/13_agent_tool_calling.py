"""第 13 课：Agent 实战（一）—— 工具调用与多轮记忆。

Agent 的本质就一句话：模型只输出「我要调哪个工具、参数是什么」，
真正的执行永远在你的代码里。这条边界决定了安全性和可观测性。

本课覆盖：工具表长什么样、循环中间的消息序列、注册自己的工具、
多轮对话记忆、上下文裁剪。

运行：uv run python lessons/13_agent_tool_calling.py
"""

from __future__ import annotations

from typing import Any

from agent.llm import MockLLM, Reply, ToolCall
from agent.loop import run_agent, run_conversation
from agent.memory import ChatSession
from agent.tools import TOOL_REGISTRY, Tool, openai_tool_schemas


def show_tool_schemas() -> None:
    """模型看到的不是 Python 函数，而是这份 JSON Schema。"""
    for schema in openai_tool_schemas():
        function = schema["function"]
        params = list(function["parameters"]["properties"])
        print(f"  {function['name']}({', '.join(params)}) - {function['description']}")


def trace_messages() -> None:
    """把循环中间的消息打出来：这是理解 Agent 最快的方式。"""
    messages: list[dict[str, Any]] = [
        {"role": "system", "content": "你是助手"},
        {"role": "user", "content": "北京天气怎么样？"},
    ]
    answer, final = run_conversation(messages, MockLLM())
    for message in final:
        content = str(message.get("content"))[:40]
        calls = [call["function"]["name"] for call in message.get("tool_calls") or []]
        print(f"  {message['role']:9} {content!r} {calls or ''}")
    print(f"最终答案：{answer}")
    print("注意：工具结果是以 role=tool 的消息回填给模型的，不是返回值直接拼字符串")


def gadget_status(gadget_id: str) -> str:
    table = {"1024": "在线，今日曝光 1.2 万", "2048": "离线，昨日曝光 0"}
    return table.get(gadget_id, f"挂件 {gadget_id} 不存在")


class AlwaysCallLLM:
    """演示用模型：第一次必定调用指定工具，拿到结果后再作答。"""

    def __init__(self, name: str, arguments: dict[str, Any]) -> None:
        self.name = name
        self.arguments = arguments

    def chat(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
    ) -> Reply:
        if messages[-1]["role"] == "tool":
            return Reply(content=f"查询结果：{messages[-1]['content']}")
        return Reply(tool_calls=(ToolCall(self.name, self.arguments),))


def custom_tool() -> None:
    """注册自己的工具：写一个 Tool，放进 registry，再传给循环。"""
    custom = Tool(
        name="gadget_status",
        description="查询直播挂件的在线状态与曝光量。",
        parameters={
            "type": "object",
            "properties": {"gadget_id": {"type": "string", "description": "挂件 ID"}},
            "required": ["gadget_id"],
        },
        func=gadget_status,
    )
    registry = {**TOOL_REGISTRY, custom.name: custom}
    answer = run_agent(
        "挂件 1024 在线吗",
        AlwaysCallLLM("gadget_status", {"gadget_id": "1024"}),
        registry=registry,
    )
    print(f"自定义工具结果：{answer}")


def memory_demo() -> None:
    """ChatSession 负责把历史消息带进下一轮。"""
    session = ChatSession(MockLLM())
    print(f"第一轮：{session.ask('北京天气怎么样？')}")
    print(f"第二轮：{session.ask('那上海的天气呢')}")
    print(f"第三轮：{session.ask('你好')}")
    print(f"当前轮数 {session.turns}，角色序列 {session.roles()}")
    print("真实模型靠这些历史理解「那上海呢」指的是什么")


def trimming_demo() -> None:
    """上下文有上限，旧消息要裁掉；工具消息不能只留一半。"""
    session = ChatSession(MockLLM(), max_messages=4)
    for index in range(1, 4):
        session.ask(f"第 {index} 个问题：北京天气怎么样？")
    print(f"裁剪后角色序列：{session.roles()}")
    print(f"消息总数 {len(session.messages)}（上限 4 条 + 1 条 system）")
    print("一轮工具调用会留下 4 条：user / assistant(tool_calls) / tool / assistant(答案)")
    print("如果裁剪后第一条是 tool，说明它对应的 assistant 被裁掉了，下一轮 API 会报错")


def main() -> None:
    for section in (show_tool_schemas, trace_messages, custom_tool, memory_demo, trimming_demo):
        print(f"\n== {section.__name__} ==")
        section()


if __name__ == "__main__":
    main()


# ===== 练习 =====
# 1. 给 agent/tools.py 加一个 fetch_order(order_id) 工具，并用 AlwaysCallLLM 调通。
# 2. 让 trimming_demo 的 max_messages=2，观察裁剪规则如何保证工具消息成对。
# 3. 把 ChatSession 接到 Streamlit 的 session_state，实现刷新页面不丢历史。
