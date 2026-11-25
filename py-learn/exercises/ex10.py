"""练习 10：并发与异步。运行：uv run python exercises/ex10.py"""

from __future__ import annotations

import asyncio
import time


async def wait_and_return(delay: float) -> float:
    """异步等待 delay 秒后返回 delay。"""
    raise NotImplementedError("TODO: asyncio.sleep")


async def fetch_all(delays: list[float]) -> list[float]:
    """并发执行所有等待，返回按输入顺序排列的结果列表。"""
    raise NotImplementedError("TODO: asyncio.gather")


if __name__ == "__main__":
    delays = [0.1, 0.1, 0.1]

    start = time.perf_counter()
    result = asyncio.run(fetch_all(delays))
    cost = time.perf_counter() - start

    assert result == delays
    assert cost < 0.25, f"没有并发，耗时 {cost:.2f}s（串行会是 0.3s）"
    print(f"练习 10 通过，耗时 {cost:.2f}s")
