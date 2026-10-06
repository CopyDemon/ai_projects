"""Tom 的大脑：agent 循环和工具

跟第一课的 agent 循环是同一个东西，只是改成可以接收整段对话，
并且把每一步做了什么记下来，交给网页显示。
"""

from ollama import chat

MODEL = "qwen3:8b"

SYSTEM_PROMPT = (
    "You are Tom, a friendly green lizard assistant. "
    "Use the tools for any math instead of calculating in your head. "
    "Always reply in the same language as the user's latest message. "
    "If the user writes in Chinese, your whole reply must be in Chinese."
)

# 防止模型一直要工具停不下来
MAX_STEPS = 10


def add(a: int, b: int) -> int:
    """Add two numbers.

    Args:
        a: The first number
        b: The second number

    Returns:
        The sum of the two numbers
    """
    return a + b


def multiply(a: int, b: int) -> int:
    """Multiply two numbers.

    Args:
        a: The first number
        b: The second number

    Returns:
        The product of the two numbers
    """
    return a * b


TOOLS = [add, multiply]
AVAILABLE_FUNCTIONS = {fn.__name__: fn for fn in TOOLS}


def run(history: list[dict]) -> dict:
    """跑一轮对话。

    history 是网页发过来的全部对话记录，每条是 {"role": "user" 或 "assistant", "content": "..."}。
    返回 Tom 的回答，还有中间的思考和工具调用，网页会把它们显示出来。
    """
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history
    steps = []

    for _ in range(MAX_STEPS):
        response = chat(model=MODEL, messages=messages, tools=TOOLS, think=True)
        msg = response.message
        messages.append(msg)

        if msg.thinking:
            steps.append({"type": "thinking", "text": msg.thinking.strip()})

        if not msg.tool_calls:
            return {"reply": msg.content, "steps": steps}

        for tc in msg.tool_calls:
            name = tc.function.name
            args = tc.function.arguments
            fn = AVAILABLE_FUNCTIONS.get(name)
            result = fn(**args) if fn else f"unknown tool {name}"
            steps.append({"type": "tool", "name": name, "args": args, "result": str(result)})
            messages.append({"role": "tool", "tool_name": name, "content": str(result)})

    return {"reply": "我想了太多步还没想完，先停在这里。", "steps": steps}
