"""快速测试脚本 - 验证 mini-cursor 功能."""
import asyncio
import os

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langchain_openai import ChatOpenAI

from src.tools import TOOLS

load_dotenv()


async def quick_test():
    """快速测试工具调用."""
    model = ChatOpenAI(
        model="qwen-plus",
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL"),
        temperature=0,
    )

    model_with_tools = model.bind_tools(TOOLS)

    messages = [
        SystemMessage("你是助手，使用工具完成任务。"),
        HumanMessage("列出当前目录，然后创建一个 test.txt 文件，内容为 'Test successful!'"),
    ]

    print("🧪 开始测试...\n")

    for i in range(5):
        print(f"⏳ 迭代 {i + 1}")
        response = await model_with_tools.ainvoke(messages)
        messages.append(response)

        if not response.tool_calls:
            print(f"\n✅ 测试完成: {response.content}\n")
            break

        for tool_call in response.tool_calls:
            tool = next((t for t in TOOLS if t.name == tool_call["name"]), None)
            if tool:
                result = await tool.ainvoke(tool_call["args"])
                messages.append(ToolMessage(content=result, tool_call_id=tool_call["id"]))


if __name__ == "__main__":
    asyncio.run(quick_test())
