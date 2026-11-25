"""练习 11 参考答案。运行：uv run python solutions/sol11.py"""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path


def word_freq(text: str, top: int) -> list[tuple[str, int]]:
    counts = Counter(word.lower() for word in text.split())
    return counts.most_common(top)


def status_codes(log: str) -> dict[str, int]:
    codes = re.findall(r"\b([1-5]\d{2})\b", log)
    return dict(Counter(codes))


def count_by_suffix(directory: Path) -> Counter[str]:
    return Counter(path.suffix for path in directory.glob("*") if path.is_file())


if __name__ == "__main__":
    assert word_freq("Py py CPP cpp py", 2) == [("py", 3), ("cpp", 2)]

    log = "GET /a 200 12ms\nGET /b 404 5ms\nGET /c 200 8ms"
    assert status_codes(log) == {"200": 2, "404": 1}

    folder = Path(__file__).resolve().parent.parent / "exercises"
    stats = count_by_suffix(folder)
    assert stats[".py"] >= 10, f"期望至少 10 个 py 文件，实际 {stats}"
    print("练习 11 通过")
