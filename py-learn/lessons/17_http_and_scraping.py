"""第 17 课：网络请求与抓取（httpx）。

C++ 里做 HTTP 要拉 libcurl 并手写回调；Python 的 httpx 同步/异步同一套 API，
而且默认带连接池、超时、重试这些生产环境必需的东西。

本课不起外网请求：本地起一个 HTTP 服务，用它演示抓取、并发、超时与重试，
所以断网也能跑，结果稳定可复现。

运行：uv run python lessons/17_http_and_scraping.py
"""

from __future__ import annotations

import contextlib
import html.parser
import http.server
import tempfile
import threading
import time
from collections.abc import Iterator
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from pathlib import Path

import httpx

LATENCY = 0.05
PAGES = 6


class TitleParser(html.parser.HTMLParser):
    """标准库自带的 HTML 解析器，取 <title> 不需要装 bs4。"""

    def __init__(self) -> None:
        super().__init__()
        self.title = ""
        self._in_title = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "title":
            self._in_title = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._in_title = False

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title += data.strip()


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args: object) -> None:
        pass  # 关掉访问日志，否则会刷满屏幕


class SlowHandler(QuietHandler):
    """每个请求故意慢 50ms，让串行与并发的差距看得出来。"""

    def do_GET(self) -> None:
        time.sleep(LATENCY)
        super().do_GET()


def make_site(root: Path, pages: int) -> None:
    for index in range(pages):
        html = f"<html><head><title>Page {index}</title></head><body>hello {index}</body></html>"
        (root / f"page{index}.html").write_text(html, encoding="utf-8")


@contextlib.contextmanager
def local_site(pages: int) -> Iterator[str]:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        make_site(root, pages)
        handler = partial(SlowHandler, directory=str(root))
        server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            host, port = server.server_address[:2]
            yield f"http://{host}:{port}"
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=2)


def fetch_title(client: httpx.Client, url: str) -> str:
    response = client.get(url, timeout=2.0)
    response.raise_for_status()
    parser = TitleParser()
    parser.feed(response.text)
    return parser.title


def single_request() -> None:
    with local_site(1) as base, httpx.Client() as client:
        response = client.get(f"{base}/page0.html", timeout=2.0)
        print(f"状态码 {response.status_code}，Content-Type {response.headers['content-type']}")
        print(f"正文长度 {len(response.text)} 字符，标题 {fetch_title(client, str(response.url))}")


def serial_vs_concurrent() -> None:
    with local_site(PAGES) as base, httpx.Client() as client:
        urls = [f"{base}/page{i}.html" for i in range(PAGES)]

        start = time.perf_counter()
        serial = [fetch_title(client, url) for url in urls]
        serial_cost = time.perf_counter() - start

        start = time.perf_counter()
        with ThreadPoolExecutor(max_workers=4) as pool:
            concurrent = list(pool.map(partial(fetch_title, client), urls))
        concurrent_cost = time.perf_counter() - start

    print(f"串行 {serial_cost:.2f}s：{serial}")
    print(f"并发 {concurrent_cost:.2f}s：{concurrent}")
    speedup = serial_cost / concurrent_cost
    print(f"提速约 {speedup:.1f} 倍（每请求人为延迟 {LATENCY * 1000:.0f}ms）")


def retry_and_timeout() -> None:
    with local_site(1) as base, httpx.Client() as client:
        missing = f"{base}/not-exist.html"
        for attempt in range(1, 4):
            try:
                client.get(missing, timeout=1.0).raise_for_status()
            except httpx.HTTPStatusError as exc:
                print(f"  第 {attempt} 次：{exc.response.status_code} {exc.response.reason_phrase}")
        print("4xx 是服务端明确拒绝，重试没用；5xx / 超时才值得重试")

        try:
            client.get(f"{base}/page0.html", timeout=0.001)
        except httpx.TimeoutException:
            print("超时要显式捕获，否则会以通用异常冒到上层")


def crawl_style_notes() -> None:
    print("合规底线：先看 robots.txt 与 ToS，控制速率，别打穿对方服务")
    print("抓取顺序：列表页 -> 详情页 -> 解析 -> 清洗 -> 落库（CSV/DB）")
    print("稳定性：连接池复用、超时必设、指数退避、失败落盘可重放")
    print("解析选择：结构固定用 JSON API；必须解析 HTML 时优先 CSS 选择器（bs4/selectolax）")


def main() -> None:
    for section in (single_request, serial_vs_concurrent, retry_and_timeout, crawl_style_notes):
        print(f"\n== {section.__name__} ==")
        section()


if __name__ == "__main__":
    main()


# ===== 练习 =====
# 1. 把并发抓取改成 asyncio + httpx.AsyncClient，对比与线程池的代码复杂度。
# 2. 加一个「最多 3 个并发」的限流器，避免打满对方服务。
# 3. 解析页面里所有 <a href>，用 urllib.parse.urljoin 拼成绝对地址。
