"""第 07 课：异常与资源管理。

C++ 用 RAII + 析构函数保证释放；Python 用 with 语句 + __exit__ 达到同样目的，
因为 Python 对象的回收时机不确定（引用计数 + GC），不能依赖 __del__。

本课覆盖：try/except/else/finally、自定义异常、异常链、
EAFP、上下文管理器（类实现 + contextlib）。

运行：uv run python lessons/07_exceptions.py
"""

from __future__ import annotations

import time
from collections.abc import Iterator
from contextlib import contextmanager


class InsufficientBalance(Exception):
    """业务异常：继承 Exception 即可，不要继承 BaseException。"""

    def __init__(self, need: float, have: float) -> None:
        super().__init__(f"需要 {need}，只有 {have}")
        self.need = need
        self.have = have


def order_of_blocks() -> None:
    def parse(text: str) -> int:
        try:
            value = int(text)
        except ValueError:
            print("  except：转换失败")
            return 0
        else:
            print("  else：没有异常才执行")
            return value
        finally:
            print("  finally：无论如何都执行（清理资源放这里）")

    print(f"成功的分支：{parse('42')}")
    print(f"失败的分支：{parse('abc')}")


def custom_exception() -> None:
    def withdraw(balance: float, amount: float) -> float:
        if amount > balance:
            raise InsufficientBalance(amount, balance)
        return balance - amount

    try:
        withdraw(100, 250)
    except InsufficientBalance as exc:
        print(f"捕获业务异常：{exc}；结构化字段 need={exc.need} have={exc.have}")


def exception_chaining() -> None:
    try:
        try:
            int("abc")
        except ValueError as exc:
            raise RuntimeError("解析配置失败") from exc
    except RuntimeError as exc:
        print(f"外层：{exc}；原因：{type(exc.__cause__).__name__}")


def eafp_vs_lbyl() -> None:
    data = {"name": "huoyibo"}
    # LBYL: 先检查再操作（C++ 风格）
    if "age" in data:
        print(data["age"])
    # EAFP: 先做，出错再处理（Python 风格，少一次查表，也没有竞态窗口）
    try:
        print(data["age"])
    except KeyError:
        print("EAFP：没有 age 字段，用默认值")


class Timer:
    """上下文管理器：进入时记时间，退出时打印耗时（异常路径也走）。"""

    def __enter__(self) -> Timer:
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type: object, exc: object, tb: object) -> bool:
        print(f"  耗时 {(time.perf_counter() - self.start) * 1000:.3f} ms")
        return False  # 返回 False 表示异常继续向外传播


@contextmanager
def section(title: str) -> Iterator[None]:
    print(f"-- {title} 开始")
    try:
        yield
    finally:
        print(f"-- {title} 结束（哪怕中途抛异常）")


def context_managers() -> None:
    with Timer():
        sum(range(200_000))
    with section("演示"):
        print("  正文")


def main() -> None:
    for step in (order_of_blocks, custom_exception, exception_chaining, eafp_vs_lbyl):
        print(f"\n== {step.__name__} ==")
        step()
    print("\n== context_managers ==")
    context_managers()


if __name__ == "__main__":
    main()


# ===== 练习 =====
# 1. 写 @retry(times=3, delay=0.1) 装饰器：失败重试，全部失败才抛出。
# 2. 写 open_quietly(path) 上下文管理器：文件不存在时不崩，退出时一定关闭。
# 3. 解释 finally 里 return 会掩盖异常，为什么这是坏习惯。
