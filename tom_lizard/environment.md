# Tom Lizard 环境记录

这里记录 Tom 用到的所有软件、环境、包和模型。每装一样东西、删一样东西，都要在这里写清楚：哪天、装了什么、版本、为什么要装、用什么命令装的。

## 一、整体是怎么搭起来的

从下往上一共五层：

1. **Ollama**：电脑上的一个 App，在后台跑模型
2. **模型**：从 Ollama 下载的模型文件，比如 qwen3:8b
3. **conda 环境 `tom_lizard`**：一个独立的 Python 环境，跟电脑上别的项目分开
4. **Python 包**：装在 conda 环境里，我们的代码用它们去跟 Ollama 说话
5. **Tom 网页服务**：用 uvicorn 跑起来的 FastAPI 程序，给浏览器提供聊天页面

你在网页上发一句话，经过的路线是这样的：

```
浏览器网页
  ↓ 把整段对话发到 http://127.0.0.1:8000/api/chat
uvicorn 收到请求，交给 FastAPI
  ↓ FastAPI 用 pydantic 检查格式，调用 agent.py
agent.py 跑 agent 循环
  ↓ ollama 包通过 httpx 把对话发到 http://localhost:11434
Ollama App 用 qwen3:8b 算出回答
  ↑ 原路返回，最后网页把 Tom 的回答显示出来
```

这里有两个服务器，别搞混：8000 端口是我们自己的 Tom 网页服务，11434 端口是 Ollama 的模型服务。

## 二、电脑上的基础软件

这些不属于某个项目，是整台电脑共用的。

| 软件 | 版本 | 装在哪 | 干什么用 | 什么时候装的 |
| --- | --- | --- | --- | --- |
| Ollama | 0.40.0 | `/Applications/Ollama.app` | 在本机下载和运行开源大模型 | 2024-11-19 以前就装了，App 会自己更新。2026-10-02 是 0.35.0，2026-10-09 发现自动更新到了 0.40.0 |
| Miniforge | conda 24.3.0 | `~/miniforge3` | 管理 Python 环境。默认从 conda-forge 下载包 | 以前就装了 |

### Ollama 怎么启动

- 打开 Ollama App 就行，它会在后台跑一个服务，地址是 `http://localhost:11434`
- 检查它有没有在跑：

```
curl localhost:11434/api/version
```

返回 `{"version":"0.40.0"}` 这样的内容就说明在跑。2026-10-02 实际测过。

- 不想开 App 也可以在终端里跑 `ollama serve`，效果一样

## 三、模型

**电脑上所有模型的完整清单在 `ai_projects/my_model_list.md`**，包括大小、实测内存、谁下的、怎么运行和删除。这里只记 Tom 用到的。

| 模型 | 大小 | 下载日期 | 为什么下载 | 用在哪 |
| --- | --- | --- | --- | --- |
| qwen3:8b | 5.2GB | 2026-10-02 | 支持工具调用和思考，官方 tool calling 文档的例子就用它，速度快适合练手 | 第一课起，Tom 网页也用它 |

qwen3:8b 的详细信息，用 `ollama show qwen3:8b` 查的：

- 参数量 8.2B，就是 82 亿个参数。参数越多一般越聪明，但越慢越占内存
- 量化方式 Q4_K_M。量化就是把模型的数字压缩成更少的位数，文件变小、跑得更快，聪明程度损失一点点
- 上下文长度 40960 个 token。token 大概是一个词或半个词，这个数字是模型一次能看到的最大文字量
- 能力：completion 文字生成，tools 工具调用，thinking 思考
- 许可证 Apache 2.0，可以商用

模型相关命令：

```
ollama list              # 看下载了哪些模型
ollama pull qwen3:8b     # 下载模型
ollama show qwen3:8b     # 看模型详细信息
ollama rm 模型名          # 删除模型
```

## 四、怎么启动 Tom

每次要用 Tom，按顺序做：

