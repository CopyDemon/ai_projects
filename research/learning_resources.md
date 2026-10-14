# 资料：学 AI 开发的书和课程

## 已经买的

### THE LLM ENGINEER: Building Transformer Language Models with Python and PyTorch

2026-10-09 买的。

#### 书的基本信息

从亚马逊商品页抓的，2026-10-09：

- 作者 Lachlan James
- Kindle 版，ASIN `B0GWSRQSLK`，链接 https://www.amazon.com/dp/B0GWSRQSLK
- 出版日期 2026-04-11，292 页，文件 6.4MB
- Kindle 价 37.99 美元，纸质书标价 49.67 美元
- 商品页没有出版社这一栏，很可能是作者自己出版的
- **没有任何书评和评分**
- 搜索引擎、Google Books、Open Library 都没收录。作者在网上找不到 AI 相关的介绍

第一次查的时候只用了搜索引擎，以为这本书查不到，记成了“网上查不到任何信息”。后来直接抓亚马逊页面才找到，前面的说法是错的。

#### 书的内容

按亚马逊上的介绍，从“预测下一个 token”讲起，一直讲到用 OpenAI 兼容的接口提供服务。搭出来的模型结构跟 Llama 3、Mistral、Gemma 一样，只是规模小。每章都有能跑的代码、常见 bug 和练习。

| 内容 | 这台 MacBook 能不能做 | 依据 |
| --- | --- | --- |
| 从零写 BPE 分词器 | 能 | 纯 Python，不挑硬件 |
| attention、多头 attention、GQA | 能 | PyTorch MPS 实测能用 |
| 完整的 Transformer 块：RMSNorm、SwiGLU、RoPE | 能 | 同上 |
| 训练：AdamW、学习率调度、梯度裁剪 | 能 | 同上 |
| bf16 混合精度 | **能** | 2026-10-09 实测：PyTorch 2.14.1 在 MPS 上 bf16 autocast 和纯 bf16 训练都成功 |
| 多卡分布式训练 DDP | **只能跑通代码，体会不到多卡** | 实测 gloo 后端可用，nccl 不可用。Mac 只有一块 GPU，DDP 本来就是给多张显卡用的 |
| 实验记录 Weights & Biases | 能，但要联网注册账号 | 是云服务，不是本地的 |
| 从零写 LoRA 和 QLoRA | LoRA 能。QLoRA 要看书里怎么写 | 书说是从零实现。如果用了 bitsandbytes 库，它在 macOS 上只有 CPU 版，没有 GPU 加速 |
| DPO 偏好对齐训练 | 能，小模型就行 | 跟普通训练一样 |
| GPTQ、AWQ 量化 | **要看书用的什么库** | AutoAWQ 已经停止维护，官方说 Mac 用 MLX-LM。GPTQModel 有 Mac 支持。书如果用的是只支持 NVIDIA 的库，在 Mac 上跑不了 |
| 导出 GGUF，用 llama.cpp 和 Ollama 跑 | 能 | Ollama 已经在用 |
| vLLM 部署 | **勉强** | 官方说 Mac 只是实验性支持，要自己从源码编译，只能用 CPU。想用 GPU 要装社区做的 vllm-metal 插件 |

结论：大部分章节在 Mac 上能做。DDP、GPTQ 和 AWQ、vLLM 这几章是按 NVIDIA 显卡写的，在 Mac 上可能要换工具或者只能看懂原理。到时候实在要跑，可以临时租云上的 NVIDIA 显卡，按小时付钱。

#### 完整目录

2026-10-09 用户从 Kindle 截图发来的：

