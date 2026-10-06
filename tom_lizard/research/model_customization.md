# 资料：怎么改造现成的模型

2026-10-02 查的。以后要深入做的时候从这里接着往下查。

这里的信息有日期限制。软件更新很快，真正动手之前要重新上网核对一遍版本和支持情况。

## 总览：五个层次

| 层次 | 做法 | 动不动模型本身 | 难度 | 这台电脑能不能做 | 状态 |
| --- | --- | --- | --- | --- | --- |
| 1 | 提示词，system prompt | 不动 | 最简单 | 能 | Tom 在用 |
| 2 | Ollama Modelfile | 不动，外面包一层 | 简单 | 能 | 实际测过 |
| 3 | 外面加系统：工具、记忆、查资料 | 不动 | 中等 | 能 | 路线图第 3 到 5 步 |
| 4 | 微调，LoRA | 动 | 难 | 能训练，装回 Ollama 未确认 | 只查了资料，没试 |
| 5 | 从头训练 | 全新 | 极难 | 不能 | 不考虑 |

## 第 2 层：Ollama Modelfile

### 指令

来源 https://docs.ollama.com/modelfile ，2026-10-02 查的官方文档：

| 指令 | 干什么 |
| --- | --- |
| `FROM` | 必须有。基于哪个模型 |
| `PARAMETER` | 改运行参数，比如 temperature、上下文长度 num_ctx |
| `TEMPLATE` | 发给模型的完整提示词模板 |
| `SYSTEM` | 写死 system prompt |
| `MESSAGE` | 预先放几条对话记录，可以用来给模型看示范 |
| `LICENSE` | 许可证 |
| `REQUIRES` | 需要的最低 Ollama 版本 |
| `CAPABILITY` | 给 GGUF 或 MLX 模型加能力标记 |
| `ADAPTER` | 叠加 LoRA adapter。**官方现在的文档页面里没有写这个指令**，见下面第 4 层 |

官方例子：

```
FROM llama3.2
PARAMETER temperature 1
PARAMETER num_ctx 4096
SYSTEM You are Mario from super mario bros, acting as an assistant.
```

命令：

```
ollama create 新模型名 -f ./Modelfile    # 创建
ollama run 新模型名                       # 运行
ollama show 新模型名 --parameters         # 看参数
ollama show 新模型名 --system             # 看 system prompt
ollama rm 新模型名                        # 删除
```

### 2026-10-02 实际测试

```
FROM qwen3:8b
PARAMETER temperature 0.3
SYSTEM 你是 Tom，一只友好的绿色小蜥蜴。你永远用中文回答，每次回答的最后都加上一个 🦎。
```

- 问 who are you，原版回答 I am Qwen, a large language model developed by Alibaba Cloud.
- tom-demo 回答 我是 Tom，一只友好的绿色小蜥蜴。🦎
- 创建前后 `~/.ollama/models` 都是 6.7G。新模型共用原模型的权重文件，几乎不占额外空间
- `ollama show tom-demo --parameters` 看到 temperature 从默认的 0.6 变成了 0.3，其他参数 top_k 20、top_p 0.95 等继承自原模型
- 测完删了

踩过的坑：在没有交互终端的环境里，`ollama run 模型名 "问题"` 会卡住不退出。改用 HTTP 接口就没问题：

```
curl -s localhost:11434/api/chat -d '{"model":"qwen3:8b","think":false,"stream":false,"messages":[{"role":"user","content":"who are you?"}]}'
```

### 什么时候用第 2 层而不是第 1 层

- 第 1 层的提示词写在我们自己的代码里，只有 Tom 的程序会带上
- 第 2 层写进模型配置，任何程序调用这个模型都会带上，比如在终端里 `ollama run`，或者以后接别的软件
- Tom 目前只有自己的程序在用，第 1 层就够了

## 第 4 层：微调

### 基本概念

