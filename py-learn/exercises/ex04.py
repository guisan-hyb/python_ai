"""练习 04：控制流与推导式。运行：uv run python exercises/ex04.py"""

from __future__ import annotations


def fizzbuzz(n: int) -> list[str]:
    """返回 1..n 的字符串，3 的倍数 "Fizz"，5 的倍数 "Buzz"，15 的倍数 "FizzBuzz"。"""
    # raise NotImplementedError("TODO")
    ret = []
    for i in range(1, n + 1):
        if i % 15 == 0:
            ret.append("FizzBuzz")
        elif i % 3 == 0:
            ret.append("Fizz")
        elif i % 5 == 0:
            ret.append("Buzz")
        else:
            ret.append(str(i))

    return ret


def flatten(nested: list[object]) -> list[int]:
    """把 [[1, 2], [3, [4, 5]]] 拍平成 [1, 2, 3, 4, 5]（递归）。"""
    # raise NotImplementedError("TODO: isinstance(item, list)")
    ret = []
    for item in nested:
        if isinstance(item, list):
            ret.extend(flatten(item))
        else:
            ret.append(item)
    return ret


def transpose(matrix: list[list[int]]) -> list[list[int]]:
    """转置 [[1, 2], [3, 4]] -> [[1, 3], [2, 4]]，用 zip + 推导式。"""
    # raise NotImplementedError("TODO: 一行 zip(*matrix)")

    # Error:
    # ret = []
    # for list1,list2 in zip(list[0],list[1],strict=True):
    #     ret.append([list1,list2])
    # return ret

    return [list(row) for row in zip(*matrix, strict=False)]


if __name__ == "__main__":
    assert fizzbuzz(5) == ["1", "2", "Fizz", "4", "Buzz"]
    assert fizzbuzz(15)[-1] == "FizzBuzz"
    assert flatten([[1, 2], [3, [4, 5]]]) == [1, 2, 3, 4, 5]
    assert transpose([[1, 2, 3], [4, 5, 6]]) == [[1, 4], [2, 5], [3, 6]]
    print("练习 04 通过")
