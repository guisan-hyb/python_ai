from __future__ import annotations

from fastapi.testclient import TestClient

from projects.live_dashboard.analysis import by_gadget, load, overview
from projects.live_dashboard.api import app


def test_overview_totals() -> None:
    data = overview(load())
    assert data["days"] == 8
    assert data["exposure"] == 174700
    assert data["ctr"] == 0.048


def test_top_gadget_by_ctr() -> None:
    frame = by_gadget(load(), metric="ctr", top=1)
    assert frame.iloc[0]["gadget"] == "讲解卡"


def test_top_gadget_by_cvr() -> None:
    frame = by_gadget(load(), metric="cvr", top=1)
    assert frame.iloc[0]["gadget"] == "抽奖转盘"


def test_api_health_and_chat() -> None:
    client = TestClient(app)
    assert client.get("/health").json() == {"status": "ok"}
    reply = client.post("/chat", json={"message": "整体情况怎么样"}).json()["reply"]
    assert "曝光" in reply
