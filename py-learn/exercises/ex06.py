"""练习 06：类与 dataclass。运行：uv run python exercises/ex06.py"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Vector2D:
    """TODO: 补全下面三个方法。"""

    x: float
    y: float

    def __add__(self, other: Vector2D) -> Vector2D:
        raise NotImplementedError("TODO: 逐分量相加，返回新的 Vector2D")

    def __mul__(self, scalar: float) -> Vector2D:
        raise NotImplementedError("TODO: 数乘")

    def __abs__(self) -> float:
        raise NotImplementedError("TODO: 返回模长")


@dataclass(frozen=True)
class CacheKey:
    """这个类不用改：体会 frozen 让实例可哈希、能当 dict 的键。"""

    name: str
    version: int


if __name__ == "__main__":
    a, b = Vector2D(1, 2), Vector2D(3, 4)
    assert a + b == Vector2D(4, 6)
    assert a * 3 == Vector2D(3, 6)
    assert abs(Vector2D(3, 4)) == 5.0
    assert {CacheKey("api", 1): "v1"}[CacheKey("api", 1)] == "v1"
    print("练习 06 通过")
