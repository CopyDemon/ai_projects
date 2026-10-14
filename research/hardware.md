# 资料：哪台电脑适合跑本地模型

2026-10-09 查的。硬件参数不会变，但软件支持会变，用之前要重新核对第三部分。

## 一、三台电脑

| | MacBook Pro 14 寸 2023 | Mac Studio 2023 | 台式机 |
| --- | --- | --- | --- |
| 芯片 | M2 Pro | M2 Max | i7-4770K 加 GTX 1080 Ti |
| 模型能用的内存 | 32GB 统一内存 | **64GB 统一内存** | **11GB 显存**，超出部分要放到主板内存里 |
| 内存带宽 | 200GB/s | 400GB/s | 显存 484GB/s |
| GPU | 16 或 19 核 | 30 或 38 核，还没确认是哪种 | 3584 个 CUDA 核心，Pascal 架构，2017 年 |
| 功耗 | | | 显卡 TDP 250W |
| 现在用来干什么 | 开发 Tom，跑 qwen3:8b | 没用 | 没用 |

台式机还不知道的：主板内存多大，装的什么系统，NVIDIA 驱动是哪个版本。

## 二、跑模型看什么

- **能装下多大的模型，看内存**。模型必须整个放进显存或统一内存才跑得快。放不下的部分会挪到 CPU 和普通内存上，速度会慢很多
- **吐字快不快，主要看内存带宽**。每生成一个字，都要把模型的参数从内存里读一遍
- **Mac 的统一内存**：CPU 和 GPU 共用同一块内存，所以 64GB 的大部分都能给模型用。普通电脑的显卡只能用自己的显存，1080 Ti 就是 11GB

按 Ollama 页面上的模型大小，2026-10-02 查的：

| 模型 | 文件大小 | MacBook M2 Pro 32GB | Mac Studio M2 Max 64GB | 1080 Ti 11GB |
| --- | --- | --- | --- | --- |
| qwen3:8b | 5.2GB | 能 | 能 | 能 |
| qwen3:14b | 9.3GB | 能 | 能 | 很勉强，上下文一长就放不下 |
| qwen3.6:27b | 19GB | 能，但剩给别的程序的内存不多 | 能，很宽松 | 放不下 |
| qwen3.6:35b | 24GB | 很勉强 | 能 | 放不下 |

实际跑起来还要额外占内存存上下文，上下文越长占得越多，所以不能只看文件大小。上面这张表是按文件大小估的。

2026-10-09 在 MacBook 上实测了 qwen3:8b，文件 5.23GB：

| 上下文长度 | 实际占内存 |
| --- | --- |
| 4096 | 5.92GB |
| 16384 | 7.85GB |
| 32768，Ollama 0.40.0 的默认 | 10GB |
| 40960 | 11.51GB |

大约每 1000 个 token 多占 0.15GB。别的模型多占多少不一样，模型越大一般占得越多。所以 1080 Ti 的 11GB 和 Jetson 的 8GB 跑 qwen3:8b 都得把上下文调小。

## 三、软件支持情况

### GTX 1080 Ti 的问题：老了，正在被各家放弃

- **NVIDIA 驱动**：580 系列是最后一个支持 GTX 10 系列的驱动。2025 年 10 月以后不再有新的功能更新，只有安全更新到 2028 年
- **Ollama**：支持算力等级 5.0 以上的显卡，1080 Ti 是 6.1，在支持列表里。但 5.0 到 6.2 的显卡要求驱动 570 以上，所以要装 570 到 580 之间的驱动
- **PyTorch**：最常用的 AI 训练框架。2.8 版开始，CUDA 12.8 的版本已经不支持 Pascal 了，只有 CUDA 12.6 的版本还支持。官方计划 2.15 版删掉 CUDA 12.6，**2.14 是最后一个支持 1080 Ti 的版本**
- 1080 Ti 没有 Tensor Core，就是新显卡上专门加速 AI 运算的那部分硬件

### Mac 的情况：越来越好

- **Ollama**：2026-09-25 发布的 0.40.0 开始，Apple Silicon 上支持的模型会自动用苹果的 MLX 跑。2026-10-08 最新正式版是 0.40.2。我们那台 MacBook 上还是 0.35.0，App 应该会自己更新
- **微调**：苹果官方的 mlx-lm 可以在 Mac 上做 LoRA 微调，见 `tom_lizard/research/model_customization.md`。64GB 比 32GB 宽松得多

