"""练习 12 参考答案。

运行：uv run pytest solutions/sol12.py -v
"""

from __future__ import annotations

import pytest


def clamp(value: int, low: int, high: int) -> int:
    if low > high:
        raise ValueError("low 不能大于 high")
    return max(low, min(value, high))


def parse_int(text: str, default: int = 0) -> int:
    try:
        return int(text)
    except ValueError:
        return default


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