- **微调**：拿自己准备的数据继续训练模型，真正改动模型内部的数字
- **LoRA**：原模型不动，另外训练一小块附加参数叫 adapter，用的时候叠在原模型上。要训练的东西少很多，普通电脑也能做
- **QLoRA**：原模型先量化压缩再做 LoRA，更省内存
- **适合教什么**：说话风格、固定输出格式、某种特定任务的做法
- **不适合教什么**：新知识。想让模型知道新东西，第 3 层给它查资料更靠谱，也容易更新

### Mac 上的工具：mlx-lm

来源 https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/LORA.md ，苹果 ml-explore 团队的官方仓库，2026-10-02 查的。

安装：

```
pip install "mlx-lm[train]"
```

训练：

```
mlx_lm.lora --model <模型路径> --train --data <数据文件夹> --iters 600
```

合并 adapter 和原模型：`mlx_lm.fuse`

训练数据格式是 JSONL，就是一行一个 JSON，每条例子必须在一行里。支持四种结构：

- chat：对话格式，带 role 的消息列表
- tools：带工具调用的对话
- completions：prompt 加 completion 一问一答
- text：只有一段 text

文档里列的支持的模型结构：Mistral、Llama、Phi2、Mixtral、Qwen2、Gemma、OLMo、MiniCPM、InternLM2。**这个列表可能没更新**，qwen3 支不支持要动手前再查。

32GB 内存的省内存办法，文档原话的意思：

- batch size 调到 1 或 2
- 只微调 4 到 8 层
- 开 gradient checkpointing
- 长的例子切成短的

文档里的参考速度：M1 Max 32GB 大约每秒 250 个 token。

导出 GGUF 格式：文档说只支持 Mistral、Mixtral、Llama 风格的模型，而且要 fp16 精度。

### 没确认的问题：训练完怎么放回 Ollama

- Ollama 官方现在的 Modelfile 文档里找不到 `ADAPTER` 的说明。2026-10-02 查了 https://docs.ollama.com/modelfile 和 https://docs.ollama.com/import 都没有
- 非官方镜像的旧版文档 https://ollama.readthedocs.io/en/modelfile/ 写着：`ADAPTER` 用来叠加 LoRA adapter，路径可以是绝对路径或者相对 Modelfile 的路径，safetensors 格式的 adapter 只支持 Llama、Mistral、Gemma，没有 Qwen
- Ollama 0.40.0-rc0 的发布说明里提到 Apple Silicon 上默认用 MLX 跑模型，以后 MLX 训练出来的东西可能更容易接进来。这只是预发布版，没确认
- 有第三方文章讲怎么把 LoRA adapter 打包成一个文件给 Ollama 用，没细看：https://www.jocheojeda.com/2026/08/22/one-file-model-ollama-lmstudio/

### 以后真要做的时候，按这个顺序验证

1. 重新查 Ollama 最新文档，看 ADAPTER 现在支持哪些模型
2. 重新查 mlx-lm 最新文档，看支不支持当时要用的模型
3. 先用很小的模型和很少的数据试通整条流程：准备数据、训练、合并、导入 Ollama、跑起来
4. 流程通了再换成正式的模型和数据
5. 训练前后用同一批问题对比，确认真的变好了

## 删除模型里的东西

- 让模型真正忘掉某些知识，叫 machine unlearning，现在还是研究课题，没有成熟好用的工具
- 实际做法通常是用提示词或微调让它不说，而不是真的从模型里删掉

这部分没有专门上网查，是一般性的说法。真要做的时候要查最新进展。

## 查证来源汇总

- Ollama Modelfile 官方文档 https://docs.ollama.com/modelfile
- Ollama 导入模型官方文档 https://docs.ollama.com/import
- Ollama 发布记录 https://github.com/ollama/ollama/releases
- mlx-lm LoRA 文档 https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/LORA.md
- Ollama 旧版文档，非官方镜像 https://ollama.readthedocs.io/en/modelfile/
- 第三方文章，没细看 https://www.jocheojeda.com/2026/08/22/one-file-model-ollama-lmstudio/
