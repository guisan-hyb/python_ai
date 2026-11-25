"""第 12 课：工程化——测试、静态检查、依赖与提交。

会写语法只是入门，能把代码「持续改对」靠的是这一套：
测试跑得快、检查能自动做、依赖能复现、改动可回滚。

本课覆盖：pytest 的写法与运行、ruff 规则、类型检查、uv 工作流、
logging 代替 print、__main__ 入口、打包。

运行：uv run python lessons/12_engineering.py
"""

from __future__ import annotations

import logging
import sys

logger = logging.getLogger("lesson12")


def pure_function(n: int) -> int:
    """可测试的纯函数：同样输入永远同样输出，没有副作用。"""
    if n < 0:
        raise ValueError("n 必须非负")
    return sum(range(n + 1))


def testing() -> None:
    assert pure_function(3) == 6
    assert pure_function(0) == 0
    try:
        pure_function(-1)
    except ValueError:
        print("异常路径也要断言，不能只测顺利情况")
    print("pytest 里就是把这些断言放进 test_ 开头的函数里，见 tests/test_agent.py")
    print("运行：uv run pytest -q；定位单个：uv run pytest tests/test_agent.py -k agent")
    print('参数化：@pytest.mark.parametrize("n,expected", [(3, 6), (0, 0)])')
    print("夹具：@pytest.fixture 提供共享的初始化对象（数据库连接、临时目录）")


def linting() -> None:
    print("ruff 同时负责：格式化（替代 black）+ 检查（替代 flake8/isort 一堆）")
    print("本工程 pyproject.toml 已配好 E/F/I/UP/B/SIM 规则和 100 列宽度")
    print("命令：uv run ruff check . --fix  /  uv run ruff format .")
    print("编辑器里：保存即格式化（.vscode/settings.json 已配置）")


def type_checking() -> None:
    print("运行时不做类型检查，但静态检查能在编码阶段抓到大量 bug")
    print("VSCode 里 Pylance 已经在做（settings 里开了 standard 模式）")
    print("命令行可用：uvx pyright . 或 uvx mypy .")


def workflow() -> None:
    print("uv sync            按 uv.lock 精确还原环境（CI / 换机都用它）")
    print("uv add requests    加运行时依赖，自动改 pyproject + lock")
    print("uv add --dev pytest 加开发依赖")
    print("uv run <cmd>       在工程环境里执行命令，不必手动 activate")
    print("uv lock --upgrade  升级依赖并更新锁文件（先跑测试再提交）")


def logging_instead_of_print() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    logger.info("正式代码用 logging，print 只留在临时调试里")
    logger.info("需要排查时打开 DEBUG，不用改代码")
    logging.shutdown()


def entry_point() -> None:
    print(f"模块被直接运行时 __name__ = {__name__!r}")
    print("把入口写成 `if __name__ == '__main__': main()`")
    print("这样文件既能当脚本跑，又能被 import 做测试，两不耽误")
    print(f"命令行参数在 sys.argv 里：{sys.argv}")


def packaging() -> None:
    print("pyproject.toml = 项目元数据 + 依赖 + 工具配置（一个文件搞定）")
    print("打包成 wheel：uv build，产物在 dist/")
    print("发布到内部源前，先确认 license 和包名，别把 .env 打进去")


def main() -> None:
    for section in (
        testing,
        linting,
        type_checking,
        workflow,
        logging_instead_of_print,
        entry_point,
        packaging,
    ):
        print(f"\n== {section.__name__} ==")
        section()


if __name__ == "__main__":
    main()


# ===== 练习 =====
# 1. 给 pure_function 写 3 个参数化测试，包含负数抛异常的分支。
# 2. 故意写一行超过 100 列和一处未使用导入，跑 ruff 看它怎么报，再改回来。
# 3. 用 uv add --dev pytest-cov 装覆盖率工具，跑 --cov=agent 看报告。
