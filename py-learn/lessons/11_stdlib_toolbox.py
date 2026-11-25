"""第 11 课：标准库工具箱。

C++ 的标准库偏「数据结构 + 算法」；Python 的标准库偏「日常任务」：
路径、JSON、正则、时间、命令行、日志、计数，全都自带。

本课覆盖：pathlib、json、re、datetime、argparse、
collections（Counter/defaultdict/deque）、functools、logging。

运行：uv run python lessons/11_stdlib_toolbox.py
"""

from __future__ import annotations

import argparse
import json
import logging
import re
from collections import Counter, defaultdict, deque
from datetime import datetime, timedelta
from functools import cache, partial
from pathlib import Path

logger = logging.getLogger("lesson11")


def paths() -> None:
    root = Path(__file__).resolve().parent.parent
    print(f"工程根目录 {root.name}，lessons 下 py 文件 {len(list(root.glob('lessons/*.py')))} 个")
    print(f"路径分段：{root.parts[-2:]}")
    print(f"换后缀：{Path('report.csv').with_suffix('.md').name}")
    print(f"用 / 拼路径（跨平台，不用手写分隔符）：{root / 'lessons'}")


def jsons() -> None:
    payload = {"name": "huoyibo", "tags": ["py", "cpp"], "ok": True}
    text = json.dumps(payload, ensure_ascii=False, indent=2)
    print(text)
    print(f"反序列化得到 {type(json.loads(text)).__name__}，字段 {list(json.loads(text))}")


def regex() -> None:
    log = "2026-11-24 ERROR db timeout; 2026-11-24 INFO retry ok"
    dates = re.findall(r"\d{4}-\d{2}-\d{2}", log)
    print(f"findall 日期：{dates}")

    pattern = re.compile(r"(?P<level>ERROR|INFO)\s+(?P<msg>.+?)(?:;|$)")
    for match in pattern.finditer(log):
        print(f"  命名分组 level={match['level']} msg={match['msg']}")

    masked = re.sub(r"\d{4}", "****", "1234-5678")
    print(f"sub 打码：{masked}")


def dates() -> None:
    now = datetime.now()
    print(f"现在：{now:%Y-%m-%d %H:%M:%S}")
    print(f"三天后：{(now + timedelta(days=3)):%Y-%m-%d}")
    print(f"ISO 格式：{now.isoformat(timespec='seconds')}")


def cli() -> None:
    parser = argparse.ArgumentParser(prog="demo")
    parser.add_argument("path")
    parser.add_argument("--top", type=int, default=10)
    args, unknown = parser.parse_known_args(["data.csv", "--top", "3", "--unknown"])
    print(f"path={args.path} top={args.top} 未识别={unknown}")
    print("真实脚本里：args = parser.parse_args()。C++ 用 getopt，Python 自带这套")


def collections_demo() -> None:
    print(f"Counter 统计：{Counter('banana').most_common(2)}")

    groups: dict[str, list[int]] = defaultdict(list)
    for value in (1, 2, 3, 4):
        groups["even" if value % 2 == 0 else "odd"].append(value)
    print(f"defaultdict 免去判空：{dict(groups)}")

    queue = deque([1, 2], maxlen=3)
    queue.append(3)
    print(f"deque 固定长度队列：{list(queue)}")


def functools_demo() -> None:
    @cache
    def fib(n: int) -> int:
        return n if n < 2 else fib(n - 1) + fib(n - 2)

    print(f"functools.cache 版 fib(30) = {fib(30)}，缓存统计 {fib.cache_info()}")

    def apply(value: int, factor: int) -> int:
        return value * factor

    double = partial(apply, factor=2)
    print(f"partial 固定参数：double(21) = {double(21)}")


def logging_demo() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
    logger.info("日志比 print 好在：可分级、可开关、能带模块名和行号")
    logger.warning("生产环境把级别调到 WARNING 就能关掉 info")
    logging.shutdown()


def main() -> None:
    for section in (
        paths,
        jsons,
        regex,
        dates,
        cli,
        collections_demo,
        functools_demo,
        logging_demo,
    ):
        print(f"\n== {section.__name__} ==")
        section()


if __name__ == "__main__":
    main()


# ===== 练习 =====
# 1. 统计一个目录下每种扩展名的文件数量（pathlib + Counter）。
# 2. 解析 Nginx 风格日志行，按状态码分组计数（正则命名分组 + defaultdict）。
# 3. 给你的脚本加 argparse 入口，支持 --verbose 控制日志级别。
