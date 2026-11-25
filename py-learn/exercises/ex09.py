"""练习 09：模块与导入。运行：uv run python exercises/ex09.py"""

from __future__ import annotations


def load(name: str) -> object | None:
    """按名字导入模块；导入失败返回 None，不要抛异常。

    提示：importlib.import_module + try/except ImportError。
    """
    raise NotImplementedError("TODO: importlib.import_module + try/except ImportError")


def callable_names(module: object) -> list[str]:
    """返回模块里所有公开的可调用对象名（不含下划线开头）。"""
    raise NotImplementedError("TODO: dir() + getattr + callable")


if __name__ == "__main__":
    assert load("math") is not None
    assert load("definitely_not_a_module_xyz") is None

    names = callable_names(load("math"))
    assert "sqrt" in names
    assert not any(n.startswith("_") for n in names)

    print("练习 09 通过")
