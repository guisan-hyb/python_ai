"""第 08 课：迭代器与生成器。

C++ 的迭代器是一对指针；Python 的迭代器是实现了 __iter__ / __next__ 的对象。
生成器（yield）让你用「写循环」的方式产出「迭代器」，是 Python 最省内存的惯用法。

本课覆盖：迭代协议、StopIteration、生成器函数、惰性求值、
生成器表达式 vs 列表推导、itertools、yield from。

运行：uv run python lessons/08_iterators_generators.py
"""

from __future__ import annotations

import itertools
import sys
from collections.abc import Iterator


class Countdown:
    """手写迭代器：__iter__ 返回自身，__next__ 到末尾抛 StopIteration。"""

    def __init__(self, start: int) -> None:
        self.current = start

    def __iter__(self) -> Countdown:
        return self

    def __next__(self) -> int:
        if self.current <= 0:
            raise StopIteration
        self.current -= 1
        return self.current + 1


def generator_basics() -> None:
    def countdown(start: int) -> Iterator[int]:
        while start > 0:
            yield start  # 暂停在这里，下次 next() 继续
            start -= 1

    print(f"生成器可直接 for：{list(countdown(3))}")
    gen = countdown(3)
    print(f"手动 next：{next(gen)} {next(gen)}")


def laziness() -> None:
    calls: list[int] = []

    def tracked(n: int) -> Iterator[int]:
        for i in range(n):
            calls.append(i)
            yield i * i

    gen = tracked(1_000_000)
    print(f"创建生成器时计算了几次？{len(calls)}")
    print(f"只取前 3 个：{list(itertools.islice(gen, 3))}")
    print(f"这时才计算了 {len(calls)} 次 —— 惰性求值")


def memory_compare() -> None:
    as_list = [n for n in range(100_000)]
    as_gen = (n for n in range(100_000))
    print(f"列表 {sys.getsizeof(as_list)} 字节，生成器 {sys.getsizeof(as_gen)} 字节")


def itertools_demo() -> None:
    evens = (n for n in itertools.count(0) if n % 2 == 0)
    print(f"islice 取前 5 个偶数：{list(itertools.islice(evens, 5))}")
    print(f"chain 拼接：{list(itertools.chain([1, 2], [3], range(4, 6)))}")
    words = sorted(["a", "bb", "cc", "d"], key=len)
    groups = [(length, list(group)) for length, group in itertools.groupby(words, key=len)]
    print(f"groupby 按长度分组：{groups}")


def yield_from() -> None:
    def inner() -> Iterator[int]:
        yield from (1, 2)

    def outer() -> Iterator[int]:
        yield 0
        yield from inner()  # 把子生成器整个委托出去
        yield 3

    print(f"yield from：{list(outer())}")


def main() -> None:
    for section in (generator_basics, laziness, memory_compare, itertools_demo, yield_from):
        print(f"\n== {section.__name__} ==")
        section()
    print(f"\n手写迭代器：{list(Countdown(3))}")


if __name__ == "__main__":
    main()


# ===== 练习 =====
# 1. 写 chunked(iterable, size) 生成器，把序列切成固定大小的块。
# 2. 写 read_lines(path) 逐行读大文件，不要一次 readlines()，对比内存占用。
# 3. 用 itertools 实现「前 n 个斐波那契数」，要求惰性、可无限。