| 章 | 主题 | 重点小节 |
| --- | --- | --- |
| 前言、引言 | 为什么写这本书、要准备什么、关于规模的说明 | |
| 1 | 语言模型在干什么 | 预测下一个 token，n-gram 到神经网络，GPT 和 BERT 的历史，1.6 装 Python 和 PyTorch |
| 2 | 字符级语言模型 | 从原始文本做数据集，2.3 简单的 MLP 语言模型，训练循环，loss 和 perplexity，生成文字 |
| 3 | 分词 | BPE 从零实现，GPT-2、GPT-4、Llama 怎么分词，WordPiece 和 SentencePiece，分词器的坑 |
| 4 | embedding 和位置编码 | 正弦位置编码，学习的位置编码，RoPE，ALiBi |
| 5 | 自注意力和多头注意力 | 从零写注意力，因果遮罩，多头，GQA，Flash Attention，KV cache |
| 6 | Transformer 块和完整模型 | pre-norm 和 post-norm，RMSNorm，SwiGLU，残差连接，算参数量 |
| 7 | 训练流程 | 准备和清洗数据，去重，打包序列，AdamW，余弦学习率，梯度裁剪，Weights & Biases，完整训练一个小模型 |
| 8 | 扩大训练规模 | 混合精度 fp16 和 bf16，梯度累积，DDP，断点续训，评估，scaling laws |
| 9 | 解码和推理 | 贪心，temperature，top-k，top-p，重复惩罚，KV cache，批量推理，投机解码，结构化输出 |
| 10 | 监督微调和高效微调 | 指令数据集，全量微调，LoRA 从零实现，QLoRA，怎么选 rank 和 alpha |
| 11 | 对齐和偏好优化 | RLHF 全貌，奖励模型，PPO 的问题，DPO 从零实现，偏好数据集，Constitutional AI 和 RLAIF |
| 12 | 量化和高效推理 | INT8 和 INT4，GPTQ，AWQ，GGUF 和 llama.cpp，质量和速度的取舍 |
| 13 | 部署 | vLLM，PagedAttention，用 Ollama 本地部署，延迟和吞吐，OpenAI 兼容接口，RAG，监控 |
| 14 | 接下来学什么 | MoE，多模态，读 GPT-2、Llama 3、Mistral 源码，把 Llama 3 的权重装进自己从零写的模型 |
| 附录 A | 硬件指南 | 每章要多少 GPU 内存，GPU 档次，只用 CPU 怎么办，云 GPU |
| 附录 B、C | PyTorch 速查，数学符号速查 | |

除了第 1 章和第 14 章，每章最后都有“常见 bug”和“练习”两节。

#### 从目录看出来的

好的地方：

- 顺序很合理，一层一层往上搭，前面学的后面都用得上
- 内容是现在主流模型真正在用的东西，不是过时的老结构
- 每章有常见 bug 和练习，适合边学边动手
- 附录 A 有每章的 GPU 内存需求，可以直接拿来对照这台 Mac
- 14.4 把真实的 Llama 3 权重装进自己写的模型，能检验前面写得对不对

要留意的地方：

- **太密了**：292 页塞了 14 章加 3 个附录，平均一章 20 页左右，第 7 章有 12 节。Raschka 的书 368 页，内容范围比这本窄，只讲到微调。所以这本每个知识点可能只讲一两页，讲不深
- **用的例子是 2024 年的**：书 2026 年 4 月出版，但 1.4 节说的“现在的大模型”是 GPT-4o 和 Llama 3，这两个都是 2024 年发布的。Llama 4 在书出版前就已经出了。说明内容可能是 2024 年左右的知识写的，部分工具和说法可能过时
- 每章结构一模一样，可能是作者认真设计的，也可能是用 AI 批量生成的。光看目录分不出来，要看正文

结论：目录本身没问题，覆盖面很好。质量要看正文讲得深不深、代码能不能跑。

#### 怎么在退款期内验货

10% 大约是前 29 页，正好能读到前言、引言、第 1 章和第 2 章开头，包括 1.6 装环境和 2.3 第一段模型代码。把这两节的代码拿来实际跑，最能看出书的质量。

#### 试读验货结果

2026-10-09 用户发来 Kindle 试读部分的截图：前言、引言、第 1 章全部、第 2 章开头。书里能核对的代码和数字都实际跑过或者查过了，用的临时环境测完已删。

**对的地方：**

- 文字清楚好懂，结构很好，概念讲得准
- “The quick brown fox” 在 GPT-4 分词器里是 `[791, 4062, 14198, 39935]`，用 tiktoken 实测完全一致。词表大约 10 万，实测 100277，也对
- GPT-1、GPT-2、GPT-3、BERT、注意力机制这些历史讲得都对
- 第 2 章的数据集代码和 CharMLP 模型代码，看起来没问题
- 1.6 节说 Apple Silicon 可以用 MPS，环境检查脚本也考虑了 MPS

