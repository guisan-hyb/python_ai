"""FastAPI 后端：把 Agent 包成 HTTP 接口，后续 Streamlit / 前端都能调它。"""

from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel, Field

from agent.llm import MockLLM
from agent.loop import run_agent

app = FastAPI(title="py-learn API", version="0.1.0")
llm = MockLLM()


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000, description="用户输入")


class ChatResponse(BaseModel):
    reply: str


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/chat")
def chat(req: ChatRequest) -> ChatResponse:
    return ChatResponse(reply=run_agent(req.message, llm))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("api.main:app", host="127.0.0.1", port=8000, reload=True)
