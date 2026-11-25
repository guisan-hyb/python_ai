# 直播挂件数据看板

把 15–17 课的内容串起来：pandas 分析 → matplotlib 图表 → Streamlit 看板 → Agent 问答 → FastAPI 接口。
数据是 `data/metrics.csv` 里的 mock 明细，模型是规则模型，**全程离线**。

## 启动

```bash
cd ~/code/py/py-learn

# 看板
uv run streamlit run projects/live_dashboard/app.py

# 接口（另开一个终端）
uv run uvicorn projects.live_dashboard.api:app --reload
# 文档：http://127.0.0.1:8000/docs
```

## 目录

| 文件 | 职责 |
| --- | --- |
| `data/metrics.csv` | 原始明细：日期、挂件、曝光、点击、订单、GMV |
| `analysis.py` | 纯计算：加载、派生 CTR/CVR、汇总、排名、走势 |
| `tools.py` | 把分析函数包成 Agent 可调用的工具 |
| `mock_llm.py` | 规则模型：按关键词决定调哪个工具 |
| `app.py` | Streamlit 看板 + 聊天 |
| `api.py` | FastAPI：`/health` `/overview` `/gadgets` `/chat` |
| `Dockerfile` | 容器化示例（本机未安装 Docker，未实际构建） |

## 数据口径

- `ctr = click / exposure`
- `cvr = order_cnt / click`
- 整体指标是先把明细求和再算比率，不是对每日比率求平均

## 换成真实模型

```python
from agent.llm import OpenAICompatibleLLM

llm = OpenAICompatibleLLM(base_url="...", model="...", api_key="...")
session = ChatSession(llm, registry=PROJECT_TOOLS)  # 工具层完全不用改
```

真实模型会自己判断该调 `overview` 还是 `top_gadgets`，把 `AnalystLLM` 整个换掉即可。

## 三个可以继续做的练习

1. 加一个 `compare_gadgets(a, b)` 工具，回答「讲解卡比集卡好在哪」。
2. 在 `analysis.py` 加环比/同比，并在看板里显示变化率。
3. 把 CSV 换成 SQLite，用 SQL 重写 `load()`，对比两种读取方式。
