"""第 10 课：并发与异步。

C++ 里线程是真并行（多核），代价是锁和内存模型；
CPython 有 GIL，同一时刻只有一个线程执行字节码，所以：

    IO 密集（网络、磁盘、sleep） -> 线程或 asyncio 都有用，等待时不占 GIL
    CPU 密集（计算）             -> 线程帮不上忙，要用 multiprocessing

本课覆盖：串行 vs 线程池的耗时对比、asyncio 的 async/await/gather、
什么场景该选哪个。

运行：uv run python lessons/10_concurrency_async.py
"""

from __future__ import annotations

import asyncio
import time
from concurrent.futures import ThreadPoolExecutor

TASKS = [("a", 0.2), ("b", 0.2), ("c", 0.2), ("d", 0.2)]


def fetch(name: str, delay: float) -> str:
    """模拟一次网络请求：睡 delay 秒。"""
    time.sleep(delay)
    return f"{name} 完成"


def serial() -> float:
    start = time.perf_counter()
    for name, delay in TASKS:
        fetch(name, delay)
    return time.perf_counter() - start


def threaded() -> float:
    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=len(TASKS)) as pool:
        list(pool.map(lambda task: fetch(*task), TASKS))
    return time.perf_counter() - start


async def aio_fetch(name: str, delay: float) -> str:
    await asyncio.sleep(delay)  # 让出事件循环，其它任务继续跑
    return f"{name} 完成"


async def aio_all() -> list[str]:
    return await asyncio.gather(*(aio_fetch(name, delay) for name, delay in TASKS))


def asyncio_demo() -> None:
    start = time.perf_counter()
    results = asyncio.run(aio_all())
    cost = time.perf_counter() - start
    print(f"asyncio.gather 结果：{results}")
    print(f"asyncio 耗时 {cost:.2f}s（串行需要 {sum(d for _, d in TASKS):.2f}s）")


def compare() -> None:
    print(f"串行：{serial():.2f}s")
    print(f"4 线程：{threaded():.2f}s  <- 等待 IO 时线程会释放 GIL")
    print("如果是纯计算任务，多线程不会有这个加速，要用 multiprocessing")


def cpu_bound_note() -> None:
    print("CPU 密集：concurrent.futures.ProcessPoolExecutor 或 multiprocessing")
    print("asyncio 适合：高并发网络请求、WebSocket、数据库连接池")
    print("线程适合：少量阻塞调用（老库没有 async 版本时）")


def main() -> None:
    for section in (compare, asyncio_demo, cpu_bound_note):
        print(f"\n== {section.__name__} ==")
        section()


if __name__ == "__main__":
    main()


# ===== 练习 =====
# 1. 用 asyncio 并发请求 10 个 URL（可用 httpx.AsyncClient 访问 httpbin），对比串行耗时。
# 2. 写一个线程安全的计数器，分别用 Lock 和不加锁跑 10 万次，观察结果差异。
# 3. 判断：下载 100 张图片、计算 100 万个素数，各该用哪种并发模型？
