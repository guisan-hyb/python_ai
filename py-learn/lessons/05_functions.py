"""第 05 课：函数与参数。

C++ 默认按值传递，要用引用得写 `T&`；Python 没有这个选择——
所有参数都是「对象引用的传递」：函数收到的是同一个对象的引用，
能不能改到外面，取决于你对这个对象做了什么（改内容 vs 重新绑定名字）。

本课覆盖：参数传递、可变默认值陷阱、*args/**kwargs、
仅位置/仅关键字参数、闭包、lambda、装饰器。

运行：uv run python lessons/05_functions.py
"""

from __future__ import annotations

import functools
import sys
import time
from collections.abc import Callable


def call_by_object_reference() -> None:
    def add_item(bucket: list[int]) -> None:
        bucket.append(99)  # 改的是同一个 list 的内容

    def rebind(bucket: list[int]) -> list[int]:
        bucket = [0]  # 只改了本地名字，外面看不见
        bucket.append(1)
        return bucket

    items = [1]
    add_item(items)
    print(f"函数里 append，外面能看到：{items}")
    returned = rebind(items)
    print(f"函数里重新绑定只影响函数内：外面还是 {items}，返回的是 {returned}")
    print("所以不存在「值传递/引用传递」之争，叫 call by object reference")


def mutable_default_trap() -> None:
    def append_bad(item: int, bucket: list[int] = []) -> list[int]:  # noqa: B006
        bucket.append(item)
        return bucket

    def append_good(item: int, bucket: list[int] | None = None) -> list[int]:
        target = [] if bucket is None else bucket
        target.append(item)
        return target

    print(f"错误写法第一次：{append_bad(1)}")
    print(f"错误写法第二次：{append_bad(2)}  <- 默认值只创建一次，被复用了")
    print(f"正确写法：{append_good(1)} / {append_good(2)}")


def argument_kinds() -> None:
    def request(url: str, /, *, method: str = "GET", **headers: str) -> str:
        detail = ",".join(f"{k}={v}" for k, v in headers.items())
        return f"{method} {url} [{detail}]"

    print(request("/api", method="POST", token="abc"))
    try:
        request(url="/api")  # type: ignore[call-arg]
    except TypeError as exc:
        print(f"url 被 / 设成仅位置参数，所以传 url= 会报错：{exc}")


def varargs() -> None:
    def total(*numbers: float, scale: float = 1.0) -> float:
        return sum(numbers) * scale

    print(f"*args 收集成元组：{total(1, 2, 3, scale=2)}")


def closures() -> None:
    def make_counter() -> Callable[[], int]:
        count = 0

        def counter() -> int:
            nonlocal count  # 没有这句会变成局部变量
            count += 1
            return count

        return counter

    tick = make_counter()
    print(f"闭包持有状态：{[tick() for _ in range(3)]}")


def lambdas() -> None:
    pairs = [("b", 2), ("a", 1)]
    print(f"按第一个元素排序：{sorted(pairs, key=lambda p: p[0])}")
    print(f"按第二个元素倒序：{sorted(pairs, key=lambda p: p[1], reverse=True)}")


def decorators() -> None:
    def timed(func: Callable[[int], str]) -> Callable[[int], str]:
        @functools.wraps(func)  # 保留原函数名/文档，否则调试时看不到真名
        def wrapper(n: int) -> str:
            start = time.perf_counter()
            result = func(n)
            cost = (time.perf_counter() - start) * 1000
            return f"{result}（耗时 {cost:.3f} ms）"

        return wrapper

    @timed
    def work(n: int) -> str:
        return f"处理 {n} 条"

    print(work(10))
    print(f"装饰器没有吃掉函数名：{work.__name__}")


def recursion() -> None:
    print(f"默认递归深度 {sys.getrecursionlimit()}，C++ 是栈溢出，Python 会抛 RecursionError")

    def factorial(n: int) -> int:
        return 1 if n <= 1 else n * factorial(n - 1)

    print(f"10! = {factorial(10)}")
    print("深递归建议改写成循环，或提高 sys.setrecursionlimit 并配足栈")


def main() -> None:
    for section in (
        call_by_object_reference,
        mutable_default_trap,
        argument_kinds,
        varargs,
        closures,
        lambdas,
        decorators,
        recursion,
    ):
        print(f"\n== {section.__name__} ==")
        section()


if __name__ == "__main__":
    main()


# ===== 练习 =====
# 1. 写一个 @retry(times=3) 装饰器，被装饰函数抛异常时重试，全部失败才抛出。
# 2. 写 make_multiplier(n) 返回一个函数，验证闭包不会被循环变量串掉。
# 3. 解释为什么 `def f(x, acc=[])` 的 acc 在多次调用间共享。
