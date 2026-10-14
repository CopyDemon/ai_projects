# 我的本地模型清单

这台 MacBook Pro 上用 Ollama 下载的所有模型，都记在这里。

**规矩：每次下载、删除、更新模型，都必须马上更新这个文件。** 不管是谁下的，我自己、Claude Code 还是别的 Claude 会话。

最后更新：2026-10-09，Ollama 0.40.0

## 一、模型总表

内存占用是 2026-10-09 在这台电脑上一个一个加载实测的，用的是 `ollama ps`。所有模型都是 100% 跑在 GPU 上。

| 模型名 | 参数量 | 硬盘 | 内存，默认设置 | 内存，上下文 4096 | 能干什么 | 谁下的，为什么 | 下载日期 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `qwen3:8b` | 8.2B | 5.2GB | 9.91GB | 5.92GB | 对话、工具调用、思考 | Claude Code，给 Tom Lizard 用 | 2026-10-02 |
| `hf.co/unsloth/Qwen3-14B-GGUF:latest` | 14.8B | 9.0GB | 14.59GB | 9.80GB | 对话、工具调用、思考 | Claude Fable 5，写博客和验证信息 | 2026-10-09 |
| `hf.co/bartowski/Qwen2.5-Coder-7B-Instruct-GGUF:latest` | 7.62B | 4.7GB | 6.58GB | 4.74GB | 写代码、工具调用、代码补全 | Claude Fable 5，写博客和验证信息 | 2026-10-09 |
| `hf.co/bartowski/Llama-3.2-3B-Instruct-GGUF:latest` | 3.21B | 2.0GB | 6.02GB | 2.55GB | 对话、工具调用 | Claude Fable 5，写博客和验证信息 | 2026-10-09 |
| `llama3.2:latest` | 3.2B | 2.0GB | 6.02GB | 2.55GB | 对话、工具调用 | 很早以前自己下的 | 大约 2024 年底 |
| `nomic-embed-text:latest` | 137M | 274MB | 0.37GB | | 把文字变成向量，不能对话 | Claude Fable 5，写博客和验证信息 | 2026-10-06 |

合计：模型文件夹一共 22GB。硬盘还剩 296GB，总共 926GB。电脑内存 32GB。

### 每个模型的详细信息

用 `ollama show 模型名` 查的。

| 模型名 | 架构 | 量化 | 最长上下文 | 许可证 |
| --- | --- | --- | --- | --- |
| `qwen3:8b` | qwen3 | Q4_K_M | 40960 | Apache 2.0 |
| `hf.co/unsloth/Qwen3-14B-GGUF:latest` | qwen3 | Q4_K_M | 40960 | 没显示 |
| `hf.co/bartowski/Qwen2.5-Coder-7B-Instruct-GGUF:latest` | qwen2 | Q4_K_M | 32768 | 没显示 |
| `hf.co/bartowski/Llama-3.2-3B-Instruct-GGUF:latest` | llama | Q4_K_M | 131072 | 没显示 |
| `llama3.2:latest` | llama | Q4_K_M | 131072 | Llama 3.2 社区许可 |
| `nomic-embed-text:latest` | nomic-bert | F16 | 2048 | Apache 2.0 |

### 注意

- **两个 Llama 3.2 3B 基本是同一个模型**：`llama3.2:latest` 从 Ollama 官方下的，`hf.co/bartowski/Llama-3.2-3B-Instruct-GGUF` 从 Hugging Face 下的。大小、量化、实测内存都一样，但硬盘上是两份不同的文件，各占 2GB。要省空间可以删一个，删之前确认 Fable 5 那边没在用
- **默认设置很占内存**：Ollama 0.40.0 不指定上下文时，实测都用 32768，所以默认设置那一列比上下文 4096 那一列多很多。比如 Qwen3-14B 默认要 14.59GB。两个大模型同时开着，32GB 内存就紧张了
- **能干什么那一列**是 `ollama show` 里 Capabilities 显示的：completion 是对话，tools 是工具调用，thinking 是思考，insert 是代码补全，embedding 是变成向量

## 二、模型文件在哪

所有模型都在 `~/.ollama/models/` 里，也就是 `/Users/shengpang/.ollama/models/`。

```
~/.ollama/models/
├── blobs/       真正的模型文件，名字是一长串 sha256 编码，看不出是哪个模型
└── manifests/   每个模型的清单，记着它用了 blobs 里的哪些文件
    ├── registry.ollama.ai/library/   从 Ollama 官方下的
    └── hf.co/                        从 Hugging Face 下的
```

**不要直接去 blobs 文件夹里删文件。** 多个模型可能共用同一个文件，手动删会把别的模型弄坏。删模型一律用 `ollama rm`。

查某个模型的权重是 blobs 里的哪个文件：

```
ollama show qwen3:8b --modelfile | grep "^FROM"
```

各模型的权重文件，2026-10-09 查的：

