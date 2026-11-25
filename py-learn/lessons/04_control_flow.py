"""第 04 课：控制流与推导式。

C++ 的 for 是「计数器 + 条件」，Python 的 for 是「遍历可迭代对象」。
习惯了 range/enumerate/zip 之后，下标循环基本会消失。

本课覆盖：if/elif、for-else、while-else、range、enumerate、zip、
推导式、海象运算符、match-case。

运行：uv run python lessons/04_control_flow.py
"""

from __future__ import annotations


def branches() -> None:
    def grade(score: int) -> str:
        if score >= 90:
            return "A"
        elif score >= 60:  # Python 没有 switch 的历史包袱，elif 就是 else if
            return "B"
        return "C"

    print([f"{s}->{grade(s)}" for s in (95, 72, 30)])
    print(f"链式比较 0 <= n <= 100：{0 <= 72 <= 100}")  # C++ 里会写错成 (0<=n)<=100


def for_else() -> None:
    for n in (3, 7, 11):
        if n % 2 == 0:
            break
    else:
        print("没有偶数时执行 else（找质数类的逻辑很好用）")

    while_else_count = 0
    while while_else_count < 3:
        while_else_count += 1
    else:
        print(f"while-else 同理，计数到 {while_else_count}")


def looping() -> None:
    print(f"range(2, 10, 3) -> {list(range(2, 10, 3))}")
    names = ["a", "b"]
    for i, name in enumerate(names, start=1):
        print(f"  {i}. {name}")
    for name, score in zip(names, [90, 85], strict=True):
        print(f"  {name}={score}")


def comprehensions() -> None:
    squares = [n * n for n in range(1, 6)]
    print(f"列表推导 {squares}")
    print(f"带条件 {[n for n in squares if n % 2]}")
    name_length = {word: len(word) for word in ("aa", "bbb")}
    print(f"字典推导 {name_length}")
    lengths = sorted({len(word) for word in ("aa", "bb", "c")})
    print(f"集合推导自动去重 {lengths}")
    print(f"生成器表达式省内存：sum = {sum(n * n for n in range(10**6))}")


def walrus() -> None:
    values = [1, 2, 3]
    if (size := len(values)) > 2:
        print(f"海象运算符先赋值再判断：size={size}")
    if (n := int("123")) and n > 100:
        print(f"赋值表达式的值可以直接用：n={n}")


def pattern_matching() -> None:
    def describe(value: object) -> str:
        match value:
            case 0:
                return "零"
            case int() as n if n < 0:  # 带守卫条件
                return f"负数 {n}"
            case [x, y]:  # 解构序列
                return f"二元组 {x},{y}"
            case {"type": "user", "id": uid}:  # 解构字典
                return f"用户 {uid}"
            case _:
                return "其它"

    for sample in (0, -5, [1, 2], {"type": "user", "id": 7}, "abc"):
        print(f"  {sample!r} -> {describe(sample)}")


def main() -> None:
    for section in (branches, for_else, looping, comprehensions, walrus, pattern_matching):
        print(f"\n== {section.__name__} ==")
        section()


if __name__ == "__main__":
    main()


# ===== 练习 =====
# 1. 用 match-case 实现 FizzBuzz（3 的倍数、5 的倍数、15 的倍数）。
# 2. 写 flatten(nested) 把 [[1,2],[3,[4]]] 拍平成 [1,2,3,4]（提示：递归 + isinstance）。
# 3. 用 zip 和推导式实现矩阵转置 [[1,2],[3,4]] -> [[1,3],[2,4]]。
