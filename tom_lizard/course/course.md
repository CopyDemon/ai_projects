# Tom Lizard 课程

一课一个文件，文件名是 `lessonXX_主题.py`。每课都是能单独运行的小程序，学一个概念。学会的东西再搬进 Tom 的正式应用代码里。

运行任何一课：

```
conda activate tom_lizard
cd tom_lizard/course
python lessonXX_主题.py
```

## 课程列表

| 课 | 文件 | 主题 | 状态 |
| --- | --- | --- | --- |
| 1 | `lesson01_agent_loop.py` | agent 循环和工具调用 | 已跑通 |

## 第一课：agent 循环

学到的概念：

- **LLM**：大语言模型。它只会做一件事，读一段文字，接着往下写。
- **Ollama**：在自己电脑上跑开源模型的软件。它在后台开一个服务，代码通过它和模型说话。
- **tool calling**：给模型一份工具清单，模型可以回答“我要调用某个工具，参数是这些”。模型自己不执行任何东西，执行的是我们的代码。
- **agent 循环**：问模型，模型要工具就执行，把结果发回去，再问，直到模型直接给出回答。agent 的核心就是这个循环。
- **messages**：对话记录。模型本身不记事，每次请求都要把完整记录发过去。
- **thinking**：有些模型回答前会先输出一段思考过程，qwen3 就是。

实际跑的结果：问 (11434 + 12341) * 412，Tom 调用了 add 和 multiply，答案 9795300，正确。跑了两次都对。

注意到的问题：模型在同一轮里同时调用了 add 和 multiply，multiply 用的 23775 是它自己心算的，没等 add 的结果。这次算对了，但说明模型可能自己瞎算，不一定老老实实用工具。

查证来源：

- Ollama tool calling 官方文档 https://docs.ollama.com/capabilities/tool-calling
- Ollama 最新版本 0.35.1 https://github.com/ollama/ollama/releases
- qwen3 模型页面 https://ollama.com/library/qwen3
- ollama Python 库 0.6.3 https://pypi.org/project/ollama/