| 模型名 | blobs 里的文件名开头 |
| --- | --- |
| `qwen3:8b` | `sha256-a3de86cd1c13` |
| `hf.co/unsloth/Qwen3-14B-GGUF:latest` | `sha256-5eaa0870bd81` |
| `hf.co/bartowski/Qwen2.5-Coder-7B-Instruct-GGUF:latest` | `sha256-1664fccab734` |
| `hf.co/bartowski/Llama-3.2-3B-Instruct-GGUF:latest` | `sha256-6c1a2b411610` |
| `llama3.2:latest` | `sha256-dde5aa3fc5ff` |
| `nomic-embed-text:latest` | `sha256-970aa74c0a90` |

## 三、常用命令

### 看有哪些模型

```
ollama list
```

SIZE 那一列是硬盘大小。

### 看哪些模型正在运行

```
ollama ps
```

什么都没列出来就是没有模型在跑。各列的意思：

- **SIZE**：实际占的内存
- **PROCESSOR**：`100% GPU` 是全在 GPU 上，`100% CPU` 是全在普通内存里跑，会慢很多，`48%/52% CPU/GPU` 这种是一部分一部分
- **CONTEXT**：上下文长度
- **RUNNER**：用什么引擎跑的，现在都是 llamacpp
- **UNTIL**：什么时候自动关掉

看整个模型文件夹占了多少硬盘：

```
du -sh ~/.ollama/models
```

### 运行模型

在终端里直接聊天，输入 `/bye` 退出：

```
ollama run qwen3:8b
```

从 Hugging Face 下的模型，名字要写全：

```
ollama run hf.co/unsloth/Qwen3-14B-GGUF
```

在代码里用，比如 Tom，是通过 Ollama 的接口，地址 `http://localhost:11434`。用 curl 试：

```
curl -s localhost:11434/api/chat -d '{"model":"qwen3:8b","stream":false,"messages":[{"role":"user","content":"你好"}]}'
```

embedding 模型不能聊天，要用另一个接口：

```
curl -s localhost:11434/api/embed -d '{"model":"nomic-embed-text","input":"你好"}'
```

省内存的运行方法，把上下文调小：在 `ollama run` 里面输入 `/set parameter num_ctx 4096`，或者在接口里加 `"options":{"num_ctx":4096}`。

### 关闭模型

模型用完不会马上释放内存，默认留 5 分钟。想马上释放：

```
ollama stop qwen3:8b
```

关完用 `ollama ps` 确认已经没了。

### 删除模型

```
ollama rm qwen3:8b
```

删之前想清楚有没有项目在用，删完要更新这个文件。2026-10-02 测过：删一个跟别的模型共用文件的模型，Ollama 只删它自己独有的部分，别的模型不受影响。

### 下载模型

从 Ollama 官方下：

```
ollama pull qwen3:8b
```

从 Hugging Face 下，格式是 `hf.co/用户名/仓库名`，后面可以加量化类型。不加的话默认用 Q4_K_M，仓库里没有 Q4_K_M 就自动挑一个：

```
ollama pull hf.co/bartowski/Llama-3.2-3B-Instruct-GGUF
ollama pull hf.co/bartowski/Llama-3.2-3B-Instruct-GGUF:Q8_0
```

### 看模型的详细信息

```
ollama show qwen3:8b                 # 参数量、上下文长度、量化、能力、许可证
ollama show qwen3:8b --parameters    # 运行参数，比如 temperature
ollama show qwen3:8b --modelfile     # 完整配置，包括权重文件路径
```

## 四、下载新模型以后必须做的事

1. 在第一部分的总表里加一行：模型名、参数量、硬盘大小、谁下的、为什么下、下载日期
2. 实测内存：加载一次，用 `ollama ps` 看默认设置和上下文 4096 两种情况各占多少，测完 `ollama stop`
3. 用 `ollama show` 查架构、量化、最长上下文、许可证，填进详细信息表
4. 用 `ollama show 模型名 --modelfile | grep "^FROM"` 查权重文件，填进第二部分的表
5. 更新合计：`du -sh ~/.ollama/models` 和剩余硬盘空间
6. 在下面的变更记录里写一条
7. 改最上面的最后更新日期

删除模型也一样：从表里删掉那一行，更新合计，写变更记录。

## 五、变更记录

| 日期 | 做了什么 | 谁做的 |
| --- | --- | --- |
| 大约 2024 年底 | 下载 llama3.2:latest | 自己 |
| 2026-10-02 | 下载 qwen3:8b，给 Tom Lizard 用 | Claude Code |
| 2026-10-02 | 建了测试模型 tom-demo 演示 Modelfile，测完删了 | Claude Code |
| 2026-10-06 | 下载 nomic-embed-text | Claude Fable 5 |
| 2026-10-09 | 下载 Qwen3-14B、Qwen2.5-Coder-7B、Llama-3.2-3B，都从 Hugging Face | Claude Fable 5 |
| 2026-10-09 | 建立这个清单，每个模型实测了内存 | Claude Code |

## 查证来源

- Ollama 常见问题，关于 ollama ps、上下文长度、模型保留时间 https://docs.ollama.com/faq
- 从 Hugging Face 下载模型 https://huggingface.co/docs/hub/ollama
- 命令列表来自本机 `ollama --help`
