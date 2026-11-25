"""练习 05 参考答案。运行：uv run python solutions/sol05.py"""

from __future__ import annotations

import functools
from collections.abc import Callable


def make_multiplier(factor: int) -> Callable[[int], int]:
    def multiply(value: int) -> int:
        return value * factor

    return multiply


def retry(times: int) -> Callable[[Callable[[], str]], Callable[[], str]]:
    def decorator(func: Callable[[], str]) -> Callable[[], str]:
        @functools.wraps(func)
        def wrapper() -> str:
            last_error: Exception | None = None
            for _ in range(times + 1):
                try:
                    return func()
                except Exception as exc:
                    last_error = exc
            if last_error is None:
                raise RuntimeError("不可能发生")
            raise last_error

        return wrapper

    return decorator


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
