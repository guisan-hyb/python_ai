"""练习 07 参考答案。运行：uv run python solutions/sol07.py"""

from __future__ import annotations

import time


class InsufficientFunds(Exception):
    def __init__(self, need: float, have: float) -> None:
        super().__init__(f"需要 {need}，只有 {have}")
        self.need = need
        self.have = have


def withdraw(balance: float, amount: float) -> float:
    if amount > balance:
        raise InsufficientFunds(amount, balance)
    return balance - amount


class Timer:
    def __enter__(self) -> Timer:
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type: object, exc: object, tb: object) -> bool:
        self.elapsed = time.perf_counter() - self.start
        return False


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
