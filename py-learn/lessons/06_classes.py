"""第 06 课：类、数据类与鸭子类型。

C++ 的 class 偏「布局 + 访问控制」，Python 的 class 偏「命名空间 + 协议」。
Python 没有真正的 private，也不要求接口继承：能做出同样的动作就算数（鸭子类型）。

本课覆盖：__init__/self、dataclass、property、继承与 super、
__repr__/__eq__/__add__、slots、frozen。

运行：uv run python lessons/06_classes.py
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field


class Manual:
    """手写类：__init__、__repr__、__eq__ 都要自己写。"""

    def __init__(self, name: str, count: int = 0) -> None:
        self.name = name
        self.count = count

    def __repr__(self) -> str:
        return f"Manual(name={self.name!r}, count={self.count})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Manual):
            return NotImplemented
        return (self.name, self.count) == (other.name, other.count)

    def increment(self) -> None:
        self.count += 1


@dataclass
class Point:
    """dataclass 自动生成 __init__/__repr__/__eq__，等价于上面手写那堆。"""

    x: float
    y: float

    def __add__(self, other: Point) -> Point:
        return Point(self.x + other.x, self.y + other.y)

    def norm(self) -> float:
        return (self.x**2 + self.y**2) ** 0.5


@dataclass(frozen=True)
class Config:
    """frozen=True：不可修改、可哈希，适合当 dict 的键。"""

    host: str
    port: int = 8000


@dataclass(slots=True)
class Packed:
    """slots=True：去掉 __dict__，实例更省内存。"""

    x: int
    y: int


@dataclass
class Account:
    owner: str
    _balance: float = field(default=0.0, repr=False)

    @property
    def balance(self) -> float:
        return self._balance

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("金额必须为正")
        self._balance += amount


class Animal:
    def __init__(self, name: str) -> None:
        self.name = name

    def speak(self) -> str:
        return "..."

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.name!r})"


class Dog(Animal):
    def speak(self) -> str:
        return f"{self.name}: 汪"

    def fetch(self) -> str:
        return f"{self.name} 把球捡回来"


def manual_vs_dataclass() -> None:
    a, b = Manual("x"), Manual("x")
    print(f"手写类：{a} 相等? {a == b}")
    p, q = Point(3, 4), Point(1, 2)
    print(f"dataclass：{p} 长度 {p.norm():.2f}")
    print(f"运算符重载：{p} + {q} = {p + q}")


def frozen_and_slots() -> None:
    cfg = Config(host="127.0.0.1")
    try:
        cfg.port = 9000  # type: ignore[misc]
    except Exception as exc:
        print(f"frozen 拒绝赋值：{type(exc).__name__}")
    print(f"frozen 可哈希，能当键：{ {cfg: 'server'} }")

    loose = Manual("n")
    print(f"普通实例有 __dict__，占 {sys.getsizeof(loose)} 字节 + 字典开销")
    print(f"slots 实例 {sys.getsizeof(Packed(1, 2))} 字节，没有 __dict__")


def properties() -> None:
    acc = Account("huoyibo")
    acc.deposit(100)
    print(f"property 只读：{acc.balance}")
    try:
        acc.deposit(-1)
    except ValueError as exc:
        print(f"校验生效：{exc}")


def inheritance() -> None:
    dog = Dog("旺财")
    print(f"{dog} 说 {dog.speak()}")
    print(f"MRO（方法解析顺序）：{[cls.__name__ for cls in Dog.__mro__]}")
    print("Python 支持多继承，但日常优先用组合，C++ 也是这个结论")


def duck_typing() -> None:
    class Cat:
        def speak(self) -> str:
            return "喵"

    for obj in (Dog("旺财"), Cat()):
        print(f"{type(obj).__name__}.speak() -> {obj.speak()}（没有共同基类也能用）")


def main() -> None:
    for section in (manual_vs_dataclass, frozen_and_slots, properties, inheritance, duck_typing):
        print(f"\n== {section.__name__} ==")
        section()


if __name__ == "__main__":
    main()


# ===== 练习 =====
# 1. 用 dataclass 实现 Vector2D，支持 __add__ / __mul__ / __abs__。
# 2. 给 Account 加 withdraw()，余额不足时抛自定义异常（第 07 课会讲）。
# 3. 用 slots=True 和普通 dataclass 各建 10 万个实例，比较进程内存占用。
