"""练习 09 参考答案。运行：uv run python solutions/sol09.py"""

from __future__ import annotations

import importlib


def load(name: str) -> object | None:
    try:
        return importlib.import_module(name)
    except ImportError:
        return None


def callable_names(module: object) -> list[str]:
    return [
        name for name in dir(module) if not name.startswith("_") and callable(getattr(module, name))
    ]


if __name__ == "__main__":
    assert load("math") is not None
    assert load("definitely_not_a_module_xyz") is None

    names = callable_names(load("math"))
    assert "sqrt" in names
    assert not any(name.startswith("_") for name in names)
    print("练习 09 通过")
