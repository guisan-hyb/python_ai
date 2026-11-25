"""第 03 课：容器与拷贝。

对照表：
    std::vector<T>   -> list
    std::map<K,V>    -> dict（3.7 起保持插入顺序）
    std::set<T>      -> set
    std::pair / tuple-> tuple（不可变，可哈希）
    std::deque       -> collections.deque（第 11 课）

最容易踩的坑是拷贝：`b = a` 只是别名，嵌套结构还需要 deepcopy。

运行：uv run python lessons/03_containers.py
"""

from __future__ import annotations

import copy


def lists() -> None:
    nums = [3, 1, 2]
    nums.append(4)
    nums.insert(0, 0)
    print(f"增删：{nums}，pop() 取尾 {nums.pop()}，剩下 {nums}")
    nums.sort()
    print(f"排序（原地）：{nums}；sorted 返回新列表：{sorted(nums, reverse=True)}")
    print(f"按条件排序：{sorted(['bb', 'a', 'ccc'], key=len)}")


def dicts() -> None:
    user = {"name": "huoyibo", "role": "dev"}
    user["lang"] = "cpp"  # 直接赋值就是插入
    print(f"插入后：{user}")
    print(f"安全取值 get：{user.get('age', '未填')}")
    print(f"键视图 {list(user)}，值视图 {list(user.values())}")
    print(f"弹出 role：{user.pop('role')}，剩下 {user}")
    print(f"合并：{user | {'level': 3}}")


def sets() -> None:
    a, b = {1, 2, 3}, {3, 4}
    print(f"交 {a & b} 并 {a | b} 差 {a - b} 对称差 {a ^ b}")
    print(f"去重（不保序）：{set([3, 1, 3, 2])}")
    print(f"tuple 可以进 set：{len({(1, 2), (3, 4)})} 个元素")
    print("list 不可哈希，放进 set 会抛 TypeError（因为它是可变的）")


def tuples() -> None:
    point = (3, 4)
    x, y = point  # 解包，C++ 的 std::tie 类似
    print(f"解包 x={x} y={y}")
    single = (1,)  # 单元素必须带逗号，否则是 int
    print(f"单元素元组 {single!r} 类型 {type(single).__name__}")


def shallow_vs_deep() -> None:
    grid = [[1, 2], [3, 4]]
    shallow = grid[:]
    shallow[0].append(99)
    print(f"浅拷贝只复制外层，内层共享：{grid}")

    grid = [[1, 2], [3, 4]]
    deep = copy.deepcopy(grid)
    deep[0].append(99)
    print(f"深拷贝完全独立：{grid}")


def complexity() -> None:
    print("list 尾部 append/pop 是 O(1)，头部 insert(0) 是 O(n)")
    print("dict/set 查找平均 O(1)，list 的 in 是 O(n)")
    print(f"验证：{1 in [1, 2, 3]}（10 万条时差异明显）")


def main() -> None:
    for section in (lists, dicts, sets, tuples, shallow_vs_deep, complexity):
        print(f"\n== {section.__name__} ==")
        section()


if __name__ == "__main__":
    main()


# ===== 练习 =====
# 1. 写 dedupe(items)：去重同时保持首次出现顺序（用 dict 或 set+列表）。
# 2. 写 group_by(records, key_fn) 返回 dict[str, list]。
# 3. 解释为什么 set 里不能放 list，但能放 tuple。
