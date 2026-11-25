# py-learn

给有 C++ 基础的 Python 全栈 + AI Agent 学习工程：18 课讲义、12 组练习（含 5–12 参考答案）、
一个把全栈链路串起来的综合项目。

## 环境要求

| 项目 | 说明 |
| --- | --- |
| 系统 | macOS（本机 arm64，Apple Silicon） |
| Python | 3.13.18，由 `uv` 管理，不依赖系统 Python |
| 包管理 | `uv` 0.13+（替代 pip/venv/conda，一条命令建环境） |
| 编辑器 | VSCode + Python / Pylance / Debugpy / Jupyter / Ruff 扩展 |
| 不需要 | Anaconda（商用授权有坑、体积大）；Docker 仅第 18 课可选 |

## 依赖清单

运行时依赖（`pyproject.toml` 里声明，`uv.lock` 锁定精确版本）：

| 包 | 当前版本 | 用来做什么 | 哪一课用到 |
| --- | --- | --- | --- |
| `fastapi` | 0.165.0 | 写 HTTP 接口，自带 `/docs` 调试页 | 14、18、综合项目 |
| `uvicorn` | 0.54.0 | 跑 FastAPI 的 ASGI 服务器 | 14、18、综合项目 |
| `pydantic` | 2.14.4 | 请求体校验与类型转换 | 14、18、综合项目 |
| `streamlit` | 1.67.0 | 几十行代码做出可交互页面 | 综合项目 |
| `httpx` | 0.28.1 | 同步/异步 HTTP 客户端 | 17、18、接真实模型 |
| `pandas` | 3.1.1 | 表格数据处理与聚合 | 15、16、综合项目 |
| `matplotlib` | 3.11.2 | 画图并保存 PNG | 16、综合项目 |

开发依赖（`uv add --dev`）：

| 包 | 当前版本 | 用途 |
| --- | --- | --- |
| `pytest` | 9.2.0 | 运行 `tests/` 与 `solutions/sol12.py` |
| `ruff` | 0.17.6 | 格式化 + 静态检查，保存即格式化 |
| `ipykernel` / `ipython` | 7.4.0 / 9.19.1 | Jupyter 内核与交互式终端 |

间接依赖里 `numpy`、`pyarrow` 是 pandas/streamlit 带进来的，不用手动管。

## 目录结构

```
py-learn/
├── lessons/            18 课正文 + 课程表 README
├── exercises/          12 组练习（自带断言，跑通即过关）
├── solutions/          练习 05–12 参考答案
├── projects/
│   └── live_dashboard/ 综合项目：看板 + Agent 问答 + API + Dockerfile
├── agent/              LLM 抽象 / 工具注册 / ReAct 循环 / 会话记忆
├── api/、ui/           最小示例（第 13–14 课的配套代码）
├── notebooks/          Jupyter 上手示例
├── tests/              工程测试（含综合项目）
├── pyproject.toml      依赖 + ruff + pytest 配置
└── .vscode/            解释器、调试、任务配置
```

## 快速开始

```bash
cd ~/code/py/py-learn
uv sync                                     # 建 .venv，按 uv.lock 装依赖
uv run python lessons/01_variables_types.py # 跑第一课
uv run pytest -q                            # 工程测试
uv run ruff check .                         # 静态检查
```

VSCode 打开 `~/code/py/py-learn`：先点左下角 `Restricted Mode` 信任文件夹，
再用 `Cmd+Shift+P → Python: Select Interpreter` 选 `./.venv/bin/python`。

## 每天怎么用

| 想做的事 | 命令 |
| --- | --- |
| 跑某一课 | `uv run python lessons/03_containers.py` |
| 做练习 | `uv run python exercises/ex03.py` |
| 对答案 | `uv run python solutions/sol05.py`（01–04 没有收录答案） |
| 交互式试代码 | `uv run ipython` 或打开 `notebooks/*.ipynb` |
| 起示例接口 | `uv run uvicorn api.main:app --reload` → `http://127.0.0.1:8000/docs` |
| 起看板 | `uv run streamlit run projects/live_dashboard/app.py` |
| 起看板接口 | `uv run uvicorn projects.live_dashboard.api:app --reload` |
| 格式化 | `uv run ruff format .` |
| 加依赖 | `uv add 包名`；开发依赖 `uv add --dev 包名` |

不想记命令：`Terminal → Run Task…` 里已经配好上面几项。内置终端是 `Ctrl+``，不是 `Cmd+``。

## 学习路径

1. `lessons/01` – `lessons/12`：语言基础，每课配 `exercises/exNN.py`
2. `lessons/13` – `lessons/14`：Agent 原理（工具调用、记忆、错误恢复）
3. `lessons/15` – `lessons/17`：数据、图表、网络
4. `lessons/18`：部署与交付
5. `projects/live_dashboard`：把上面全部串一遍

课程表和每课要点见 [lessons/README.md](lessons/README.md)。

## 环境重建

换机器或想清空重来时：

```bash
uv python install 3.13      # 若新机器没有 3.13
uv venv --clear .venv       # 重建虚拟环境
uv sync                     # 按 uv.lock 还原依赖
```

`uv.lock` 要入库，这样别人（或 CI）装到的版本和你完全一致。

## 常见问题

| 现象 | 原因与处理 |
| --- | --- |
| `Cmd+`` 打不开终端 | VSCode 在 mac 上也是 `Ctrl+``；`Cmd+`` 是系统切窗口 |
| 补全/调试不可用 | 还在 `Restricted Mode`，点左下角信任文件夹 |
| 图表里中文变方框 | matplotlib 默认无中文字体，见第 16 课三种解法 |
| `uv sync` 很慢 | 首次要下大包（pandas/pyarrow）；可配内网 PyPI 镜像 |
| Dockerfile 没跑过 | 本机未安装 Docker，第 18 课只做静态检查 |
| 想换模型 | 见下一节，只替换 LLM 实现类 |

## 接真实模型

```python
from agent.llm import OpenAICompatibleLLM

llm = OpenAICompatibleLLM(
    base_url="https://api.deepseek.com",  # 或公司网关 / OpenAI
    model="deepseek-chat",
    api_key=os.environ["LLM_API_KEY"],
)
```

把 `api/main.py`、`ui/app.py`、`projects/live_dashboard/` 里的 Mock 实现换掉即可，
工具层、记忆层、接口层都不用改。

## 当前验证状态

- `ruff check .` 通过，`ruff format --check .` 全部已格式化
- `pytest` 通过（含 `tests/test_dashboard.py`）
- `lessons/00` – `lessons/18` 逐个执行通过
- `solutions/sol05` – `sol12` 断言全部通过
- Streamlit 看板返回 200；FastAPI `/health` `/overview` `/gadgets` `/chat` 实测正常
- Docker 未验证（本机无 Docker）
