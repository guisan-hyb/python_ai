"""给 C++ 背景的第一课：把熟悉的概念换成 Python 写法。

直接运行：uv run python basics/01_cpp_vs_python.py
"""

from __future__ import annotations

from dataclasses import dataclass


def variables() -> None:
    # C++: int x = 1;  Python: 没有声明，类型跟着值走（但可以标注）
    x: int = 1
    name: str = "huoyibo"
    ratio: float = 0.75
    flags: list[bool] = [True, False]
    print(f"变量：{x=} {name=} {ratio=} {flags=}")


def containers() -> None:
    # C++: std::vector / std::map / std::set
    nums = [3, 1, 2]
    nums.sort()
    lookup = {"北京": 10, "上海": 21}
    unique = set([1, 2, 2, 3])  # set 自动去重，C++ 里要 insert 后看 size
    print(f"列表：{nums}  字典：{lookup}  集合：{unique}")
    print(f"区间切片（C++ 没有直接对应）：{nums[1:]}")


@dataclass
class Point:
    """C++ 的 struct/class，Python 用 dataclass 一行搞定。"""

    x: float
    y: float

    def norm(self) -> float:
        return (self.x**2 + self.y**2) ** 0.5


def classes() -> None:
    p = Point(3, 4)
    print(f"对象：{p}  长度：{p.norm()}")


def comprehensions() -> None:
    # C++ 里要写 for 循环 + push_back，Python 一行
    squares = [n * n for n in range(6)]
    even = {n for n in range(10) if n % 2 == 0}
    print(f"列表推导：{squares}  集合推导：{even}")


def exceptions() -> None:
    try:
        _ = 1 / 0
    except ZeroDivisionError as exc:
        print(f"异常：{type(exc).__name__}: {exc}")


if __name__ == "__main__":
    variables()
    containers()
    classes()
    comprehensions()
    exceptions()