1. 确认 Ollama 在跑：`curl localhost:11434/api/version` 有返回就行。没有就打开 Ollama App
2. 进环境并启动网页服务：

```
conda activate tom_lizard
cd tom_lizard/app
uvicorn main:app --reload
```

3. 浏览器打开 http://127.0.0.1:8000
4. 用完在终端按 `Ctrl+C` 关掉服务

uvicorn 几个参数的意思，用 `uvicorn --help` 在本机查的：

- `main:app` 意思是去 `main.py` 文件里找一个叫 `app` 的东西来跑
- `--reload` 改了代码自动重启，开发时用。不加的话改了代码要手动重启
- `--host` 默认是 `127.0.0.1`，意思是只有这台电脑自己能访问，别人连不进来。要让同一个 WiFi 下的手机访问，可以改成 `--host 0.0.0.0`，但这样同网络的人都能用，要小心
- `--port` 默认是 `8000`

2026-10-02 实际测过：页面能打开，能聊天，能连续多轮对话。

## 五、conda 环境

### 现有环境

| 环境名 | Python | 建立日期 | 用途 |
| --- | --- | --- | --- |
| tom_lizard | 3.12.14 | 2026-10-02 | Tom 项目专用 |

为什么要单独建环境：每个项目需要的包和版本不一样，混在一起容易互相冲突。单独建一个，坏了也不影响别的项目，删掉重建就行。

### 怎么进入环境

```
conda activate tom_lizard
```

进去以后终端前面会显示 `(tom_lizard)`。用完退出：

```
conda deactivate
```

不进入环境也可以直接用环境跑一个命令：

```
conda run -n tom_lizard python 文件名.py
```

### 从零重建环境

环境的配置写在 `tom_lizard/environment.yml` 里。新电脑或者环境坏了，跑这几条命令：

```
cd tom_lizard
conda env create -f environment.yml
conda activate tom_lizard
ollama pull qwen3:8b
```

实际测过两次，都是建一个测试环境，测完删掉：

- 2026-10-02 第一次，只有 ollama，第一课跑通了
- 2026-10-02 第二次，加了 fastapi 和 uvicorn，网页能打开，对话能用
- 2026-10-02 第三次，加了 numpy，第三课跑出来的结果和原环境一模一样

要先删掉旧环境再重建的话：

```
conda env remove -n tom_lizard
```

### 当初一步步装东西用的命令

都是 2026-10-02，按这个顺序：

```
conda create -y -n tom_lizard python=3.12
conda run -n tom_lizard pip install ollama==0.6.3
conda run -n tom_lizard pip install fastapi==0.142.2 uvicorn==0.54.0
conda run -n tom_lizard pip install numpy==2.5.3
```

第一条建环境并装 Python 3.12。第三条是做网页界面时装的。第四条是第三课从零训练小 Tom 时装的。第二条用 pip 装 ollama 库，因为官方文档就是用 pip 装的。conda-forge 上其实也有，包名叫 `ollama-python`，2026-10-02 查的时候也是 0.6.3，两种装法都行。我们统一用 pip 装 Python 库，conda 只管 Python 本身，这样不容易乱。

## 六、Python 包

### 我们主动装的包

按安装顺序：

