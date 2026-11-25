"""HTTP 接口层：指标查询 + Agent 问答。

启动：uv run uvicorn projects.live_dashboard.api:app --reload
"""

from __future__ import annotations

from typing import Any

from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

from agent.memory import ChatSession
from projects.live_dashboard.analysis import by_gadget, load, overview
from projects.live_dashboard.mock_llm import AnalystLLM
from projects.live_dashboard.tools import PROJECT_TOOLS

app = FastAPI(title="live-dashboard", version="0.1.0")
FRAME = load()
SESSION = ChatSession(AnalystLLM(), registry=PROJECT_TOOLS)


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=500)


class ChatResponse(BaseModel):
    reply: str


def _records(frame: Any) -> list[dict[str, Any]]:
    """把 numpy 标量转成原生类型，否则 JSON 序列化会失败。"""
    return [
        {key: (value.item() if hasattr(value, "item") else value) for key, value in row.items()}
        for row in frame.to_dict("records")
    ]


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/overview")
def get_overview() -> dict[str, float | int]:
    return overview(FRAME)


@app.get("/gadgets")
def get_gadgets(
    metric: str = Query("ctr", pattern="^(ctr|cvr|gmv|exposure)$"),
    top: int = Query(3, ge=1, le=10),
) -> list[dict[str, Any]]:
    return _records(by_gadget(FRAME, metric=metric, top=top))


@app.post("/chat")
def chat(request: ChatRequest) -> ChatResponse:
    return ChatResponse(reply=SESSION.ask(request.message))
