"""第 18 课：部署与交付。

本地能跑不等于能上线。上线要回答四个问题：
依赖能不能精确复现、配置从哪来、进程怎么优雅退出、出问题怎么发现。

本课用 projects/live_dashboard 的真实文件演示，不假装跑过容器
（本机没装 Docker，构建步骤只在文件里给出）。

运行：uv run python lessons/18_deploy_and_ship.py
"""

from __future__ import annotations

import importlib.metadata
import os
import signal
import sys
import threading
import tomllib
import warnings
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def package_metadata() -> None:
    version = importlib.metadata.version("py-learn")
    print(f"已安装的包版本：py-learn=={version}")

    with (ROOT / "pyproject.toml").open("rb") as handle:
        config = tomllib.load(handle)
    project = config["project"]
    dev_count = len(config["dependency-groups"]["dev"])
    print(f"pyproject 里的名称 {project['name']}，Python 要求 {project['requires-python']}")
    print(f"运行时依赖 {len(project['dependencies'])} 个，开发依赖 {dev_count} 个")
    print("运行 uv build 会产出 dist/py_learn-<version>-py3-none-any.whl")


@dataclass(frozen=True)
class Settings:
    """配置一律从环境变量来：代码里不写死地址、端口、密钥。"""

    host: str = "127.0.0.1"
    port: int = 8000
    log_level: str = "INFO"

    @classmethod
    def from_env(cls, env: dict[str, str] | None = None) -> Settings:
        source = os.environ if env is None else env
        return cls(
            host=source.get("APP_HOST", "127.0.0.1"),
            port=int(source.get("APP_PORT", "8000")),
            log_level=source.get("LOG_LEVEL", "INFO"),
        )


def configuration() -> None:
    default = Settings.from_env({})
    overridden = Settings.from_env(
        {"APP_HOST": "0.0.0.0", "APP_PORT": "9000", "LOG_LEVEL": "DEBUG"}
    )
    print(f"默认配置 {default}")
    print(f"环境变量覆盖后 {overridden}")
    print("容器里用 docker run -e APP_PORT=9000 ...；本地用 .env + pydantic-settings 也行")


def healthcheck() -> None:
    warnings.simplefilter("ignore")
    from fastapi.testclient import TestClient

    from projects.live_dashboard.api import app

    client = TestClient(app)
    print(f"GET /health -> {client.get('/health').json()}")
    print(f"GET /overview -> keys={list(client.get('/overview').json())}")
    print("健康检查要轻：只探活，不要在里面查库或调外部接口")


def graceful_shutdown() -> None:
    stop = threading.Event()

    def handle(signum: int, _frame: object) -> None:
        print(f"  收到信号 {signum}，开始收尾")
        stop.set()

    previous = signal.signal(signal.SIGTERM, handle)
    try:
        os.kill(os.getpid(), signal.SIGTERM)  # 给自己发一个，演示收到信号后的行为
        stop.wait(timeout=1)
        print(f"  stop_event 已置位：{stop.is_set()}（关闭连接池、flush 日志放这里）")
    finally:
        signal.signal(signal.SIGTERM, previous)


def container_file() -> None:
    dockerfile = ROOT / "projects" / "live_dashboard" / "Dockerfile"
    text = dockerfile.read_text(encoding="utf-8")
    checks = {
        "基础镜像": "FROM python:3.13-slim",
        "依赖锁定": "uv sync --frozen",
        "启动命令": "CMD [",
        "健康检查": "HEALTHCHECK",
    }
    for label, marker in checks.items():
        print(f"  {label:6} {'OK' if marker in text else '缺失'}  ({marker})")
    print(f"文件位置 {dockerfile.relative_to(ROOT)}，共 {len(text.splitlines())} 行")
    print("本机没有 Docker，这段只做静态检查；构建命令是 docker build -t live-dashboard .")


def checklist() -> None:
    print("1. 依赖：uv.lock 入库，部署用 uv sync --frozen，禁止线上 pip install 最新版")
    print("2. 配置：全部走环境变量，密钥不进镜像；.env 已在 .gitignore 里")
    print("3. 启动：uvicorn --host 0.0.0.0，前面套 nginx/网关，不直接暴露")
    print("4. 观测：结构化日志 + /health + 关键指标（QPS、P99、错误率）")
    print("5. 发布：先灰度一台，观察 10 分钟，再全量；回滚方案提前写好")
    print("6. 资源：容器设 CPU/内存上限，Python 进程注意内存峰值（pandas 全量加载很吃内存）")


def pipeline_text() -> None:
    print("CI 最小流水线（GitLab CI 风格）：")
    print("  test:    uv sync --frozen && uv run ruff check . && uv run pytest -q")
    print("  build:   uv build && docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA .")
    print("  deploy:  按 tag 触发，部署前跑一次 /health 冒烟，失败自动回滚上一版本")
    print(f"  当前解释器 {sys.version.split()[0]}，Python 版本要与镜像保持一致")


def main() -> None:
    for section in (
        package_metadata,
        configuration,
        healthcheck,
        graceful_shutdown,
        container_file,
        checklist,
        pipeline_text,
    ):
        print(f"\n== {section.__name__} ==")
        section()


if __name__ == "__main__":
    main()


# ===== 练习 =====
# 1. 给 API 加 /version 接口，返回 pyproject 里的版本号，并写测试。
# 2. 把 Settings 换成 pydantic-settings，支持 .env 文件与类型校验。
# 3. 给 Streamlit 看板加缓存失效策略（TTL），说明为什么不能用默认永久缓存。
