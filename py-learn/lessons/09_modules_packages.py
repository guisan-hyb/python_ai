"""第 09 课：模块、包与导入机制。

C++ 用 #include 做文本粘贴 + 链接器去重；Python 是运行时按名字查找模块。
所以「循环导入」在 Python 里是真实存在的问题，而头文件互相 #include 反而常见。

一个模块 = 一个 .py 文件；一个包 = 带 __init__.py 的目录（3.3+ 也支持命名空间包）。

本课覆盖：三种导入写法、__name__ 守卫、sys.path、本工程内的包、
相对导入、循环导入的成因。

运行：uv run python lessons/09_modules_packages.py
"""

from __future__ import annotations

import sys

from agent.tools import calculate


def import_styles() -> None:
    import math
    import math as m
    from math import sqrt

    print(f"整模块导入：pi = {math.pi:.5f}")
    print(f"起别名：floor({3.7}) = {m.floor(3.7)}")
    print(f"只导一个名字：sqrt(16) = {sqrt(16)}")
    public_names = [name for name in dir(math) if not name.startswith("_")]
    print(f"模块本身是一个对象，公开名字 {len(public_names)} 个")


def name_guard() -> None:
    print(f"当前模块的 __name__ = {__name__!r}")
    print("直接运行脚本时是 '__main__'；被 import 时是 'lessons.09_modules_packages'")
    print("这正是 `if __name__ == '__main__':` 能区分「运行」和「被导入」的原因")


def search_path() -> None:
    print(f"sys.path[0] = {sys.path[0]}")
    print("查找顺序：内置模块 -> sys.path 里的目录（当前目录排最前）-> site-packages")
    print("C++ 里没有这个概念，因为链接期就把符号定死了")


def project_package() -> None:
    print(f"从本工程的 agent 包导入：{calculate('2*3')}")
    print("工程根目录有 pyproject.toml，uv sync 时会把它装成可编辑包")
    print("所以无论从哪个目录运行，都能 `from agent.xxx import ...`")


def relative_imports() -> None:
    print("包内部互相引用推荐写相对导入：from .tools import calculate")
    print("绝对导入（from agent.tools import ...）在重构目录时更容易失效")
    print("注意：相对导入只能在包内使用，直接运行 lessons/xx.py 时不可用")


def circular_imports() -> None:
    print("a.py 导入 b.py，b.py 又导入 a.py -> 运行时可能拿到半初始化的模块")
    print("C++ 靠前置声明绕开，Python 的常见解法是：延迟导入（函数内 import）或抽公共模块")


def main() -> None:
    for section in (
        import_styles,
        name_guard,
        search_path,
        project_package,
        relative_imports,
        circular_imports,
    ):
        print(f"\n== {section.__name__} ==")
        section()


if __name__ == "__main__":
    main()


# ===== 练习 =====
# 1. 新建 utils/ 包，写 utils/text.py 提供 slugify()，再从 lessons 里以两种方式导入。
# 2. 制造一次循环导入并观察报错，然后用「函数内延迟导入」修好。
# 3. 解释为什么 `python lessons/09_modules_packages.py` 能找到 agent 包，而
#    `cd /tmp && python ~/code/py/py-learn/lessons/09_modules_packages.py` 可能找不到。