**错的地方：**

1. **第 1 章第一段代码印出来的结果是错的，而且解释也跟着错了。** 书上说 “the” 后面接 cat 和 mat 的概率都是 0.496，“因为它们在文中出现次数一样”。实际文本里 the 后面是 cat 3 次、mat 1 次。实际运行结果是 cat 0.741，mat 0.249。书上印的结果还少了 “the” 这一项。说明这段输出不是真的跑出来的
2. **算错了一千倍。** 书上说 50,000 的三次方是 1250 亿，实际是 125 万亿
3. **1.6 节的安装命令在 Mac 上直接失败。** 用 CUDA 12.1 的 pip 命令在这台 Mac 上实测报错 “No matching distribution found for torch”。conda 那条命令用的是 pytorch 官方 conda 频道，PyTorch 官方 2024 年就宣布 2.5 以后不再往那里发布了
4. **配套代码仓库找不到。** 书里说仓库地址写在前言里，但前言里没有。GitHub 上搜不到这本书的仓库
5. **一个函数的参数名起错了。** `sample_next_token(model_probs, temperature)` 叫 probs，但代码里是把它当 logits 用的，先除以 temperature 再 softmax。如果真传概率进去，结果就是错的。对新手很容易造成误解

**其他发现：**

- 前言自己写着：读过 Raschka 的书、想继续往下学的人，这本书正好接着讲。也就是说作者自己把它定位成 Raschka 那本的后续
- 书里说索引是用 LLM 帮忙生成的
- 1.4 节的模型表里有 Gemma 3 和 DeepSeek R1，都是 2025 年初发布的，但没有 2025 年 4 月发布的 Llama 4 和 Qwen3。所以内容的知识大概停在 2025 年 3 月左右，比出版早一年。之前根据目录说是 2024 年，看了正文要更正为 2025 年初

**结论：**

文字写得好，但前 10% 就有 4 到 5 处能验证的错误，而且是“印出来的结果不是跑出来的”这种错。对新手最危险：分不清是书错了还是自己错了，会浪费大量时间。建议先读 Raschka 的书，它有大量读者验证过，代码免费公开。这本以后读完 Raschka 再考虑，作者自己也是这么定位的。

#### 读的时候注意

- 没有书评，质量不知道。每章代码都要实际跑通。跑不通或者跟官方文档对不上，就对照 Raschka 的书和 nanoGPT
- 书是 2026 年 4 月出的，里面用到的库可能已经更新或者停止维护，比如 AutoAWQ。照着做之前先查一下库现在的状态

## 学习路线

2026-10-09 记的。Gemini 推荐的顺序是：

1. THE LLM ENGINEER，Lachlan James，从零搭模型
2. LLM Engineer's Handbook，Iusztin 和 Labonne，把模型做成生产系统
3. AI Engineering，Chip Huyen，用现成模型做应用。用户说的是 “ai engineer”，按书名推测是这本，待确认

### 第二本：LLM Engineer's Handbook

- 作者 Paul Iusztin、Maxime Labonne，Packt 出版，2024-10-22，第一版。没找到第二版
- 讲的是怎么把大模型做成一个完整的生产系统：数据管道、RAG、微调、偏好对齐、评估、推理优化、部署、LLMOps
- 配套代码 https://github.com/PacktPublishing/LLM-Engineers-Handbook
- **要用很多云服务**，代码仓库里写的：OpenAI API、Hugging Face、Comet ML 和 Opik、AWS SageMaker、MongoDB、Qdrant、ZenML。仓库说用默认设置跑一遍整个项目**大约 25 美元**，大部分花在 AWS SageMaker 上训练和推理
- 本地要 Python 3.11、Poetry、Docker。仓库说 macOS 能跑，要加一个环境变量
- 2024 年出的，这个领域变化快，里面的一些工具可能已经过时
- 书评说信息很多，但讲“怎么做”多，讲“为什么这么做”少

### 第三本：AI Engineering

