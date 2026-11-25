"""练习 05：函数与装饰器。运行：uv run python exercises/ex05.py"""

from __future__ import annotations

from collections.abc import Callable


def make_multiplier(factor: int) -> Callable[[int], int]:
    """返回一个函数，把入参乘以 factor（闭包）。"""
    raise NotImplementedError("TODO")


def retry(times: int) -> Callable[[Callable[[], str]], Callable[[], str]]:
    """装饰器：被装饰函数抛异常时最多重试 times 次，全失败再抛出。

    提示：用 functools.wraps 保留原函数名。
    """
    raise NotImplementedError("TODO: 用 functools.wraps 包装")


if __name__ == "__main__":
    triple = make_multiplier(3)
    assert triple(7) == 21
    assert make_multiplier(0)(5) == 0

    attempts = 0

    @retry(times=2)
    def flaky() -> str:
        global attempts
        attempts += 1
        if attempts < 3:
            raise RuntimeError("还没成功")
        return "成功"

    assert flaky() == "成功"
    assert attempts == 3
    print("练习 05 通过")
