"""练习 07：异常与上下文管理器。运行：uv run python exercises/ex07.py"""

from __future__ import annotations

import time


class InsufficientFunds(Exception):
    """TODO: 让异常带上 need / have 两个结构化字段。"""


def withdraw(balance: float, amount: float) -> float:
    """余额不足时抛 InsufficientFunds，否则返回新余额。"""
    raise NotImplementedError("TODO")


class Timer:
    """TODO: __enter__ 用 time.perf_counter() 记开始时间，
    __exit__ 算出 elapsed 秒存到 self.elapsed。
    """

    def __enter__(self) -> Timer:
        raise NotImplementedError("TODO")

    def __exit__(self, exc_type: object, exc: object, tb: object) -> bool:
        raise NotImplementedError("TODO: 返回 False，别吞异常")


if __name__ == "__main__":
    assert withdraw(100, 40) == 60

    try:
        withdraw(100, 150)
    except InsufficientFunds as exc:
        assert exc.need == 150 and exc.have == 100
    else:
        raise AssertionError("没有抛异常")

    timer = Timer()
    with timer:
        time.sleep(0.01)
    assert timer.elapsed >= 0.01

    print("练习 07 通过")