## 四、结论

**Mac Studio M2 Max 64GB 明显更好**：

1. 能跑的模型大得多。64GB 能宽松地跑 27B 和 35B 的模型，1080 Ti 最多跑 8B 到 14B
2. 速度不吃亏。带宽 400GB/s，1080 Ti 是 484GB/s。跑能放进 11GB 的小模型，1080 Ti 可能稍快一点，但差得不多。这个没实际测过
3. 软件在往 Mac 这边倾斜，1080 Ti 正在被驱动和 PyTorch 放弃
4. 安静省电，适合一直开着当模型服务器

**1080 Ti 台式机**：可以跑小模型当第二个服务器，但不值得在上面花时间搭环境。

## 五、推荐的用法：Mac Studio 当模型服务器

```
MacBook 上写代码、跑 Tom 网页  →  局域网  →  Mac Studio 上的 Ollama 跑大模型
```

Ollama 默认只让本机访问，地址是 `127.0.0.1:11434`。要让局域网里的其他电脑访问，按官方文档在 Mac Studio 上设置：

```
launchctl setenv OLLAMA_HOST "0.0.0.0:11434"
```

然后重启 Ollama App。Tom 的代码里把 Ollama 地址改成 Mac Studio 的局域网 IP 就行。

**安全提醒**：Ollama 没有自带的密码验证。改成 `0.0.0.0` 以后，同一个网络里的任何设备都能用它。家里的网络问题不大，**不要在公共网络或者公司网络上这么做**。

这一步还没做，做的时候要实际测一遍。

## 六、如果换成 RX 7900 XTX

2026-10-09 查的。这张卡我现在没有，是假设。

### 规格

| | RX 7900 XTX | Mac Studio M2 Max | GTX 1080 Ti |
| --- | --- | --- | --- |
| 模型能用的内存 | 24GB 显存 | 64GB | 11GB |
| 内存带宽 | **960GB/s** | 400GB/s | 484GB/s |
| 功耗 | 整卡 355W，建议 800W 电源 | | 250W |
| 架构 | AMD RDNA 3，gfx1100，2022 年底发布 | | NVIDIA Pascal，2017 年 |

### 跟 Mac Studio 比

- **快**：带宽是 Mac Studio 的 2.4 倍。放得进 24GB 的模型，按带宽算吐字速度大概能快一倍多。这只是按带宽推算，没实际测过
- **装得少**：24GB 能跑 qwen3:14b 和 qwen3.6:27b，27B 文件 19GB，剩的空间不多，上下文不能太长。qwen3.6:35b 文件 24GB，放不下。Mac Studio 64GB 能跑更大的模型
- 简单说：**7900 XTX 是跑中等模型跑得快，Mac Studio 是能跑更大的模型**

### 软件支持

- **Ollama**：官方文档写着 Linux 和 Windows 都支持 RX 7900 XTX。Linux 要装 AMD ROCm 7 驱动，Windows 要支持 ROCm 7 和 HIP 7 的驱动
- **ROCm**：AMD 的 AI 计算平台，作用相当于 NVIDIA 的 CUDA。官方 Linux 支持列表里有 RX 7900 XTX。2026-10-09 最新是 ROCm 7.14.0，支持 Ubuntu 22.04 和 24.04 等
- **Windows**：网上文章说 2026 年 3 月的 ROCm 7.2 开始 Windows 也能原生装，PyTorch 也能用，但都说 Linux 上最稳。这条来自第三方文章，AMD 官方的 Linux 文档里没提 Windows
- **不是 CUDA**：很多 AI 工具和教程默认用 NVIDIA 显卡，AMD 能用的越来越多，但偶尔会遇到只支持 CUDA 的东西

### 放进 4770K 台式机的问题

- 建议电源 800W，台式机原来的电源多大还不知道，很可能要换
- 这台机器 2013 年的，CPU 和主板都很老。只跑推理的话，模型全在显卡里，CPU 影响不大。这一点没有专门查证

### 价格，2026-10-09 查的

- 新的：美国最低零售大约 1358 美元，上市价是 999 美元
- 二手：几个网站说法不一样，eBay 大约 765 美元，另一个网站最低挂牌 1083 美元
- 价格变化快，要买的时候重新查

