# Snake Eye

一个能"看"的 AI：一个很小的前端负责开摄像头拍照并不断传给服务器，服务器上的后端用模型看图、回答你的问题，答不上来就上网查，查到的东西记下来，下次直接会。

原始想法在 `readme.md`。这个文件记需求、路线图、技术方案和进度，边学边改。

## 先说实话：这个项目赚不赚钱

- **直接赚钱：很难。** 摄像头加 AI 问答这件事，大厂已经有成熟产品，手机 App 和智能眼镜都能做。一个人做出来的版本，没人会付钱
- **长期成长：很有用。** 要碰的东西，多模态模型、前后端分离、设备往服务器传数据、检索记忆、联网查资料，都是现在接活和找工作最常问的。而且跟 Tom Lizard 路线图里的"能动手"和"能记事"两步重合，做了这个等于 Tom 也往前走了
- 结论：当学习项目做，值得。别指望它变成产品

## 架构：前后端分离

2026-10-06 定的。前端和后端是两个独立的程序，中间靠网络说话。

```
前端，很小，只干三件事          后端，在固定服务器上，干重活
┌──────────────────┐            ┌─────────────────────────────┐
│ 1. 开摄像头拍一张  │  每隔几秒   │ 收图 → 看图模型描述 → 写日志   │
│ 2. 传给服务器     │ ─────────→ │ 收问题 → 查日志、查记忆、上网  │
│ 3. 显示回答       │ ←───────── │        → 模型回答 → 返回      │
└──────────────────┘            │ Ollama 跑模型，向量库存记忆    │
  手机 / 树莓派 / 电脑            └─────────────────────────────┘
```

前端打算做两种，都很小：

- **Python 脚本版**：几十行，用 opencv 拍照，用 HTTP 传给服务器。能跑在 Mac、树莓派这类有摄像头的小设备上
- **网页版**：一个 HTML 文件，用浏览器自带的摄像头接口拍照上传。手机打开网页就能用，不用装 App。限制是浏览器只在 HTTPS 或 localhost 下才允许开摄像头，手机连服务器必须配 HTTPS 证书，见下面技术方案

后端一套代码，不管前端是谁，接口一样。

### "固定服务器"现在是哪台

现在只有这台 M2 Pro 跑得动模型，所以**第一阶段服务器就是这台 Mac**，前端在手机或另一台电脑上，走家里 WiFi 连过来。代码从第一天就按前后端分离写，以后把后端搬到别的机器上只要改一个地址。

以后真要放到外面的固定服务器上，有两条路，到时候再选：

1. 家里放一台一直开着的机器当服务器，一次性花钱，之后不花
2. 租带 GPU 的云服务器，按月付费。这违反"不依赖付费云服务"的规矩，要你明确同意，到时候我先查价格再说

## 先纠正一个概念：什么叫"不断学习"

readme 里说"机器学习会通过每次用户询问不断迭代更新"。这里要分清两种"学习"：

1. **改模型本身**：就是 Tom 第三课那种训练，调模型里的数字。每问一次就重新训练一遍，做不到也没必要。大模型微调一次要几小时，而且教不进新知识，详见 `tom_lizard/research/model_customization.md`
2. **改模型外面的系统**：模型不动，把每次问答和上网查到的东西存进服务器上的资料库。下次问类似问题时，先从资料库里找出相关内容，连着问题一起发给模型。这叫 **RAG**，检索增强生成。模型没变，但整个系统确实"越用越懂"

Snake Eye 做第 2 种，这也是业界做"记忆"的标准做法。你 2026-10-06 下载的 `nomic-embed-text` 模型就是干这个用的，它把一段文字变成一串数字，用来找相似的内容。

## 硬件上能做到什么程度

M2 Pro 32GB 跑一个 8B 的看图模型，看一张图要几秒钟。所以"不断检测周围环境"不是每秒几十帧的实时视频，而是**前端每隔几秒传一张照片，服务器看一眼，记下来**。这对"回答你看到了什么"够用，也省流量。要真正实时识别物体，得用传统的小视觉模型，比如 YOLO，那是以后的事。

## 路线图

每一步做完都要是能跑的东西。

