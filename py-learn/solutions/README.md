# 参考答案

对应 `exercises/ex05.py` – `ex12.py`。

```bash
uv run python solutions/sol05.py            # 05–11：脚本自带断言
uv run pytest solutions/sol12.py -v         # 12：本身就是一个 pytest 文件
```

建议顺序：先自己写，断言全过再对答案。答案不是唯一解，重点看思路，
比如 `sol08.py` 的 `chunked` 用生成器而不是 `list` 切片，就是为了保持惰性。

01–04 的参考实现没有收录：那几课你已经独立通过，保留你自己的写法更有价值。
