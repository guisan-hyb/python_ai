"""对话记忆：多轮上下文 + 窗口裁剪。

C++ 类比：这不是 std::vector::push_back，而是一个有容量上限的环形缓冲。
模型上下文长度有限，所以旧消息必须裁掉；但 tool 消息不能和它的
assistant tool_calls 拆散，否则下一轮 API 调用会直接报错。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from agent.llm import LLM
from agent.loop import SYSTEM_PROMPT, run_conversation
from agent.tools import Tool


@dataclass
class ChatSession:
    """把 LLM + 工具表 + 消息历史绑在一起，对外只暴露 ask()。"""

    llm: LLM
    max_messages: int = 12
    registry: dict[str, Tool] | None = None
    messages: list[dict[str, Any]] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.messages:
            self.messages.append({"role": "system", "content": SYSTEM_PROMPT})

    def ask(self, text: str) -> str:
        self.messages.append({"role": "user", "content": text})
        answer, _ = run_conversation(self.messages, self.llm, registry=self.registry)
        self.trim()
        return answer

    def trim(self) -> None:
        """保留 system + 最近 max_messages 条，且不能从半条工具调用中间开始。"""
        system, rest = self.messages[0], self.messages[1:]
        keep = rest[-self.max_messages :]
        while keep and keep[0].get("role") == "tool":
            keep = keep[1:]
        self.messages[:] = [system, *keep]

    def reset(self) -> None:
        self.messages[:] = [{"role": "system", "content": SYSTEM_PROMPT}]

    @property
    def turns(self) -> int:
        return sum(1 for message in self.messages if message["role"] == "user")

    def roles(self) -> list[str]:
        """调试用：看一眼当前上下文由哪些角色组成。"""
        return [str(message["role"]) for message in self.messages]
