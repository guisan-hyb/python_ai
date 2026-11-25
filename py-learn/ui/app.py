"""Streamlit 界面：几十行代码就能把 Agent 变成可交互的页面。

启动：uv run streamlit run ui/app.py
"""

from __future__ import annotations

import streamlit as st

from agent.llm import MockLLM
from agent.loop import run_agent

st.set_page_config(page_title="py-learn Agent", page_icon="🤖")
st.title("🤖 py-learn Agent")
st.caption("当前使用 Mock 模型，不联网、不花钱。")
st.caption("试着问「北京天气怎么样」或「帮我计算 12*(3+4)」。")

if "llm" not in st.session_state:
    st.session_state.llm = MockLLM()
if "history" not in st.session_state:
    st.session_state.history = []

for role, text in st.session_state.history:
    with st.chat_message(role):
        st.markdown(text)

if prompt := st.chat_input("输入你的问题"):
    st.session_state.history.append(("user", prompt))
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("思考中…"):
            answer = run_agent(prompt, st.session_state.llm)
        st.markdown(answer)

    st.session_state.history.append(("assistant", answer))
