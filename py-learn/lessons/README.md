# 课程表：C++ 开发者视角的 Python

18 课，每课都是一个能直接运行的脚本，注释里标了对应的 C++ 概念。

| # | 主题 | 对应的 C++ 知识 | 这一课要打破的直觉 |
| --- | --- | --- | --- |
| 01 | 变量、类型与对象 | 变量 / 指针 / 拷贝构造 | 赋值不是拷贝，类型属于对象 |
| 02 | 字符串 | `std::string` | str 不可变，文本与字节要显式转换 |
| 03 | 容器与拷贝 | vector / map / set / pair | 浅拷贝会让嵌套结构共享 |
| 04 | 控制流与推导式 | for / switch / 算法库 | for 是遍历而不是计数 |
| 05 | 函数与参数 | 值传递 / 引用传递 / 模板 | 只有对象引用传递，默认参数只算一次 |
| 06 | 类与数据类 | class / struct / 继承 | 无真 private，鸭子类型，dataclass 省样板 |
| 07 | 异常与资源管理 | RAII / 析构函数 | 用 with 代替析构，异常即正常流程 |
| 08 | 迭代器与生成器 | 迭代器 / 惰性求值 | yield 让「循环」变成可暂停的函数 |
| 09 | 模块与包 | #include / 命名空间 / 链接 | 导入是运行时行为，循环导入是真问题 |
| 10 | 并发与异步 | std::thread / future | GIL 决定 IO 与 CPU 场景选型不同 |
| 11 | 标准库工具箱 | STL + 系统 API | 路径、JSON、正则、日志全都自带 |
| 12 | 工程化 | CMake / 单测 / 静态检查 | 测试与检查是日常，不是额外工作 |
| 13 | Agent 实战一：工具调用与记忆 | 回调 / 插件注册 | 模型只决定调什么，执行永远在本地 |
| 14 | Agent 实战二：错误恢复 | 异常安全 / 重试 | 超时、工具报错、死循环都要兜底 |
| 15 | 数据处理（pandas） | vector + 手写聚合 | 向量化表达，索引与类型由库管 |
| 16 | 数据可视化（matplotlib） | 无标准库对应 | Agg 后端、中文字体是必踩的坑 |
| 17 | 网络请求与抓取（httpx） | libcurl | 超时、连接池、重试是默认要求 |
| 18 | 部署与交付 | CMake / 打包 / 运维 | 本地能跑不等于能上线 |

## 每课怎么用

```bash
uv run python lessons/01_variables_types.py   # 先跑，看输出
```

1. 读文件头的对照说明，先猜输出
2. 运行，对答案
3. 改一个值或一行代码，再跑，验证你的模型
4. 做 `exercises/exNN.py`：补完 TODO 后运行，断言全过会打印「练习 NN 通过」
5. 卡住再看 `solutions/solNN.py`（01–04 无参考答案，已由你独立完成）

## 课程之后：综合项目

`projects/live_dashboard/` 把 15–18 课串起来：CSV → pandas → matplotlib →
Streamlit 看板 → Agent 问答 → FastAPI 接口 → Dockerfile。

```bash
uv run streamlit run projects/live_dashboard/app.py
uv run uvicorn projects.live_dashboard.api:app --reload
```

## 进度自检

```bash
for f in lessons/*.py; do uv run python "$f" > /dev/null && echo "OK $f"; done
```

18 课全部 OK，说明你对每个语法点都至少跑通过一次。