| 顺序 | 包 | 版本 | 安装日期 | 干什么用 | 为什么要装 |
| --- | --- | --- | --- | --- | --- |
| 1 | python | 3.12.14 | 2026-10-02 | Python 本身 | 写代码用。选 3.12 是因为够新又稳定，ollama 库要求 3.8 以上 |
| 2 | ollama | 0.6.3 | 2026-10-02 | Ollama 官方的 Python 库 | 用 Python 代码跟本机的 Ollama 说话，发消息、调用工具都靠它。装的时候是 PyPI 上的最新版 |
| 3 | fastapi | 0.142.2 | 2026-10-02 | 写网页后端的框架。规定有哪些网址，每个网址收到请求后干什么 | 给 Tom 做网页界面。比 Gradio 和 Streamlit 装的东西少得多，界面能完全自己控制，也是做正式应用和接活最常用的写法。装的时候是 PyPI 最新版 |
| 4 | uvicorn | 0.54.0 | 2026-10-02 | 网页服务器。真正开着端口等浏览器来连接，收到请求就交给 FastAPI | FastAPI 自己不会开端口，必须有一个服务器来跑它，官方文档用的就是 uvicorn。装的时候是 PyPI 最新版 |
| 5 | numpy | 2.5.3 | 2026-10-02 | 做数学运算，尤其是一大堆数字一起算，比如矩阵乘法 | 第三课从零训练小 Tom，神经网络的计算全靠它。几乎所有 AI 代码最底层都用它，以后肯定还会用。要求 Python 3.12 以上。装的时候是 PyPI 最新版 |

### 跟着自动装进来的包

我们没有直接装这些，是主动装的包需要它们，pip 自动装的。

**ollama 带进来的**，2026-10-02 装 ollama 时：

```
ollama 0.6.3
├── httpx 0.28.1             发 HTTP 请求
│   ├── httpcore 1.0.9       httpx 底层真正收发数据的部分
│   │   └── h11 0.16.0       按 HTTP/1.1 协议格式处理数据
│   ├── anyio 4.15.1         让程序能同时等好几件事，比如同时发几个请求
│   ├── certifi 2026.7.22    一份可信网站证书清单，访问 https 网址时用来验证对方身份
│   └── idna 3.20            处理带非英文字符的网址
└── pydantic 2.13.5          检查和整理数据格式
    ├── pydantic_core 2.46.5     pydantic 的核心部分，用 Rust 写的，所以快
    ├── annotated-types 0.8.0    给类型加限制条件，比如数字必须大于 0
    ├── typing_extensions 4.16.0 让旧版本 Python 也能用新的类型写法
    └── typing-inspection 0.4.4  在程序运行时读取类型信息
```

**fastapi 和 uvicorn 带进来的**，2026-10-02 装它们时。pydantic、anyio、h11 这些之前已经有了，不会重复装，只多了下面 4 个：

```
fastapi 0.142.2
├── starlette 1.7.0              fastapi 底下真正处理网页请求的框架，fastapi 是在它上面加了功能
├── annotated-doc 0.0.5          让代码里能给参数写说明文字，fastapi 生成接口文档时用
├── opentelemetry-api 1.45.0     监控和追踪程序运行情况的标准接口
├── pydantic                     已有，检查网页发来的数据格式
├── typing-extensions            已有
└── typing-inspection            已有

uvicorn 0.54.0
├── click 8.5.0                  做命令行工具用的，uvicorn 命令后面那些参数就是靠它解析的
└── h11                          已有，按 HTTP/1.1 协议格式处理数据
```

**numpy 没有带进来任何依赖包**，2026-10-02 装之前和装之后对比 `pip list`，只多了 numpy 自己。

关于 opentelemetry-api：它只是一套空接口，必须另外装 opentelemetry-sdk 才会真的记录东西。我们没装 SDK，所以它什么都不做。2026-10-02 在本机验证过，开一个追踪记录得到的是 `NonRecordingSpan`，`is_recording()` 是 `False`。

它们在 Tom 里起的作用：

- **httpx**：ollama 库通过它把我们的消息发到 `localhost:11434`，再把模型的回答收回来
- **pydantic**：模型返回的回答被它整理成有固定字段的对象，所以代码里能写 `response.message.tool_calls` 这样的东西。我们把 Python 函数当工具传进去的时候，函数的参数和说明也是靠它转成模型能读懂的格式。网页后端也用它检查浏览器发来的数据，格式不对直接拒绝
- **fastapi**：`app/main.py` 里用它定了三个网址：`/` 返回聊天网页，`/tom_icon.png` 返回头像，`/api/chat` 接收对话并返回 Tom 的回答
- **uvicorn**：启动 Tom 网页服务的命令就是它
- **starlette**：我们没直接用，返回网页文件用的 `FileResponse` 其实就是它提供的
- **numpy**：第三课 `lesson03_tiny_tom.py` 用它存小 Tom 的参数，做矩阵乘法，算训练时的调整方向