### 结论

- **手上已经有的话**：值得用。装 Linux 当模型服务器，跑 27B 以内的模型比 Mac Studio 快
- **为这个专门去买的话**：现在不值得。Mac Studio 已经能跑更大的模型，不花一分钱。花 1000 美元左右换速度快一倍，现在的学习阶段用不上。等以后真有需要速度的场景，比如给客户跑服务，再考虑

## 七、如果买 NVIDIA Jetson Orin Nano Super 开发套件

2026-10-09 查的。这个也是假设，现在没有。

### 规格，NVIDIA 官方页面

| | Jetson Orin Nano Super | MacBook M2 Pro | Mac Studio M2 Max | RX 7900 XTX |
| --- | --- | --- | --- | --- |
| 模型能用的内存 | **8GB**，跟系统共用 | 32GB | 64GB | 24GB |
| 内存带宽 | **102GB/s** | 200GB/s | 400GB/s | 960GB/s |
| 功耗 | **7W 到 25W** | | | 355W |
| 价格 | 399 美元 | 已有 | 已有 | 新的约 1358 美元 |

- GPU：Ampere 架构，1024 个 CUDA 核心，32 个 Tensor Core
- CPU：6 核 ARM Cortex-A78AE
- AI 算力：官方写 67 INT8 TOPS
- 存储：SD 卡和外接 NVMe 固态硬盘
- 官方定位：机器人、边缘 AI、视觉 AI，能跑小的语言模型和视觉模型

### 价格

- 2024 年 12 月上市时 249 美元
- 2026 年 7 月 22 日涨到 399 美元，涨了 60%。文章说 NVIDIA 之前因为内存太贵停产了几款 Jetson 模块，但没直接说这次涨价的原因
- 有些店卖 529 美元，有些店缺货

### 跑语言模型的实际速度

都是第三方测的，质量参差不齐，只能当参考：

- NVIDIA Jetson AI Lab 的数据，被别的文章引用的：Llama 3.2 3B 每秒约 27.7 个 token
- 有文章说 7B 左右的模型用 Ollama 每秒 14 到 15 个 token。但那篇文章写了一个不存在的 “Llama 3.2 7B”，可信度要打折扣
- 越小的模型越快，1B 以下的模型每秒能过 100 个 token

### Ollama 支持

Ollama 官方的显卡支持页面里没有提到 Jetson。网上有人在 Jetson 上用 Ollama 跑，但官方支持情况没确认，真要用得先查清楚。

### 跟我们已有的电脑比

- **装得最少**：8GB 还要分给系统用。在 MacBook 上实测，qwen3:8b 上下文 4096 时占 5.92GB，Ollama 默认的 32768 要 10GB，Jetson 放不下默认设置，必须把上下文调小
- **最慢**：带宽 102GB/s，是现在这台 MacBook 的一半，Mac Studio 的四分之一
- **最省电、最小**：7W 到 25W，巴掌大，适合装进机器人、摄像头这类设备里一直跑

### 结论

- **拿来跑 Tom 的语言模型**：不值得。399 美元买到的东西比手上已有的两台 Mac 都弱
- **它真正适合的**：给实体设备加 AI，比如机器人、智能摄像头、工厂里的检测设备。这是另一个方向，要学 Linux、摄像头、传感器、CUDA 这些
- **什么时候考虑买**：如果以后决定往边缘 AI 或机器人方向赚钱，比如给小工厂做视觉检测设备，那时它是很便宜的入门板子。现在不需要

## 八、MacBook 能不能用 PyTorch 训练 Transformer

2026-10-09 实测。建了一个临时 conda 环境装 PyTorch 2.14.1，测完删了。

- 苹果官方要求：苹果芯片，macOS 14 以上，Python 3.10 以上。这台是 macOS 26.6.2，M2 Pro 19 核 GPU，符合
- PyTorch 在 Mac 上用 GPU 叫 MPS。`torch.backends.mps.is_available()` 返回 True，能用

训练速度，每种跑了几步取平均：

| 模型 | 参数量 | 设备 | 每步 | 每秒处理 token | GPU 内存 |
| --- | --- | --- | --- | --- | --- |
| 跟 nanoGPT 莎士比亚例子一样大：6 层，384 维，上下文 256，batch 64 | 10.8M | CPU | 1607ms | 约 1 万 | |
| 同上 | 10.8M | **GPU** | **411ms** | 约 4 万 | 4.4GB |
| GPT-2 small 那么大：12 层，768 维，上下文 512，batch 4 | 162.6M | GPU | 776ms | 约 2600 | 7.0GB |

