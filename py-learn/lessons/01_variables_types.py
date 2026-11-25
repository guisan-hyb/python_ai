"""第 01 课：变量、类型与对象。

C++ 里 `int x = 1;` 会分配一块有类型的栈内存。
Python 里 `x = 1` 只是把名字 x 绑到一个对象上，类型属于对象、不属于名字。

三个必须建立的直觉：
1. 赋值不是拷贝，是把名字重新绑到另一个对象（类比：改指针指向）。
2. 同名可以先后绑定不同类型，合法但不推荐；类型标注能帮工具提前发现错误。
3. 类型标注不参与运行，它只是给人和静态检查器看的注释。

运行：uv run python lessons/01_variables_types.py
"""

from __future__ import annotations

import sys


def binding_vs_copy() -> None:
    a = [1, 2]
    b = a  # 没有拷贝，两个名字指向同一个 list
    b.append(3)
    print(f"a={a} b={b}  a is b -> {a is b}")

    c = a[:]  # 切片产生新对象，相当于 C++ 的拷贝构造
    c.append(4)
    print(f"a={a} c={c}  a is c -> {a is c}")


def inplace_vs_rebind() -> None:
    alias = base = [1]
    base += [2]  # += 对 list 是原地修改，alias 看得到
    print(f"+= 之后 alias={alias} base={base}")

    alias = base = [1]
    base = base + [2]  # + 生成新对象并重新绑定，alias 不受影响
    print(f"+ 之后  alias={alias} base={base}")


def types_live_on_objects() -> None:
    x = 42
    print(f"x={x} type={type(x).__name__} id={id(x)}")
    x = "hello"
    print(f"x={x} type={type(x).__name__} id={id(x)}")


def integers_never_overflow() -> None:
    big = 2**100
    print(f"2**100 = {big}")
    print(f"十进制位数 {len(str(big))}，64 位整型早就溢出了")
    print(f"对象占用 {sys.getsizeof(big)} 字节，位数越多占得越多")


def truthiness() -> None:
    empty_dict: dict[str, int] = {}
    print(f"None 为假：{bool(None)}")
    print(f"空容器/空串为假：{bool([])} {bool(empty_dict)} {bool('')}")
    print(f"bool 是 int 的子类：{isinstance(True, int)}，True + True = {True + True}")


def identity_vs_equality() -> None:
    a = [1, 2]
    b = [1, 2]
    print(f"a == b 比值：{a == b}")
    print(f"a is b 比身份：{a is b}")
    print(f"id 相同才是同一对象：{id(a) == id(b)}")


def hints_do_not_enforce() -> None:
    def add(x: int, y: int) -> int:
        return x + y

    print(f"正常调用：{add(1, 2)}")
    print(f"传字符串照样运行：{add('a', 'b')}；类型检查器才会报警")


def main() -> None:
    for section in (
        binding_vs_copy,
        inplace_vs_rebind,
        types_live_on_objects,
        integers_never_overflow,
        truthiness,
        identity_vs_equality,
        hints_do_not_enforce,
    ):
        print(f"\n== {section.__name__} ==")
        section()


if __name__ == "__main__":
    main()


# ===== 练习（也可以写到 exercises/ex01.py，那里有自动断言）=====
# 1. 写 swap(a, b) 返回 (b, a)，并用两个 list 验证：交换的是别名，没有拷贝元素。
# 2. `a += [3]` 和 `a = a + [3]` 对 a 的别名分别有什么影响？先预测再运行验证。
# 3. 用 id() 证明 `b = a` 与 `b = a[:]` 的区别。
