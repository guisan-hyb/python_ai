# python_ai

Python 学习仓库，分两块内容：

| 目录 | 内容 |
| --- | --- |
| `01_base/` | Python 基础语法练习，按主题分章节（变量与逻辑控制、文件、……） |
| `py-learn/` | 系统的 Python 全栈 + AI Agent 学习工程：18 课讲义、12 组练习与参考答案、综合看板项目、FastAPI 服务与测试 |

## 快速开始

```bash
cd py-learn
uv sync                          # 按 uv.lock 重建环境，不要提交 .venv
uv run python lessons/01_variables_types.py
uv run pytest -q                 # 跑测试
```

## 多机协作约定

同一个仓库在两台机器上开发，各自负责不同目录（本机 `py-learn/`，另一台 `01_base/` 与新增章节），
日常只需「先拉后推」：

```bash
git pull --rebase     # 本仓库已配置 pull.rebase=true
git add -A && git commit -m "..."
git push
```

不同目录的改动由 Git 自动三方合并，一般不会冲突。真正需要留意的只有这几处：

- `py-learn/uv.lock`、`py-learn/pyproject.toml` —— 依赖变更建议只在一台机器上做，另一台 `pull` 后 `uv sync`
- `py-learn/README.md`、本文件 —— 两边同时改同一段才会冲突
- 同一课练习文件 —— 别在两台机器上同时改同一个文件

被 `push` 拒绝时不要强推，先 `git pull --rebase` 再推。

## 提交身份

本仓库使用独立的公开身份，**不要**使用公司邮箱或公司 SSH 配置：

```bash
git config --local user.name  "guisan-hyb"
git config --local user.email "hybsfcbztk@outlook.com"
```

SSH 使用 `~/.ssh/id_ed25519_github`，在 `~/.ssh/config` 中由 `Host github.com` 单独指定。

## 不要提交的内容

`.venv/`、`__pycache__/`、`.pytest_cache/`、`.ruff_cache/`、`.env`、`.vscode/` 均已写入 `.gitignore`，
提交前可用 `git status --porcelain` 确认没有误纳入。
