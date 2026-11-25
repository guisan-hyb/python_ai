"""练习 02：字符串。运行：uv run python exercises/ex02.py"""

from __future__ import annotations


def normalize(name: str) -> str:
    """去首尾空格、转小写、把中间连续空白压成一个下划线。"""
    # raise NotImplementedError("TODO: strip + lower + 正则或 split/join")
    raw_str = name.strip().lower()
    return "_".join(raw_str.split())


def char_count(text: str) -> dict[str, int]:
    """统计每个字符出现的次数（不要用 collections.Counter）。"""
    # raise NotImplementedError("TODO: 用 dict 累加")
    cnt = {}
    for ch in text:
        if ch not in cnt:
            cnt[ch] = 0
        cnt[ch] += 1
    return cnt


def is_palindrome(text: str) -> bool:
    """忽略大小写和空格判断回文（提示：切片反转）。"""
    # raise NotImplementedError("TODO")
    raw_str = "".join(text.split()).lower()
    rvs_str = raw_str[::-1]
    return raw_str == rvs_str


if __name__ == "__main__":
    assert normalize("  Huo  Yi  Bo ") == "huo_yi_bo"
    assert char_count("aba") == {"a": 2, "b": 1}
    assert is_palindrome("Never odd or even") is True
    assert is_palindrome("python") is False
    print("练习 02 通过")
