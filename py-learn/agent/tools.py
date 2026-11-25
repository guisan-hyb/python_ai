"""工具注册表。

工具 = 名字 + 描述 + 参数 JSON Schema + 可执行函数。
模型只负责「选工具、填参数」，真正执行永远发生在你这边——这是 Agent 的安全边界。
"""

from __future__ import annotations

import ast
import operator
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Tool:
    name: str
    description: str
    parameters: dict[str, Any]
    func: Callable[..., str]

    def to_openai_schema(self) -> dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters,
            },
        }


def get_weather(city: str) -> str:
    fake_db = {
        "北京": "晴，12~23℃，北风 2 级",
        "上海": "多云，18~25℃，东南风 3 级",
        "深圳": "雷阵雨，24~30℃，南风 2 级",
        "杭州": "小雨，17~22℃，微风",
    }
    return fake_db.get(city, f"{city}：暂无数据（示例工具只内置了 4 个城市）")


_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
}


def calculate(expression: str) -> str:
    """用 AST 白名单求值，避免 eval 带来的任意代码执行。"""

    def _eval(node: ast.AST) -> float:
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, int | float):
            return float(node.value)
        if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
            return _OPS[type(node.op)](_eval(node.left), _eval(node.right))
        if isinstance(node, ast.UnaryOp) and type(node.op) in _OPS:
            return _OPS[type(node.op)](_eval(node.operand))
        raise ValueError(f"不支持的表达式：{ast.dump(node)}")

    try:
        tree = ast.parse(expression, mode="eval")
    except SyntaxError as exc:
        raise ValueError(f"表达式不合法：{expression}") from exc

    value = _eval(tree)
    return f"{expression} = {value:g}"


TOOL_REGISTRY: dict[str, Tool] = {
    tool.name: tool
    for tool in (
        Tool(
            name="get_weather",
            description="查询指定城市的天气。",
            parameters={
                "type": "object",
                "properties": {"city": {"type": "string", "description": "城市名，如 北京"}},
                "required": ["city"],
            },
            func=get_weather,
        ),
        Tool(
            name="calculator",
            description="计算四则运算表达式，例如 12*(3+4)。",
            parameters={
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "只含数字和 + - * / ( ) 的表达式",
                    }
                },
                "required": ["expression"],
            },
            func=calculate,
        ),
    )
}


def openai_tool_schemas(registry: dict[str, Tool] | None = None) -> list[dict[str, Any]]:
    """把工具表转成模型的 tools 参数。传 registry 可以只暴露一部分工具。"""
    tools = TOOL_REGISTRY if registry is None else registry
    return [tool.to_openai_schema() for tool in tools.values()]


def execute_tool(
    name: str,
    arguments: dict[str, Any],
    registry: dict[str, Tool] | None = None,
) -> str:
    tools = TOOL_REGISTRY if registry is None else registry
    tool = tools.get(name)
    if tool is None:
        return f"错误：不存在名为 {name} 的工具"
    try:
        return tool.func(**arguments)
    except Exception as exc:  # 工具出错要回给模型，而不是让整个流程崩掉
        return f"错误：{type(exc).__name__}: {exc}"