### 建环境时自带的包

`python=3.12` 会顺带装上 `pip`、`setuptools`、`wheel` 这几个装包工具，还有 openssl、sqlite 这类 Python 运行需要的底层库。这些是 conda 自动处理的，平时不用管。

完整清单随时可以查：

```
conda list -n tom_lizard
```

查证来源：每个包的说明和依赖关系都是 2026-10-02 从 PyPI 官方页面查的，比如 https://pypi.org/project/ollama/ 和 https://pypi.org/project/fastapi/ 。谁依赖谁是用 `pip show 包名` 在本机确认的，装之前和装之后各存一份 `pip list` 对比出新多了哪些包。FastAPI 的用法查的是官方文档 https://fastapi.tiangolo.com/ ，uvicorn 查的是 https://uvicorn.dev/ 。

## 七、以后装新包的规矩

1. 先上网查这个包是干什么的，最新版本是多少，确认真的需要
2. 用 `pip install 包名==版本号` 装，写死版本号，以后重建出来的环境才会一模一样
3. 把包加进 `environment.yml`
4. 在上面的“我们主动装的包”表里加一行，写清楚日期、版本、干什么用、为什么装。如果顺带装进来了别的包，也要更新依赖关系图
5. 在下面的变更记录里写一条
6. 跑一遍用到这个包的代码，确认能用

## 八、变更记录

| 日期 | 做了什么 | 命令 |
| --- | --- | --- |
| 2026-10-02 | 下载模型 qwen3:8b | `ollama pull qwen3:8b` |
| 2026-10-02 | 建 conda 环境 tom_lizard，Python 3.12.14 | `conda create -y -n tom_lizard python=3.12` |
| 2026-10-02 | 装 ollama 0.6.3，顺带装了 httpx、pydantic 等 10 个依赖包 | `conda run -n tom_lizard pip install ollama==0.6.3` |
| 2026-10-02 | 写了 environment.yml，建测试环境 tom_lizard_verify 验证能跑通，验证完删除 | `conda env create -f environment.yml -n tom_lizard_verify` 和 `conda env remove -n tom_lizard_verify` |
| 2026-10-02 | 为了做网页界面，装 fastapi 0.142.2 和 uvicorn 0.54.0，顺带装了 starlette、annotated-doc、opentelemetry-api、click 共 4 个依赖包 | `conda run -n tom_lizard pip install fastapi==0.142.2 uvicorn==0.54.0` |
| 2026-10-02 | environment.yml 加上 fastapi 和 uvicorn，再建测试环境验证网页能用，验证完删除 | 同上面的重建命令 |
| 2026-10-02 | 演示 Modelfile：用 qwen3:8b 建了一个 tom-demo 模型，测完删除。硬盘占用前后都是 6.7G | `ollama create tom-demo -f Modelfile` 和 `ollama rm tom-demo` |
| 2026-10-02 | 为了第三课装 numpy 2.5.3，没有带进别的包。environment.yml 加上 numpy，重建测试环境验证，验证完删除 | `conda run -n tom_lizard pip install numpy==2.5.3` |
| 2026-10-09 | 发现 Ollama 自动更新到 0.40.0。发现 4 个新模型，是 Claude Fable 5 写博客和验证信息时下的，记在 my_model_list.md | 无 |
| 2026-10-09 | 实测 qwen3:8b 在不同上下文长度下占多少内存，测完用 `ollama stop` 释放 | `ollama ps` 和 `ollama stop qwen3:8b` |
