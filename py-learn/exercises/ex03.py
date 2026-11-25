"""练习 03：容器与拷贝。运行：uv run python exercises/ex03.py"""

from __future__ import annotations

from collections.abc import Callable, Iterable


def dedupe(items: Iterable[str]) -> list[str]:
    """去重，同时保持元素首次出现的顺序。"""
    # raise NotImplementedError("TODO: 提示 dict.fromkeys")
    st = set()
    ret = []
    for item in items:
        if item not in st:
            st.add(item)
            ret.append(item)
    return ret


def group_by(items: Iterable[int], key: Callable[[int], str]) -> dict[str, list[int]]:
    """按 key(item) 分组，返回 {分组名: [元素...]}。"""
    # raise NotImplementedError("TODO: 用 dict.setdefault 或 defaultdict")
    ret = {}
    for item in items:
        cur_key = key(item)
        if cur_key not in ret:
            ret[cur_key] = []

        ret[cur_key].append(item)

    return ret


def safe_deep_copy(grid: list[list[int]]) -> list[list[int]]:
    """返回深层独立的副本：改副本的内层，原数据不受影响。"""
    # raise NotImplementedError("TODO: 提示 copy.deepcopy")
    import copy

    deep_copy = copy.deepcopy(grid)
    return deep_copy


if __name__ == "__main__":
    assert dedupe(["b", "a", "b", "c"]) == ["b", "a", "c"]
    assert group_by([1, 2, 3, 4], lambda n: "even" if n % 2 == 0 else "odd") == {
        "odd": [1, 3],
        "even": [2, 4],
    }

    original = [[1], [2]]
    copy_grid = safe_deep_copy(original)
    copy_grid[0].append(99)
    assert original == [[1], [2]]
    print("练习 03 通过")