GPT-2 small 原本是 124M，这里是 162.6M，因为测试代码里输入和输出层没有共用参数，多算了一份词表。

能做到什么：

- GPU 比 CPU 快大约 4 倍。nanoGPT 的 README 说 Mac 用 MPS 能快 2 到 3 倍，差不多
- nanoGPT 莎士比亚例子默认训练 5000 步，按每步 411ms 算大约 **34 分钟**。README 说一张 A100 显卡要 3 分钟
- GPT-2 small 大小的模型能训练，7GB 内存够用，但很慢。从头练出真正能用的 GPT-2，nanoGPT 说要 8 张 A100 跑 4 天，这台电脑做不到
- 所以：学习用的小模型完全够；从头训练大模型不行，也没必要
- Mac Studio M2 Max 的 GPU 核心和内存带宽都比这台多，应该更快，没实测

## 查证来源

- Mac Studio 2023 规格，苹果官方 https://support.apple.com/en-us/111835
- MacBook Pro 14 寸 2023 规格，苹果官方 https://support.apple.com/en-us/111340
- GTX 1080 Ti 规格 https://gamersnexus.net/news-pc/2820-official-nvidia-gtx-1080-ti-specs-announced 和 https://nvidianews.nvidia.com/news/nvidia-introduces-the-beastly-geforce-gtx-1080-ti-fastest-gaming-gpu-ever
- Ollama 显卡支持 https://docs.ollama.com/gpu
- Ollama 网络设置 https://docs.ollama.com/faq
- Ollama 发布记录 https://github.com/ollama/ollama/releases
- NVIDIA 580 驱动是最后一个支持 GTX 10 系列的 https://www.tomshardware.com/pc-components/gpu-drivers/nvidia-to-axe-maxwell-pascal-and-volta-gpus-with-end-of-driver-support-580-series-drivers-will-be-the-last-to-support-gtx-900-and-1000-cards
- PyTorch 2.8 去掉 Pascal 支持 https://dev-discuss.pytorch.org/t/cuda-toolkit-version-and-architecture-support-update-maxwell-and-pascal-architecture-support-removed-in-cuda-12-8-and-12-9-builds/3128
- PyTorch 2.15 计划去掉 CUDA 12.6 https://github.com/pytorch/pytorch/issues/190385
- RX 7900 XTX 规格 https://www.bhphotovideo.com/c/product/1739451-REG/amd_radeon_rx_7900_xtx.html/specs 和 https://www.techradar.com/news/amd-announces-new-radeon-rx-7900-xtx-and-rx-7900-xt-in-major-challenge-to-nvidia
- ROCm Linux 支持列表 https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html
- ROCm Windows 支持列表 https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/compatibility/compatibilityrad/windows/windows_compatibility.html
- 第三方文章，AMD 显卡跑 AI 的现状 https://idfs.ai/blog/amd-gpus-for-ai-inference-2026
- 价格 https://gpuprix.com/us/gpus/radeon-rx-7900-xtx 和 https://gpupoet.com/gpu/shop/amd-radeon-rx-7900-xtx
- Jetson Orin Nano Super 官方规格 https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-orin/nano-super-developer-kit/
- Jetson 涨价新闻 https://www.cnx-software.com/2026/07/22/nvidia-increases-the-price-of-jetson-modules-and-devkits-by-up-to-101/
- Jetson 店铺价格 https://www.sparkfun.com/nvidia-jetson-orin-nano-developer-kit.html
- Jetson 跑语言模型的第三方测试 https://www.jeremymorgan.com/blog/tech/nvidia-jetson-orin-nano-speed-test/ 和 https://gist.github.com/yalexx/f9840e347c11f7d198ff7490570eb702 和 https://www.navyaai.com/blog/jetson-orin-nano-llm-benchmark
- 苹果官方 PyTorch on Mac 说明 https://developer.apple.com/metal/pytorch/
- PyTorch 版本 https://pypi.org/project/torch/
- nanoGPT 的配置和 Mac 说明 https://github.com/karpathy/nanoGPT
