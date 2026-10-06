"""Tom 的后端服务

启动方法：
    conda activate tom_lizard
    cd tom_lizard/app
    uvicorn main:app --reload

然后浏览器打开 http://127.0.0.1:8000
"""

from pathlib import Path
from typing import Literal

from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

import agent

HERE = Path(__file__).parent

app = FastAPI(title="Tom Lizard")


# 用 pydantic 规定网页发过来的数据长什么样。
# 格式不对的请求 FastAPI 会直接拒绝，不会进到我们的代码里。
class Message(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    messages: list[Message]


@app.get("/")
def index():
    return FileResponse(HERE / "static" / "index.html")


@app.get("/tom_icon.png")
def icon():
    return FileResponse(HERE.parent / "tom_icon.png")


# 这里用普通的 def 不用 async def。
# ollama 的 chat 是会卡住等结果的那种调用，用 def 的话 FastAPI 会把它放到另一个线程里跑，
# 这样 Tom 在想的时候服务器还能处理别的请求。
@app.post("/api/chat")
def chat(req: ChatRequest):
    history = [m.model_dump() for m in req.messages]
    return agent.run(history)