1. **网页前端一直看**：浏览器开摄像头，每隔几秒拍一张。先用原生 JS 写通，再换成 React。**已完成**
2. **看一张照**：下载一个看图模型，把一张照片发给它，问"图里有什么"。学多模态模型和 `images` 参数
3. **后端收图**：用 FastAPI 写一个接口，收到一张图就调模型描述，把时间和描述写进日志。用 curl 传图测试
4. **前端连后端**：把第一步网页里的 handleFrame 改成 POST 发给后端。先在同一台 Mac 上跑，验证整条链路
5. **手机连进来**：给 Mac 配 HTTPS 证书，手机走家里 WiFi 打开同一个网页。以后有树莓派之类的小设备再写 Python 脚本版前端
6. **能问答**：后端加一个问答接口，把最近几条日志连着问题发给模型回答。前端加输入框
7. **会上网查**：问到模型不知道的东西，它调用搜索工具上网查。接着 Tom 第一课的 tool calling 做
8. **记得住**：问答和查到的东西存进向量库，下次先查库再回答。学 embedding 和 RAG
9. **搬家**：后端搬到固定服务器，前端只改地址

## 要求

1. 模型用 Ollama 在自己的机器上跑，不调云端模型 API。上网搜索用免费的搜索接口
2. 摄像头照片只在自己的设备和自己的服务器之间传。第一阶段只走家里 WiFi。以后后端放到公网上，必须加 HTTPS 和密码，没加之前不开放
3. 前端部署只要 `frontend/dist/` 文件夹，纯静态文件，设备上不用装 Node。手机打开网页就能用
4. 一次只推进一步，每步做完更新这个文件和 `environment.md`

## 技术方案

草稿，第一步做了再定。

- 后端：Python 3.12，conda 环境 `snake_eye`，跟 Tom 分开。FastAPI 加 uvicorn，复用 Tom 的写法。uvicorn 要加 `--host 0.0.0.0` 才能让手机连进来
- 前后端接口：HTTP，图片用 POST 传。先这样，够用。以后要连续视频再考虑 WebSocket
- 看图模型，2026-10-06 在 https://ollama.com/search?c=vision 查到的候选：
  - `qwen3-vl:8b`，6.1GB，Qwen 家的看图模型，跟 Tom 用的 qwen3:8b 同一家。页面只标了 vision，支不支持 tool calling 还没确认，第二步要实际测
  - `gemma4:e4b`，6.6GB，Google 的，Ollama 官方 vision 文档的例子就用它，还支持音频输入
  - `minicpm-v4.5:8b`，6.1GB，专门做视频理解，但 Ollama 页面没标 tools
  - 第二步先装一个试，三个都在 32GB 内存里跑得动
- 摄像头，Python 前端：`opencv-python`，2026-10-06 查 PyPI 最新版 5.0.0.93。macOS 第一次用会弹权限窗口，要在系统设置里给终端或 VS Code 开摄像头权限。本机有 FaceTime HD Camera，还有一个 iPhone 连续互通摄像头
- 摄像头，网页前端：浏览器的 `getUserMedia` 接口。MDN 明确写了只在安全上下文可用，就是 HTTPS 或 localhost，否则 `navigator.mediaDevices` 是 undefined。所以第五步要用 `mkcert` 给 Mac 做一张本地信任的证书，再把它的根证书装到手机上
- 记忆：`nomic-embed-text` 做 embedding，向量库第八步再选
- 前端：React 19 加 Vite 8。2026-10-06 查 React 官方文档，建新项目推荐 Next.js 或 React Router，或者用 Vite 从零搭，Create React App 已经不推荐。这里用 Vite，因为后端是 FastAPI，用不上 Next.js 的服务端功能

## 查证来源

- Ollama 看图模型列表 https://ollama.com/search?c=vision
- Ollama 官方 vision 文档，Python 发图片的写法 https://docs.ollama.com/capabilities/vision
- qwen3-vl https://ollama.com/library/qwen3-vl
- gemma4 https://ollama.com/library/gemma4
- minicpm-v4.5 https://ollama.com/library/minicpm-v4.5
- opencv-python https://pypi.org/project/opencv-python/
- macOS 摄像头权限问题 https://forum.opencv.org/t/opencv-not-authorized-to-capture-video-status-0-requesting/8512
- 浏览器摄像头接口必须 HTTPS https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia
- mkcert 做本地证书，以及怎么让 iPhone 信任 https://www.process-one.net/blog/using-a-local-development-trusted-ca-on-macos/

## 进度记录

- 2026-10-06 写了 readme 里的想法
- 2026-10-06 查证了看图模型和摄像头方案，定了路线图草稿
- 2026-10-06 架构改成前后端分离，前端小而轻放在手机或小设备上，后端在服务器上。第一阶段服务器就是这台 Mac
- 2026-10-06 建了 conda 环境 snake_eye，没装包。写了网页前端 `frontend/`，html、css、js 分开放，摄像头一直开着，每隔几秒拍一张。用 Chrome 假摄像头测过，8 秒拍 3 张，640x480，每张 8KB。真摄像头还没在浏览器里点过允许，下次打开页面试
- 2026-10-06 前端换成 React 19 加 Vite 8，摄像头逻辑搬进 Camera 组件，原生 JS 版删了。dist 240KB，开发版和 dist 版都用假摄像头测过，8 秒拍 3 张

