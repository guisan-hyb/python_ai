"""练习 06 参考答案。运行：uv run python solutions/sol06.py"""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass
class Vector2D:
    x: float
    y: float

    def __add__(self, other: Vector2D) -> Vector2D:
        return Vector2D(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar: float) -> Vector2D:
        return Vector2D(self.x * scalar, self.y * scalar)

    def __abs__(self) -> float:
        return math.hypot(self.x, self.y)


@dataclass(frozen=True)
class CacheKey:
    name: str
    version: int


if __name__ == "__main__":
    a, b = Vector2D(1, 2), Vector2D(3, 4)
    assert a + b == Vector2D(4, 6)
    assert a * 3 == Vector2D(3, 6)
    assert abs(Vector2D(3, 4)) == 5.0
    assert {CacheKey("api", 1): "v1"}[CacheKey("api", 1)] == "v1"
    print("练习 06 通过")
