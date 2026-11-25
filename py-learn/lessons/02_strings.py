"""第 02 课：字符串。

C++ 的 std::string 是「可变的字节数组 + 编码约定」。
Python 的 str 是「不可变的 Unicode 码点序列」；字节单独用 bytes 表示。

这个区别决定了两件事：
1. 任何「修改」字符串的操作都返回新串（和 Java 类似）。
2. 文本与字节之间必须显式 encode/decode，乱码问题都出在这一步。

运行：uv run python lessons/02_strings.py
"""

from __future__ import annotations


def immutability() -> None:
    s = "hello"
    try:
        s[0] = "H"  # type: ignore[index]
    except TypeError as exc:
        print(f"不可变：{type(exc).__name__}: {exc}")
    print(f"只能生成新串：{s.upper()} / {s.replace('l', 'L')}")


def slicing() -> None:
    s = "python"
    print(f"前三个 {s[:3]}，后三个 {s[-3:]}，每隔一个 {s[::2]}，反转 {s[::-1]}")
    print(f"切片越界不报错：{s[2:100]!r}")


def f_strings() -> None:
    name, score = "huoyibo", 92.567
    print(f"{name} 得分 {score:.2f}")
    print(f"右对齐 10 位：【{name:>10}】 左对齐：【{name:<10}】")
    print(f"千分位 {1234567:,}，百分比 {0.8715:.1%}，十六进制 {255:#x}")
    print(f"调试写法 {score=}")  # 3.8+ 自带名字和值


def methods() -> None:
    raw = "  Id,Name,Score\n1,huoyibo,92 \n"
    for line in raw.strip().splitlines():
        cells = [cell.strip() for cell in line.split(",")]
        print(cells)
    print(f"startswith / endswith：{'report.csv'.endswith('.csv')}")
    print(f"join 比循环 + 快：{'-'.join(['a', 'b', 'c'])}")


def text_vs_bytes() -> None:
    text = "中文"
    data = text.encode("utf-8")
    print(f"str 长度 {len(text)}（字符数），bytes 长度 {len(data)}（字节数）")
    print(f"bytes 字面量 {data!r}，解码回来 {data.decode('utf-8')!r}")
    print(f"错误处理示例：{b'\\xe4\\xb8'.decode('utf-8', errors='replace')!r}")


def raw_and_multiline() -> None:
    pattern = r"^\d{4}-\d{2}-\d{2}$"  # r 前缀：反斜杠不转义
    print(f"原始串 {pattern}")
    poem = """第一行
第二行"""
    print(poem)
    print(f"多行串行数 {len(poem.splitlines())}")


def main() -> None:
    for section in (immutability, slicing, f_strings, methods, text_vs_bytes, raw_and_multiline):
        print(f"\n== {section.__name__} ==")
        section()


if __name__ == "__main__":
    main()


# ===== 练习 =====
# 1. 写 normalize(name)：去空格、全小写、把连续空白压成一个下划线。
# 2. 统计一段文本里每个字符出现次数（用 dict，不要用 Counter）。
# 3. 把一个 GBK 编码的字节串正确转成 str，注意 errors 参数的作用。