## 第一步学到的东西：网页前端一直看

代码在 `frontend/`，React 项目，启动方法见 `environment.md`。先用原生 JS 写了一版跑通，再换成了 React，原生版删了，逻辑都搬进了 React 组件。

文件分工：

- `index.html`：只有一个空的 `<div id="root">`，页面内容全是 React 画上去的
- `src/main.jsx`：入口，把 App 组件画到 root 里
- `src/App.jsx`：整个页面，现在就一个标题加一个 Camera 组件。以后问答框加在这里
- `src/components/Camera.jsx`：摄像头组件，开摄像头、定时拍、把照片交给外面
- `src/components/Camera.css`：这个组件的样式
- `src/index.css`：全局样式

页面做的事：

1. `getUserMedia` 向浏览器要摄像头，拿到一个视频流，塞给 `<video>` 标签实时显示
2. `setInterval` 每隔几秒调一次 `takeFrame`
3. `takeFrame` 把视频当前这一帧画到一个看不见的 `<canvas>` 上，再用 `toBlob` 转成 jpeg
4. 拍到的 jpeg 交给 `onFrame`。现在 App 没传 onFrame，照片只显示和计数，第四步传一个函数进去发给后端

学到的概念，浏览器部分：

- **getUserMedia**：浏览器自带的接口，网页用它要摄像头和麦克风。不用装任何库，手机电脑都有
- **安全上下文**：浏览器只在 https、localhost 或 file:// 下才给这个接口，否则 `navigator.mediaDevices` 直接是 undefined。所以本机走 localhost，手机以后要走 https
- **facingMode: environment**：手机上选后置摄像头，电脑上没有就用默认的
- **canvas 当暗房**：视频流本身不能直接存成图片，要先画到 canvas 上再导出。jpeg 质量 0.8，一张 640x480 只有 7KB 左右，以后每隔几秒传一张给服务器，流量很小
- **blob**：一块二进制数据，这里就是一张 jpeg 文件的内容。以后 POST 给后端的就是它

学到的概念，React 部分：

- **组件**：一个函数，返回一段页面。Camera 就是一个组件，以后手机页和电脑页都能用它
- **JSX**：在 js 里直接写 html 的写法，浏览器看不懂，要 Vite 翻译成普通 js
- **state**：`useState` 存的数据。改了它页面自动跟着变，不用自己去改元素。拍的张数、最近一张、错误信息都是 state。原生版要手动 `getElementById` 再改 textContent，React 版只管改数据
- **ref**：`useRef` 存的东西。改了它页面不会变，用来放真实的 DOM 元素和摄像头流这种"不是画面"的东西
- **effect**：`useEffect`，state 变了以后要跟外面的东西打交道时用。定时器、标签页标题、自动开始都是 effect。每个 effect 可以返回一个清理函数，state 再变或组件拆掉时自动调用，定时器就是这样清掉的
- **props**：外面传给组件的参数，`onFrame` 就是。组件只管拍，拍到的照片怎么处理由外面决定，这样组件才能复用
- **lint 教的两条规矩**：effect 里不要同步改 state，effect 用到的变量都要写进依赖列表。原来 `start` 里先 `setError('')` 再开摄像头被 lint 抓出来，改成开完摄像头再改 state
- **StrictMode**：开发时 React 会故意把每个组件跑两遍找问题。所以 `start` 开头要检查摄像头是不是已经开了，不然自动开始会开两次
- **Vite 的开发和构建**：`npm run dev` 是开发服务器，改代码浏览器立刻刷新。`npm run build` 把所有东西打包进 `dist/`，4 个文件 240KB，部署只要这个文件夹
- **自动测试浏览器**：Chrome 无头模式加 `--use-fake-device-for-media-stream` 会给一个绿色假摄像头，加 `--use-fake-ui-for-media-stream` 会自动点允许。页面跑起来后要靠 Chrome 调试协议去读页面状态，用 Node 自带的 WebSocket 连上调试端口发命令就行。`--dump-dom` 不行，它在页面刚加载时就输出了

查证来源：

- getUserMedia 和安全上下文 https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia
- React 官方建项目指南 https://react.dev/learn/creating-a-react-app
- Vite 官方入门 https://vite.dev/guide/