- 作者 Chip Huyen，O'Reilly 出版，2025 年，532 页
- 作者在 Stanford 教过机器学习系统设计，在 NVIDIA 工作过
- 讲的是用现成的大模型做应用：评估和选模型、提示词、RAG、什么时候该微调、数据、推理优化、整个应用的架构
- 作者网站说它是发布以来 O'Reilly 上读的人最多的书
- 配套资料 https://github.com/chiphuyen/aie-book

### 对这个顺序的看法

- Gemini 的顺序是从底层往上学，原理最扎实，但离赚钱最远
- 按赚钱原则，第三本最接近现在企业花钱请人做的事，也最贴近 Tom 这条线。建议把它提前，或者跟第一本同时读
- 第二本要花钱用云服务，跟“尽量本地跑”的规矩冲突。读到时要先决定：花钱照着做，还是改成用 Ollama 本地跑。改的话工作量不小

### 2026-10-09 定下来的第一本书

**第一本读 Raschka 的《Build a Large Language Model (From Scratch)》。** 《AI Engineering》同时当闲书看。

理由：

- 用户是新手，想从底层学，要动手写代码。Raschka 这本只要求会 Python，从头带着写代码
- 代码仓库在 GitHub 上有 10 万多个星，读者非常多，错误早就被挑得差不多了。跟 LLM ENGINEER 那本正好相反
- 有 17 小时多的配套视频，还有每章约 30 道练习题的 PDF
- 仓库里的附加内容有从零实现 Qwen3、Llama 3.2、Gemma 3。Tom 用的就是 qwen3，读完能把书和 Tom 连起来
- 代码能在普通笔记本上跑，Mac 的 MPS 也支持。这台 Mac 已经实测过 PyTorch 训练小型 GPT
- 读完以后可以接着读作者的新书《Build a Reasoning Model (From Scratch)》，或者回头看 LLM ENGINEER 学 RoPE、LoRA、DPO

《AI Engineering》书里没有代码也没有数学公式，适合通勤、睡前看。它讲的是怎么用现成模型做应用，最接近赚钱，可以帮着决定 Tom 往哪做。完全没有机器学习基础的话，有些章节会觉得快，可以跳过。

### Raschka 这本书到底教什么

2026-10-09 从代码仓库 README 查的：

| 章 | 内容 | 有没有代码 |
| --- | --- | --- |
| 1 | 理解大语言模型 | 没有 |
| 2 | 处理文本数据：分词、BPE、数据加载 | 有 |
| 3 | 写注意力机制 | 有 |
| 4 | 从零实现一个 GPT 模型 | 有 |
| 5 | 在没标注的文本上预训练，加载 OpenAI 公开的 GPT-2 权重 | 有 |
| 6 | 微调做文本分类，比如垃圾邮件识别 | 有 |
| 7 | 微调让模型听指令，用 Ollama 给模型的回答打分 | 有 |
| 附录 A | PyTorch 入门 | 有 |
| 附录 D | 训练循环的改进：学习率预热、余弦衰减、梯度裁剪 | 有 |
| 附录 E | LoRA 高效微调 | 有 |

代码仓库里的免费附加内容还有：从零写 BPE，KV cache，GQA，MoE，从零实现 Llama 3.2、Qwen3、Qwen3.5、Gemma 3、Gemma 4，DPO 偏好对齐，给模型做聊天界面，CPU 和 MPS 结果的差异。LLM ENGINEER 那本书里的进阶内容，这里大部分都有，还是免费的。

对照用户关心的几点：

| 想学的 | 这本书教不教 |
| --- | --- |
| 什么是 AI | 只讲大语言模型，第 1 章。不讲整个 AI 领域的全貌 |
| 怎么下载模型 | 教下载和加载 GPT-2 的权重，附加内容有 Llama、Qwen3 等。用 Ollama 下载和管理模型 Tom 已经做过了 |
| 怎么用模型 | 教用自己的模型生成文字、做分类、回答指令 |
| 怎么建立模型 | **这是重点**，第 2 到 4 章从零搭 |
| 需要什么数学，为什么这样 | **不系统教数学。** 前提要求只写了 Python，没写数学。原理通过代码讲 |

### 补数学和直觉：两个免费资源

