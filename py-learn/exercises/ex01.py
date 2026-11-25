"""练习 01：变量与类型。

把每个 TODO 补完，然后运行：uv run python exercises/ex01.py
全部断言通过会打印「练习 01 通过」。
"""

from __future__ import annotations


def swap(a: object, b: object) -> tuple[object, object]:
    """返回 (b, a)。注意要求的语义：交换的是引用，不是复制元素。"""
    tmp = a
    a = b
    b = tmp
    return (a, b)


def shared_mutation() -> tuple[list[int], list[int]]:
    """返回两个名字，它们指向同一个 list，内容为 [1, 2, 3]。"""
    # raise NotImplementedError("TODO: 让两个名字指向同一个 list，并在其中一个上 append")
    a = b = []
    a.append(1)
    a.append(2)
    b.append(3)
    return (a, b)


def is_same_object(a: object, b: object) -> bool:
    """不写 a is b，用 id() 判断两个名字是否指向同一对象。"""
    # raise NotImplementedError("TODO: 用 id() 实现")
    return id(a) == id(b)


if __name__ == "__main__":
    assert swap(1, 2) == (2, 1)

    x, y = [1], [2]
    rx, ry = swap(x, y)
    assert rx is y and ry is x, "swap 必须交换引用，不能复制元素"

    a, b = shared_mutation()
    assert a is b and a == [1, 2, 3]
    assert is_same_object(a, b) is True
    assert is_same_object([1], [1]) is False

    print("练习 01 通过")
