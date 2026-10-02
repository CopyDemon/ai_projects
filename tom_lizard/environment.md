# Tom Lizard 环境记录

这里记录 Tom 用到的所有软件、环境、包和模型。每装一样东西、删一样东西，都要在这里写清楚：哪天、装了什么、版本、为什么要装、用什么命令装的。

## 一、整体是怎么搭起来的

从下往上一共四层：

1. **Ollama**：电脑上的一个 App，在后台跑模型
2. **模型**：从 Ollama 下载的模型文件，比如 qwen3:8b
3. **conda 环境 `tom_lizard`**：一个独立的 Python 环境，跟电脑上别的项目分开
4. **Python 包**：装在 conda 环境里，我们的代码用它们去跟 Ollama 说话

代码运行的时候是这样的：我们的 Python 代码调用 `ollama` 包，`ollama` 包通过 `httpx` 发 HTTP 请求到本机的 `localhost:11434`，Ollama App 收到请求，用模型算出回答，再发回来。

## 二、电脑上的基础软件

这些不属于某个项目，是整台电脑共用的。

| 软件 | 版本 | 装在哪 | 干什么用 | 什么时候装的 |
| --- | --- | --- | --- | --- |
| Ollama | 0.35.0 | `/Applications/Ollama.app` | 在本机下载和运行开源大模型 | 2024-11-19 以前就装了，App 会自己更新 |
| Miniforge | conda 24.3.0 | `~/miniforge3` | 管理 Python 环境。默认从 conda-forge 下载包 | 以前就装了 |

### Ollama 怎么启动

- 打开 Ollama App 就行，它会在后台跑一个服务，地址是 `http://localhost:11434`
- 检查它有没有在跑：

```
curl localhost:11434/api/version
```

返回 `{"version":"0.35.0"}` 这样的内容就说明在跑。2026-10-02 实际测过。

- 不想开 App 也可以在终端里跑 `ollama serve`，效果一样

## 三、模型

| 模型 | 大小 | 下载日期 | 为什么下载 | 用在哪 |
| --- | --- | --- | --- | --- |
| qwen3:8b | 5.2GB | 2026-10-02 | 支持工具调用和思考，官方 tool calling 文档的例子就用它，速度快适合练手 | 第一课起 |
| llama3.2:latest | 2.0GB | 大约 2024 年底 | 以前装的，不是这个项目下的 | Tom 不用，太小，工具调用不稳 |

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

## 四、conda 环境

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

2026-10-02 实际测过：用 environment.yml 建了一个测试环境，第一课跑通了，测完删掉了。

要先删掉旧环境再重建的话：

```
conda env remove -n tom_lizard
```

### 当初第一次建环境用的命令

2026-10-02，按这个顺序：

```
conda create -y -n tom_lizard python=3.12
conda run -n tom_lizard pip install ollama==0.6.3
```

第一条建环境并装 Python 3.12。第二条用 pip 装 ollama 库，因为官方文档就是用 pip 装的。conda-forge 上其实也有，包名叫 `ollama-python`，2026-10-02 查的时候也是 0.6.3，两种装法都行。我们统一用 pip 装 Python 库，conda 只管 Python 本身，这样不容易乱。

## 五、Python 包

### 我们主动装的包

按安装顺序：

| 顺序 | 包 | 版本 | 安装日期 | 干什么用 | 为什么要装 |
| --- | --- | --- | --- | --- | --- |
| 1 | python | 3.12.14 | 2026-10-02 | Python 本身 | 写代码用。选 3.12 是因为够新又稳定，ollama 库要求 3.8 以上 |
| 2 | ollama | 0.6.3 | 2026-10-02 | Ollama 官方的 Python 库 | 用 Python 代码跟本机的 Ollama 说话，发消息、调用工具都靠它。装的时候是 PyPI 上的最新版 |

### 跟着自动装进来的包

我们没有直接装这些，是 ollama 需要它们，pip 自动装的。依赖关系是这样的：

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

它们在 Tom 里起的作用：

- **httpx**：ollama 库通过它把我们的消息发到 `localhost:11434`，再把模型的回答收回来
- **pydantic**：模型返回的回答被它整理成有固定字段的对象，所以代码里能写 `response.message.tool_calls` 这样的东西。我们把 Python 函数当工具传进去的时候，函数的参数和说明也是靠它转成模型能读懂的格式

### 建环境时自带的包

`python=3.12` 会顺带装上 `pip`、`setuptools`、`wheel` 这几个装包工具，还有 openssl、sqlite 这类 Python 运行需要的底层库。这些是 conda 自动处理的，平时不用管。

完整清单随时可以查：

```
conda list -n tom_lizard
```

查证来源：每个包的说明和依赖关系都是 2026-10-02 从 PyPI 官方页面查的，比如 https://pypi.org/project/ollama/ 和 https://pypi.org/project/httpx/ 。谁依赖谁是用 `pip show 包名` 在本机确认的。

## 六、以后装新包的规矩

1. 先上网查这个包是干什么的，最新版本是多少，确认真的需要
2. 用 `pip install 包名==版本号` 装，写死版本号，以后重建出来的环境才会一模一样
3. 把包加进 `environment.yml`
4. 在上面的“我们主动装的包”表里加一行，写清楚日期、版本、干什么用、为什么装。如果顺带装进来了别的包，也要更新依赖关系图
5. 在下面的变更记录里写一条
6. 跑一遍用到这个包的代码，确认能用

## 七、变更记录

| 日期 | 做了什么 | 命令 |
| --- | --- | --- |
| 2026-10-02 | 下载模型 qwen3:8b | `ollama pull qwen3:8b` |
| 2026-10-02 | 建 conda 环境 tom_lizard，Python 3.12.14 | `conda create -y -n tom_lizard python=3.12` |
| 2026-10-02 | 装 ollama 0.6.3，顺带装了 httpx、pydantic 等 10 个依赖包 | `conda run -n tom_lizard pip install ollama==0.6.3` |
| 2026-10-02 | 写了 environment.yml，建测试环境 tom_lizard_verify 验证能跑通，验证完删除 | `conda env create -f environment.yml -n tom_lizard_verify` 和 `conda env remove -n tom_lizard_verify` |
