# Snake Eye 环境记录

每装一样东西、删一样东西，都要在这里写清楚：哪天、装了什么、版本、为什么要装、用什么命令装的。

## 一、整体结构

前端和后端分开。

- **前端**：`frontend/` 文件夹，用 React 写，用 Vite 构建。源码在 `frontend/src/`，构建出来的成品在 `frontend/dist/`。部署时只要 `dist/` 文件夹，里面是纯静态文件，放到任何能送文件的服务器上都能用，设备上不用装 Node
- **后端**：还没写。以后用 FastAPI 写，跑在 conda 环境 `snake_eye` 里，调 Ollama 的看图模型

前端开发用 Vite 自带的开发服务器。看成品可以用 Python 自带的 `http.server` 把 `dist/` 送出去，不用装包。

为什么不直接双击打开 html 文件：浏览器开摄像头要求"安全上下文"，就是 https、localhost 或 file:// 三种之一。file:// 理论上可以，但各家浏览器对 file:// 开摄像头的态度不一样，而且 Vite 构建出来的 html 用绝对路径引用 js，双击打开会找不到文件。用 localhost 最稳。

## 二、电脑上的基础软件

跟 Tom 共用，详见 `tom_lizard/environment.md`：Ollama 0.35.0，Miniforge conda 24.3.0。

另外用到：

| 软件 | 版本 | 干什么用 |
| --- | --- | --- |
| Node | v24.11.0 | 跑 Vite 和 npm，只在开发和构建前端时用。部署好的 dist 不需要它 |
| npm | 随 Node 装的 | 装前端的包 |
| Google Chrome | 154.0.8037.98 | 测试前端。无头模式加 `--use-fake-device-for-media-stream` 可以用假摄像头自动测，不用真人点允许 |

## 三、模型

还没下载看图模型。第二步再选，候选见 `snake_eye.md`。

`nomic-embed-text` 274MB，2026-10-06 下载的，用于以后做记忆的 embedding。现在还没用到。

## 四、怎么启动

现在只有前端。

开发时，改代码浏览器自动刷新：

```
cd snake_eye/frontend
npm run dev
```

浏览器打开 http://localhost:5173 ，点"开始看"，第一次浏览器会问要不要允许用摄像头。打开 http://localhost:5173/?auto=1 会自动开始。注意 Vite 监听的是 localhost，用 127.0.0.1 可能连不上，2026-10-06 本机就是这样。

构建成品：

```
cd snake_eye/frontend
npm run build
```

成品在 `frontend/dist/`，2026-10-06 构建出来一共 240KB，4 个文件。看成品效果：

```
conda activate snake_eye
cd snake_eye
python -m http.server 8080 --bind 127.0.0.1 --directory frontend/dist
```

浏览器打开 http://127.0.0.1:8080 。`--bind 127.0.0.1` 是只让本机访问。以后手机要连，要改成 `--bind 0.0.0.0`，而且手机那边必须是 https，见 `snake_eye.md` 技术方案。

用完 `Ctrl+C` 关掉。

## 五、conda 环境

| 环境名 | Python | 建立日期 | 用途 |
| --- | --- | --- | --- |
| snake_eye | 3.12.15 | 2026-10-06 | 后端专用。现在是空的，只有 Python 自带的东西 |

建环境的命令：

```
conda create -y -n snake_eye python=3.12
```

从零重建：

```
cd snake_eye
conda env create -f environment.yml
conda activate snake_eye
```

2026-10-06 用 environment.yml 建了测试环境 snake_eye_verify，能用它跑 http.server 送出网页，验证完删除。

### 一个坑：conda run 可能用错 Python

2026-10-06 发现，在一个 PATH 里已经排着别的环境（当时是 tom_lizard）的终端里，`conda run -n snake_eye python` 实际跑的是 tom_lizard 的 Python，`pip list` 看到一堆 fastapi、ollama 都是 tom_lizard 的。原因是 conda run 把 snake_eye 的 bin 目录加在 PATH 中间，排在前面的 tom_lizard 先被找到。

避开办法：新开一个终端再 `conda activate snake_eye`，或者直接用绝对路径 `~/miniforge3/envs/snake_eye/bin/python`。不确定的时候跑一句 `python -c "import sys; print(sys.executable)"` 看是哪个 Python。

## 六、Python 包

还没装任何包。建环境时自带 pip 26.2.1、setuptools 84.0.0、wheel 0.48.0。

## 六点五、前端的 npm 包

都在 `frontend/package.json` 里，版本锁在 `frontend/package-lock.json`。2026-10-06 用 `npm create vite@latest frontend -- --template react` 建的项目，create-vite 9.2.1，然后 `npm install` 装的。

| 包 | 版本 | 干什么用 | 为什么要装 |
| --- | --- | --- | --- |
| react | 19.3.0 | React 本身，组件、state、effect 这些 | 前端换成 React 写 |
| react-dom | 19.3.0 | 把 React 组件画到浏览器页面上 | React 分两半，这一半管浏览器 |
| vite | 8.3.3 | 开发服务器和构建工具，把 jsx 变成浏览器能跑的 js，打包成 dist | React 官方文档推荐的从零搭法 |
| @vitejs/plugin-react | 6.1.2 | 让 Vite 认识 React 的 jsx 写法 | Vite 模板自带 |
| @types/react, @types/react-dom | 19.3.0 | React 的类型说明，编辑器用来提示 | 模板自带，不影响运行 |
| oxlint | 1.87.0 | 代码检查工具，`npm run lint` 用的 | 模板自带，能提醒 React 的常见错法 |

`node_modules/` 54MB 和 `dist/` 都在模板自带的 `.gitignore` 里，不进 git。重建只要：

```
cd snake_eye/frontend
npm install
```

2026-10-06 只用 dist 测过：把 dist 用 http.server 送出去，Chrome 假摄像头 8 秒拍 3 张，和开发服务器结果一样。

## 七、以后装新包的规矩

跟 Tom 一样：先上网查，`pip install 包名==版本号` 写死版本，加进 environment.yml，在这里记一笔，重建验证，跑一遍代码。

## 八、变更记录

| 日期 | 做了什么 | 命令 |
| --- | --- | --- |
| 2026-10-06 | 建 conda 环境 snake_eye，Python 3.12.15，没装别的 | `conda create -y -n snake_eye python=3.12` |
| 2026-10-06 | 写 environment.yml，建测试环境验证能送出网页，验证完删除 | `conda env create -f environment.yml -n snake_eye_verify` 和 `conda env remove -n snake_eye_verify` |
| 2026-10-06 | 前端换成 React，用 Vite 模板建项目，装了 react 19.3.0、vite 8.3.3 等 7 个包，node_modules 54MB | `npm create vite@latest frontend -- --template react` 和 `npm install` |
