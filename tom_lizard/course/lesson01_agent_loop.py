"""第一课：最小的 agent 循环

运行方法：
    conda activate tom_lizard
    cd tom_lizard/course
    python lesson01_agent_loop.py

参考官方文档 https://docs.ollama.com/capabilities/tool-calling
"""

from ollama import chat

MODEL = "qwen3:8b"


# 第一步：准备工具。工具就是普通的 Python 函数。
# ollama 库会读函数名、参数类型和 docstring，自动转成模型看得懂的说明。
# 所以 docstring 要写清楚，模型就是靠它决定什么时候用哪个工具。
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


# 模型只会说“我要调用 add”，真正去执行的是我们的代码。
# 这个字典把工具名字对应到真正的函数。
available_functions = {
    "add": add,
    "multiply": multiply,
}


def run(question: str) -> str:
    # messages 是整段对话的记录。模型本身不记事，每次都要把全部记录发给它。
    messages = [
        {"role": "system", "content": "You are Tom, a friendly lizard assistant. Use the tools for any math."},
        {"role": "user", "content": question},
    ]

    # 第二步：agent 循环。
    # 模型要么直接回答，要么要求调用工具。
    # 要调用工具就执行，把结果塞回 messages，再问模型一次，直到它直接回答为止。
    step = 0
    while True:
        step += 1
        response = chat(model=MODEL, messages=messages, tools=[add, multiply], think=True)
        msg = response.message
        messages.append(msg)

        if msg.thinking:
            print(f"\n[第 {step} 轮] 模型在想：{msg.thinking.strip()[:200]}...")

        if not msg.tool_calls:
            return msg.content

        for tc in msg.tool_calls:
            name = tc.function.name
            args = tc.function.arguments
            fn = available_functions.get(name)
            result = fn(**args) if fn else f"unknown tool {name}"
            print(f"[第 {step} 轮] 模型要调用 {name}({args})，结果是 {result}")
            messages.append({"role": "tool", "tool_name": name, "content": str(result)})


if __name__ == "__main__":
    question = "What is (11434 + 12341) * 412?"
    print(f"问题：{question}")
    answer = run(question)
    print(f"\nTom 的回答：{answer}")
    print(f"\n正确答案：{(11434 + 12341) * 412}")
