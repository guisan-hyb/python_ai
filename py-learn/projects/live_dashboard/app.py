"""Streamlit 看板：指标卡片 + 走势图 + 挂件排名 + Agent 问答。

启动：uv run streamlit run projects/live_dashboard/app.py
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import matplotlib  # noqa: E402 - 先插 sys.path，再导入项目内模块

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import streamlit as st  # noqa: E402

from agent.memory import ChatSession  # noqa: E402
from projects.live_dashboard.analysis import by_gadget, daily, load, overview  # noqa: E402
from projects.live_dashboard.mock_llm import AnalystLLM  # noqa: E402
from projects.live_dashboard.tools import PROJECT_TOOLS  # noqa: E402

st.set_page_config(page_title="直播挂件看板", page_icon="📊", layout="wide")


@st.cache_data
def get_frame() -> Any:
    return load()


def render_metrics() -> None:
    data = overview(get_frame())
    columns = st.columns(5)
    columns[0].metric("曝光", f"{data['exposure']:,}")
    columns[1].metric("点击", f"{data['click']:,}")
    columns[2].metric("CTR", f"{data['ctr']:.2%}")
    columns[3].metric("CVR", f"{data['cvr']:.2%}")
    columns[4].metric("GMV", f"{data['gmv']:,.0f}")


def render_chart(gadget: str) -> None:
    frame = daily(get_frame(), gadget=None if gadget == "全部" else gadget)
    fig, ax = plt.subplots(figsize=(7, 3), dpi=110)
    ax.plot([day.strftime("%m-%d") for day in frame["date"]], frame["ctr"], marker="o")
    ax.set_title(f"CTR trend - {gadget}")
    ax.set_ylabel("CTR")
    ax.grid(alpha=0.3)
    st.pyplot(fig)
    plt.close(fig)


def render_table() -> None:
    st.caption("按 CTR 排序的挂件汇总")
    st.dataframe(by_gadget(get_frame(), top=10), hide_index=True, width="stretch")


def render_chat() -> None:
    if "session" not in st.session_state:
        st.session_state.session = ChatSession(AnalystLLM(), registry=PROJECT_TOOLS)
    if "chat" not in st.session_state:
        st.session_state.chat = []

    for role, text in st.session_state.chat:
        with st.chat_message(role):
            st.markdown(text)

    if prompt := st.chat_input("问数据，例如：整体情况怎么样"):
        answer = st.session_state.session.ask(prompt)
        st.session_state.chat.extend([("user", prompt), ("assistant", answer)])
        st.rerun()


def main() -> None:
    st.title("📊 直播挂件数据看板")
    st.caption("Mock 数据 + 规则模型，完全离线，可替换为真实模型")
    gadget = st.sidebar.selectbox("挂件", ["全部", "讲解卡", "抽奖转盘", "集卡"])
    render_metrics()
    left, right = st.columns([3, 2])
    with left:
        render_chart(gadget)
    with right:
        render_table()
    st.divider()
    render_chat()


main()
