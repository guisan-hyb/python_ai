"""练习 08 参考答案。运行：uv run python solutions/sol08.py"""

from __future__ import annotations

import itertools
from collections.abc import Iterable, Iterator


def chunked(items: Iterable[int], size: int) -> Iterator[list[int]]:
    buffer: list[int] = []
    for item in items:
        buffer.append(item)
        if len(buffer) == size:
            yield buffer
            buffer = []
    if buffer:
        yield buffer


def first(n: int, items: Iterable[int]) -> list[int]:
    return list(itertools.islice(items, n))


def fib() -> Iterator[int]:
    current, following = 0, 1
    while True:
        yield current
        current, following = following, current + following


if __name__ == "__main__":
    assert list(chunked(range(5), 2)) == [[0, 1], [2, 3], [4]]
    assert first(3, itertools.count(10)) == [10, 11, 12]
    assert list(itertools.islice(fib(), 8)) == [0, 1, 1, 2, 3, 5, 8, 13]
    print("练习 08 通过")
