from __future__ import annotations

import pytest

from agent.llm import MockLLM
from agent.loop import run_agent
from agent.tools import calculate, execute_tool, get_weather, openai_tool_schemas


def test_weather_tool_returns_city_data() -> None:
    assert "晴" in get_weather("北京")


def test_calculator_handles_precedence() -> None:
    assert calculate("12*(3+4)").endswith("84")


@pytest.mark.parametrize("payload", ["__import__('os').system('ls')", "1+1; import os"])
def test_calculator_rejects_arbitrary_code(payload: str) -> None:
    with pytest.raises(ValueError):
        calculate(payload)


def test_schemas_have_required_shape() -> None:
    for schema in openai_tool_schemas():
        assert schema["type"] == "function"
        assert "name" in schema["function"]


def test_unknown_tool_returns_error_text() -> None:
    assert "不存在" in execute_tool("nope", {})


def test_agent_uses_tool_then_answers() -> None:
    answer = run_agent("北京天气怎么样？", MockLLM())
    assert "晴" in answer


def test_agent_plain_question_without_tool() -> None:
    answer = run_agent("你好", MockLLM())
    assert "你好" in answer
