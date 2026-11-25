"""练习 08：迭代器与生成器。运行：uv run python exercises/ex08.py"""

from __future__ import annotations

import itertools
from collections.abc import Iterable, Iterator


def chunked(items: Iterable[int], size: int) -> Iterator[list[int]]:
    """把序列切成固定大小的块，最后一块可以不满。"""
    raise NotImplementedError("TODO: 用生成器 + 切片")


def first(n: int, items: Iterable[int]) -> list[int]:
    """惰性取前 n 个元素，不要先把整个迭代器转成 list 再切片。"""
    raise NotImplementedError("TODO: 提示 itertools.islice")


def fib() -> Iterator[int]:
    """无限斐波那契生成器：0, 1, 1, 2, 3, 5, ..."""
    raise NotImplementedError("TODO")


if __name__ == "__main__":
    assert list(chunked(range(5), 2)) == [[0, 1], [2, 3], [4]]
    assert first(3, itertools.count(10)) == [10, 11, 12]
    assert list(itertools.islice(fib(), 8)) == [0, 1, 1, 2, 3, 5, 8, 13]
    print("练习 08 通过")
