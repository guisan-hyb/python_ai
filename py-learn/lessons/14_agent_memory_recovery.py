"""第 14 课：Agent 实战（二）—— 记忆、错误恢复与边界。

能跑通的 Agent 和能上线的 Agent，差别全在这一课：
模型会超时、工具会报错、模型会陷入无限调工具。每一层都要有兜底。

本课覆盖：工具报错如何处理、LLM 失败重试、max_steps 防死循环、
多轮会话 + 重试的组合。

运行：uv run python lessons/14_agent_memory_recovery.py
"""

from __future__ import annotations

from typing import Any

from agent.llm import LLM, MockLLM, Reply, ToolCall
from agent.loop import run_agent
from agent.memory import ChatSession


class FlakyLLM:
    """前 failures 次调用抛异常，模拟网关抖动。"""

    def __init__(self, inner: LLM, failures: int = 2) -> None:
        self.inner = inner
        self.remaining = failures
        self.calls = 0
        self.failures = 0

    def chat(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
    ) -> Reply:
        self.calls += 1
        if self.remaining > 0:
            self.remaining -= 1
            self.failures += 1
            raise ConnectionError("模拟网络抖动")
        return self.inner.chat(messages, tools)


class RetryingLLM:
    """给任意 LLM 套一层重试，Agent 上层代码完全不用改（装饰器模式的变体）。"""

    def __init__(self, inner: LLM, retries: int = 2) -> None:
        self.inner = inner
        self.retries = retries

    def chat(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
    ) -> Reply:
        last_error: Exception | None = None
        for attempt in range(1, self.retries + 2):
            try:
                return self.inner.chat(messages, tools)
            except Exception as exc:
                last_error = exc
                print(f"  第 {attempt} 次调用失败：{type(exc).__name__}: {exc}")
        if last_error is None:
            raise RuntimeError("不可能发生：循环没有执行")
        raise last_error


class EndlessToolLLM:
    """永远要求继续调工具，用来验证 max_steps 兜底。"""

    def chat(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
    ) -> Reply:
        return Reply(tool_calls=(ToolCall("calculator", {"expression": "1+1"}),))


def tool_error_is_recoverable() -> None:
    """工具抛异常不会炸掉整个流程，错误文本会回到模型手里。"""
    answer = run_agent("帮我计算 1/0", MockLLM())
    print(f"答案：{answer}")
    print("execute_tool 内部 try/except 把异常转成字符串，模型据此改写计划")


def model_retry() -> None:
    flaky = FlakyLLM(MockLLM(), failures=2)
    llm = RetryingLLM(flaky, retries=2)
    print(f"答案：{run_agent('北京天气怎么样？', llm)}")
    success = flaky.calls - flaky.failures
    print(f"模型被调用 {flaky.calls} 次（失败 {flaky.failures} 次 + 成功 {success} 次）")
    print("成功次数是 2：第一次拿到工具调用，第二次是拿到工具结果后的最终回答")


def step_guard() -> None:
    answer = run_agent("随便算点什么", EndlessToolLLM(), max_steps=3)
    print(f"兜底返回：{answer}")
    print("生产环境还要记 metric：步数触顶次数是 Agent 质量的直接信号")


def session_with_retry() -> None:
    flaky = FlakyLLM(MockLLM(), failures=1)
    session = ChatSession(RetryingLLM(flaky, retries=1), max_messages=6)
    print(f"第一轮：{session.ask('北京天气怎么样？')}")
    print(f"第二轮：{session.ask('那上海的天气呢')}")
    print(f"轮数 {session.turns}，消息数 {len(session.messages)}")
    print("记忆 + 重试 + 工具，这三件事互不干扰，可以自由组合")


def main() -> None:
    for section in (tool_error_is_recoverable, model_retry, step_guard, session_with_retry):
        print(f"\n== {section.__name__} ==")
        section()


if __name__ == "__main__":
    main()


# ===== 练习 =====
# 1. 给 RetryingLLM 加指数退避（0.1s、0.2s、0.4s），并记录失败次数。
# 2. 让 max_steps=1，观察工具调用还没完成就触顶时的返回，思考该给用户什么提示。
# 3. 写一个带超时的 LLM 包装（concurrent.futures + TimeoutError）。
