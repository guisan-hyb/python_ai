"""练习 11：标准库。运行：uv run python exercises/ex11.py"""

from __future__ import annotations

from collections import Counter
from pathlib import Path


def word_freq(text: str, top: int) -> list[tuple[str, int]]:
    """按出现次数从高到低返回前 top 个 (单词, 次数)，单词统一小写。"""
    raise NotImplementedError("TODO: Counter + most_common")


def status_codes(log: str) -> dict[str, int]:
    """从形如 'GET /a 200 12ms' 的行里统计状态码出现次数（提示：re 模块）。"""
    raise NotImplementedError("TODO: 正则 + Counter")


def count_by_suffix(directory: Path) -> Counter[str]:
    """统计目录下（不递归）每个文件扩展名的数量。"""
    raise NotImplementedError("TODO: Path.glob + Counter")


if __name__ == "__main__":
    text = "Py py CPP cpp py"
    assert word_freq(text, 2) == [("py", 3), ("cpp", 2)]

    log = "GET /a 200 12ms\nGET /b 404 5ms\nGET /c 200 8ms"
    assert status_codes(log) == {"200": 2, "404": 1}

    here = Path(__file__).resolve().parent
    stats = count_by_suffix(here)
    assert stats[".py"] >= 10, f"期望至少 10 个 py 文件，实际 {stats}"

    print("练习 11 通过")
