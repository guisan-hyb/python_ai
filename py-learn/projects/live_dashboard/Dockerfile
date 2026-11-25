# 注意：本机未安装 Docker，这个文件没有实际构建过，只保证语法与思路正确
FROM python:3.13-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PYTHONUNBUFFERED=1

# 先只装依赖（不带项目本身），利用镜像层缓存
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

COPY README.md ./
COPY agent ./agent
COPY projects ./projects
RUN uv sync --frozen --no-dev

ENV PATH="/app/.venv/bin:$PATH"
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s \
    CMD python -c "import httpx; httpx.get('http://127.0.0.1:8000/health', timeout=2).raise_for_status()"

CMD ["uvicorn", "projects.live_dashboard.api:app", "--host", "0.0.0.0", "--port", "8000"]
