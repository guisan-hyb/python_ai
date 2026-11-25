"""练习 10 参考答案。运行：uv run python solutions/sol10.py"""

from __future__ import annotations

import asyncio
import time


async def wait_and_return(delay: float) -> float:
    await asyncio.sleep(delay)
    return delay


async def fetch_all(delays: list[float]) -> list[float]:
    return list(await asyncio.gather(*(wait_and_return(delay) for delay in delays)))


if __name__ == "__main__":
    delays = [0.1, 0.1, 0.1]

    start = time.perf_counter()
    result = asyncio.run(fetch_all(delays))
    cost = time.perf_counter() - start

    assert result == delays
    assert cost < 0.25, f"没有并发，耗时 {cost:.2f}s"
    print(f"练习 10 通过，耗时 {cost:.2f}s")
