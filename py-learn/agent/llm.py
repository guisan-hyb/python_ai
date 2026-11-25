"""LLM 抽象层。

刻意按 OpenAI Chat Completions 的形状设计（messages 进、Reply 出），
因为 DeepSeek、Qwen、vLLM、公司内部网关大多兼容这套接口。
将来接真实模型时，只需新增一个实现类替换 MockLLM，上层代码不用改。
"""

from __future__ import annotations

import json
import re
import uuid
from dataclasses import dataclass, field
from typing import Any, Protocol


@dataclass(frozen=True)
class ToolCall:
    """模型请求调用一个工具，参数已经解析成 dict。"""

    name: str
    arguments: dict[str, Any]
    id: str = field(default_factory=lambda: f"call_{uuid.uuid4().hex[:8]}")


@dataclass(frozen=True)
class Reply:
    """模型的一次回复：要么是最终答案，要么是一批工具调用。"""

    content: str = ""
    tool_calls: tuple[ToolCall, ...] = ()


class LLM(Protocol):
    def chat(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
    ) -> Reply: ...


class MockLLM:
    """假模型：不联网、不花钱、结果确定，用于把 Agent 循环跑通。

    规则很简单：
    - 收到用户问题：含「天气」就调 weather，「算/计算」就调 calculator，否则直接回答。
    - 收到工具结果：把它整理成一句人话回复。
    真实模型的「判断该调哪个工具」能力由它自己完成，这里用关键词模拟。
    """

    def chat(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
    ) -> Reply:
        last = messages[-1]

        if last["role"] == "tool":
            return Reply(content=f"工具 {last['name']} 返回：{last['content']}")

        text: str = last["content"]

        city = _find_city(text)
        if "天气" in text and city:
            return Reply(tool_calls=(ToolCall("get_weather", {"city": city}),))

        expression = _find_expression(text)
        if expression and ("算" in text or "计算" in text):
            return Reply(tool_calls=(ToolCall("calculator", {"expression": expression}),))

        return Reply(content=f"（Mock 模型回复）我收到了你的问题：{text}")


def _find_city(text: str) -> str | None:
    match = re.search(r"(北京|上海|广州|深圳|杭州|成都|西安|南京|武汉|苏州)", text)
    return match.group(1) if match else None


def _find_expression(text: str) -> str | None:
    match = re.search(r"[\d.]+(?:\s*[+\-*/]\s*[\d.]+)+", text)
    return match.group(0).replace(" ", "") if match else None


class OpenAICompatibleLLM:
    """真实模型接入模板（需要 API Key 才能用，默认不启用）。

    用法：
        llm = OpenAICompatibleLLM(base_url="https://api.deepseek.com", model="deepseek-chat")
        llm = OpenAICompatibleLLM(base_url="https://api.openai.com/v1", model="gpt-4o-mini")
    """

    def __init__(self, base_url: str, model: str, api_key: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.api_key = api_key

    def chat(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
    ) -> Reply:
        import httpx

        payload: dict[str, Any] = {"model": self.model, "messages": messages}
        if tools:
            payload["tools"] = tools

        response = httpx.post(
            f"{self.base_url}/chat/completions",
            json=payload,
            headers={"Authorization": f"Bearer {self.api_key}"},
            timeout=60,
        )
        response.raise_for_status()
        choice = response.json()["choices"][0]["message"]

        calls = tuple(
            ToolCall(
                name=call["function"]["name"],
                arguments=json.loads(call["function"]["arguments"] or "{}"),
                id=call.get("id", f"call_{uuid.uuid4().hex[:8]}"),
            )
            for call in choice.get("tool_calls") or []
        )
        return Reply(content=choice.get("content") or "", tool_calls=calls)