- **3Blue1Brown 的神经网络系列**，YouTube 免费，一共 7 集大约 3 小时。用动画讲神经网络是什么、梯度下降、反向传播和它背后的微积分、Transformer、注意力。适合在读书之前先看，建立直觉 https://www.3blue1brown.com/lessons/gradient-descent/
- **Karpathy 的 Neural Networks: Zero to Hero**，YouTube 免费，8 讲。第 1 讲从零写一个很小的自动求导库 micrograd，把反向传播的数学一行一行写成代码。后面几讲从字符级模型一直讲到 GPT 和分词器 https://github.com/karpathy/nn-zero-to-hero

### 建议的学习顺序

1. 3Blue1Brown 前 4 集，大约 1 个多小时：神经网络是什么，模型是怎么学的
2. Karpathy 第 1 讲：把反向传播的数学亲手写一遍。跟第三课 1KB 小 Tom 是同一个原理，更细
3. Raschka 的书，先看附录 A 学 PyTorch，再从第 1 章往下读
4. 读到第 3 章注意力之前，看 3Blue1Brown 第 5、6 集
5. 《AI Engineering》全程当闲书看

## 有名的、可以对照着看的

- **Build a Large Language Model (From Scratch)**，Sebastian Raschka，Manning 出版。用 PyTorch 一步步搭一个类似 ChatGPT 的模型。出版社页面说主要章节的代码在普通笔记本上就能跑。代码免费公开在 GitHub
  - 书 https://www.manning.com/books/build-a-large-language-model-from-scratch
  - 代码 https://github.com/rasbt/LLMs-from-scratch
- **nanoGPT**，Andrej Karpathy。大约 300 行的训练代码加 300 行的模型代码，从零训练 GPT。README 里专门写了 Mac 怎么跑
  - https://github.com/karpathy/nanoGPT

以上 2026-10-09 查的。

查证来源：

- 亚马逊商品页 https://www.amazon.com/dp/B0GWSRQSLK
- vLLM 在 macOS 上的支持 https://docs.vllm.ai/en/latest/getting_started/installation/cpu.html
- bitsandbytes 支持的平台 https://huggingface.co/docs/bitsandbytes/main/en/installation
- AutoAWQ 停止维护的公告 https://github.com/casper-hansen/AutoAWQ
- GPTQModel 支持 Apple Silicon https://github.com/ModelCloud/GPTQModel
- PyTorch MPS 的 bf16 autocast 讨论 https://github.com/pytorch/pytorch/issues/139386
- LLM Engineer's Handbook 出版信息 https://www.amazon.com/LLM-Engineers-Handbook-engineering-production/dp/1836200072
- LLM Engineer's Handbook 代码仓库和费用说明 https://github.com/PacktPublishing/LLM-Engineers-Handbook
- AI Engineering 作者页面 https://huyenchip.com/books/
- AI Engineering 出版信息 https://www.barnesandnoble.com/w/ai-engineering-chip-huyen/1146060853
- Raschka 的书 368 页，2024 年 9 月出版 https://www.manning.com/books/build-a-large-language-model-from-scratch
- GPT-4o 2024 年 5 月发布 https://en.wikipedia.org/wiki/GPT-4o
- Llama 3 2024 年 4 月发布，Llama 4 之后发布 https://en.wikipedia.org/wiki/Llama_(language_model)
- PyTorch 停止往官方 conda 频道发布 https://github.com/pytorch/pytorch/issues/138506
- Gemma 3 2025 年 3 月发布 https://en.wikipedia.org/wiki/Gemma_(language_model)
- Qwen3 2025 年 4 月发布 https://en.wikipedia.org/wiki/Qwen
- Raschka 的书和新书 https://sebastianraschka.com/books/
- Raschka 书的代码仓库，前提要求、视频、附加内容 https://github.com/rasbt/LLMs-from-scratch
- AI Engineering 书评，说书里没有代码 https://javarevisited.blogspot.com/2025/09/review-is-ai-engineering-book-by-chip.html
- Raschka 代码仓库 README，章节和附加内容 https://github.com/rasbt/LLMs-from-scratch
- 3Blue1Brown 神经网络系列 https://www.3blue1brown.com/lessons/gradient-descent/
- Karpathy 的 Neural Networks: Zero to Hero https://github.com/karpathy/nn-zero-to-hero
