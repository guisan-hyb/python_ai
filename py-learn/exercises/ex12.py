"""练习 12：工程化。

这个文件本身就是一个 pytest 文件，补完实现后运行：
    uv run pytest exercises/ex12.py -v
"""

from __future__ import annotations

import pytest


def clamp(value: int, low: int, high: int) -> int:
    """把 value 限制在 [low, high] 区间内。low > high 时抛 ValueError。"""
    raise NotImplementedError("TODO")


def parse_int(text: str, default: int = 0) -> int:
    """解析失败返回 default，不抛异常。"""
    raise NotImplementedError("TODO")


@pytest.mark.parametrize(
    ("value", "expected"),
    [(-5, 0), (0, 0), (5, 5), (15, 10)],
)
def test_clamp(value: int, expected: int) -> None:
    assert clamp(value, 0, 10) == expected


def test_clamp_rejects_bad_range() -> None:
    with pytest.raises(ValueError):
        clamp(1, 10, 0)


@pytest.mark.parametrize(("text", "expected"), [("42", 42), ("abc", 0), ("", 7)])
def test_parse_int(text: str, expected: int) -> None:
    default = 7 if text == "" else 0
    assert parse_int(text, default) == expected
