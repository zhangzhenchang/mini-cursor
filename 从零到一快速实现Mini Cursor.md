# 从零到一快速实现 Mini Cursor 🚀

## 前言

你是不是经常在 Cursor 里这样操作：

- "帮我创建一个 React 项目"
- "修改这个文件，添加 xxx 功能"
- "安装依赖并启动服务"

然后 AI 就自动帮你完成了所有操作？✨

今天，我们就来揭秘 Cursor 的实现原理，并从零开始实现一个简易版的 Mini Cursor！

虽然我们不会做得那么完善，但核心功能是可以实现的。最终效果是：**AI 可以根据你的需求自动创建项目、读写文件、执行命令、安装依赖、启动服务，全程自己调用工具完成！**

## 一、核心原理：Tool Calling 🔧

Cursor 的核心能力来自于 **Tool Calling（工具调用）**。

简单来说：

- 我们给大模型提供一组工具（Tool）
- 大模型根据用户需求，自动决定调用哪个工具
- 工具执行完返回结果，大模型继续思考下一步
- 循环往复，直到任务完成

这就像给 AI 配备了"手"和"脚"，让它不仅能"说"，还能"做"！

## 二、需要哪些工具？🛠️

要实现类似 Cursor 的功能，我们至少需要这几个工具：

### 1. 文件操作工具

- **read_file**：读取文件内容
- **write_file**：写入文件内容（自动创建目录）

### 2. 目录操作工具

- **list_directory**：列出目录下的所有文件

### 3. 命令执行工具

- **execute_command**：执行系统命令（支持指定工作目录）

有了这些工具，AI 就能像人类开发者一样操作项目了！

## 三、技术选型 📚

我们使用以下技术栈：

- **Python 3.10+**：主要编程语言
- **LangChain**：AI 应用开发框架，提供工具调用能力
- **OpenAI API**：大模型接口（兼容阿里云 DashScope）
- **uv**：现代化的 Python 包管理工具

## 四、开始实现 💻

### 4.1 项目初始化

首先创建项目结构：

```
mini-cursor-cli/
├── src/
│   ├── __init__.py          # 包初始化
│   ├── tools.py             # 工具定义
│   └── mini_cursor.py       # 主程序
├── .env                     # 环境变量
└── pyproject.toml           # 项目配置
```

### 4.2 实现工具集 - tools.py

这是核心部分！我们需要实现四个工具：

#### 1️⃣ 读取文件工具

```python
@tool
def read_file(file_path: str) -> str:
    """读取指定路径的文件内容"""
    try:
        content = Path(file_path).read_text(encoding="utf-8")
        print(f'  [工具调用] read_file("{file_path}") - 成功读取 {len(content)} 字节')
        return f"文件内容:\n{content}"
    except Exception as exc:
        print(f'  [工具调用] read_file("{file_path}") - 错误: {exc}')
        return f"读取文件失败: {exc}"
```

**关键点**：

- 使用 `@tool` 装饰器，LangChain 会自动将其转换为可调用的工具
- 返回详细的执行结果，让 AI 知道操作是否成功
- 异常处理很重要，避免程序崩溃

#### 2️⃣ 写入文件工具

```python
@tool
def write_file(file_path: str, content: str) -> str:
    """向指定路径写入文件内容，自动创建目录"""
    try:
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)  # 自动创建父目录
        path.write_text(content, encoding="utf-8")
        print(f'  [工具调用] write_file("{file_path}") - 成功写入 {len(content)} 字节')
        return f"文件写入成功: {file_path}"
    except Exception as exc:
        print(f'  [工具调用] write_file("{file_path}") - 错误: {exc}')
        return f"写入文件失败: {exc}"
```

**亮点**：

- `mkdir(parents=True, exist_ok=True)` 自动创建多级目录
- 这样 AI 就不需要先创建目录再写文件了

#### 3️⃣ 列出目录工具

```python
@tool
def list_directory(directory_path: str) -> str:
    """列出指定目录下的所有文件和文件夹"""
    try:
        files = os.listdir(directory_path)
        print(f'  [工具调用] list_directory("{directory_path}") - 找到 {len(files)} 个项目')
        return "目录内容:\n" + "\n".join(f"- {name}" for name in files)
    except Exception as exc:
        print(f'  [工具调用] list_directory("{directory_path}") - 错误: {exc}')
        return f"列出目录失败: {exc}"
```

#### 4️⃣ 执行命令工具（重点！）

```python
@tool
def execute_command(command: str, working_directory: str | None = None) -> str:
    """执行系统命令，支持指定工作目录，实时显示输出"""
    cwd = working_directory or os.getcwd()
    print(f'  [工具调用] execute_command("{command}") - 工作目录: {cwd}')

    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,  # 指定工作目录
            capture_output=False,  # 实时输出到控制台
            text=True,
        )

        if result.returncode == 0:
            print(f'  [工具调用] execute_command("{command}") - 执行成功')
            cwd_info = ""
            if working_directory:
                cwd_info = (
                    f'\n\n重要提示：命令在目录 "{working_directory}" 中执行成功。'
                    "如果需要在这个项目目录中继续执行命令，请继续传入 working_directory 参数。"
                )
            return f"命令执行成功: {command}{cwd_info}"

        print(f'  [工具调用] execute_command("{command}") - 执行失败，退出码: {result.returncode}')
        return f"命令执行失败，退出码: {result.returncode}"
    except Exception as exc:
        print(f'  [工具调用] execute_command("{command}") - 错误: {exc}')
        return f"执行命令出错: {exc}"
```

**核心设计**：

- `working_directory` 参数：避免使用 `cd` 命令切换目录
- `capture_output=False`：让命令输出实时显示在控制台
- 返回提示信息：告诉 AI 继续在该目录执行命令时要传 `working_directory`

**为什么不用 cd？**

❌ 错误示例：

```python
command="cd react-todo-app && pnpm install"
working_directory="react-todo-app"
```

这会导致找不到目录！因为已经在 `react-todo-app` 里了，再 `cd react-todo-app` 就错了。

✅ 正确示例：

```python
command="pnpm install"
working_directory="react-todo-app"
```

### 4.3 实现 Agent 主程序 - mini_cursor.py

现在我们要把工具和大模型连接起来：

```python
import asyncio
import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langchain_openai import ChatOpenAI
from tools import TOOLS

load_dotenv()

# 初始化大模型
model = ChatOpenAI(
    model=os.getenv("MODEL_NAME", "qwen-plus"),
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL"),
    temperature=0,  # 温度设为 0，让 AI 更稳定
)

async def run_agent_with_tools(query: str, max_iterations: int = 30) -> str:
    """运行 AI Agent 并使用工具完成任务"""

    # 绑定工具到模型
    model_with_tools = model.bind_tools(TOOLS)

    # 初始化对话消息
    messages = [
        SystemMessage(
            f"""你是一个项目管理助手，使用工具完成任务。

当前工作目录: {os.getcwd()}

工具：
1. read_file: 读取文件
2. write_file: 写入文件
3. execute_command: 执行命令（支持 working_directory 参数）
4. list_directory: 列出目录

重要规则 - execute_command：
- working_directory 参数会自动切换到指定目录
- 当使用 working_directory 时，绝对不要在 command 中使用 cd
- 错误示例: command="cd react-todo-app && pnpm install", working_directory="react-todo-app"
- 正确示例: command="pnpm install", working_directory="react-todo-app"

重要规则 - write_file：
- 当写入 React 组件文件（如 App.tsx）时，如果存在对应的 CSS 文件（如 App.css），在其他 import 语句后加上这个 css 的导入
"""
        ),
        HumanMessage(query),
    ]

    # 开始迭代执行
    for i in range(max_iterations):
        print(f"\n⏳ 正在等待 AI 思考... (第 {i + 1} 次)")

        # 调用大模型
        response = await model_with_tools.ainvoke(messages)
        messages.append(response)

        # 如果没有工具调用，说明任务完成
        if not response.tool_calls:
            print(f"\n✨ AI 最终回复:\n{response.content}\n")
            return str(response.content)

        # 执行工具调用
        for tool_call in response.tool_calls:
            found_tool = next((tool for tool in TOOLS if tool.name == tool_call["name"]), None)
            if found_tool is None:
                continue

            # 调用工具
            tool_result = await found_tool.ainvoke(tool_call["args"])

            # 将工具结果添加到消息历史
            messages.append(
                ToolMessage(
                    content=(
                        tool_result
                        if isinstance(tool_result, str)
                        else getattr(tool_result, "text", str(tool_result))
                    ),
                    tool_call_id=tool_call["id"],
                )
            )

    return str(messages[-1].content)
```

**核心流程**：

1. **初始化对话**：用 `SystemMessage` 告诉 AI 它的角色和可用工具
2. **循环执行**：
   - 调用大模型，获取响应
   - 如果有工具调用，执行工具
   - 将工具结果返回给大模型
   - 继续下一轮思考
3. **终止条件**：大模型不再调用工具，或达到最大迭代次数

### 4.4 定义测试任务

让我们给 AI 一个复杂的任务：

```python
CASE1 = """创建一个功能丰富的 React TodoList 应用：

1. 创建项目：pnpm create vite react-todo-app --template react-ts
2. 修改 src/App.tsx，实现完整功能的 TodoList：
 - 添加、删除、编辑、标记完成
 - 分类筛选（全部/进行中/已完成）
 - 统计信息显示
 - localStorage 数据持久化
3. 添加复杂样式：
 - 渐变背景（蓝到紫）
 - 卡片阴影、圆角
 - 悬停效果
4. 添加动画：
 - 添加/删除时的过渡动画
 - 使用 CSS transitions
5. 列出目录确认

注意：使用 pnpm，功能要完整，样式要美观，要有动画效果

之后在 react-todo-app 项目中：
1. 使用 pnpm install 安装依赖
2. 使用 pnpm run dev 启动服务器
"""

async def main():
    """主函数 - 程序入口"""
    try:
        await run_agent_with_tools(CASE1)
    except Exception as exc:
        print(f"\n❌ 错误: {exc}\n")

if __name__ == "__main__":
    asyncio.run(main())
```

## 五、运行效果 🎉

配置好环境变量后，运行：

```bash
uv run python src/mini_cursor.py
```

你会看到 AI 自动执行以下操作：

1. ✅ 调用 `execute_command` 创建 Vite 项目
2. ✅ 调用 `write_file` 写入 `App.tsx` 代码
3. ✅ 调用 `write_file` 写入 `App.css` 样式
4. ✅ 调用 `list_directory` 确认目录结构
5. ✅ 调用 `execute_command` 安装依赖（`pnpm install`）
6. ✅ 调用 `execute_command` 启动开发服务器（`pnpm run dev`）

整个过程完全自动化，你只需要等待！🚀

控制台会实时显示：

```
⏳ 正在等待 AI 思考... (第 1 次)
  [工具调用] execute_command("pnpm create vite react-todo-app --template react-ts") - 工作目录: /xxx
  [工具调用] execute_command("pnpm create vite react-todo-app --template react-ts") - 执行成功

⏳ 正在等待 AI 思考... (第 2 次)
  [工具调用] write_file("react-todo-app/src/App.tsx") - 成功写入 3245 字节

⏳ 正在等待 AI 思考... (第 3 次)
  [工具调用] execute_command("pnpm install") - 工作目录: react-todo-app
  ...
```

## 六、关键技术点总结 📝

### 6.1 Tool Calling 的本质

Tool Calling 不是魔法，它的原理是：

1. **工具描述**：我们用 `@tool` 装饰器定义工具，LangChain 会自动生成工具的 JSON Schema 描述
2. **发送给大模型**：大模型看到工具描述后，知道有哪些工具可用
3. **大模型决策**：根据用户需求，大模型决定调用哪个工具，并生成参数
4. **我们执行**：我们拿到工具调用请求，执行真正的操作
5. **返回结果**：把执行结果返回给大模型，它继续思考

### 6.2 为什么要用 working_directory？

如果不用 `working_directory`，AI 可能会这样做：

```bash
cd react-todo-app && pnpm install
cd react-todo-app && pnpm run dev
```

这样有两个问题：

1. 每次都要 `cd`，很繁琐
2. 容易出错（目录嵌套、路径错误等）

使用 `working_directory` 后：

```python
execute_command("pnpm install", working_directory="react-todo-app")
execute_command("pnpm run dev", working_directory="react-todo-app")
```

清晰、简洁、不易出错！

### 6.3 为什么 temperature=0？

`temperature` 控制大模型的"创造性"：

- `temperature=0`：输出最确定，适合工具调用
- `temperature=1`：输出更随机，适合创意写作

对于 Mini Cursor 这种需要精确执行的场景，我们希望 AI 稳定、可预测，所以设为 0。

### 6.4 为什么要限制 max_iterations？

防止 AI 陷入死循环！

比如 AI 可能会：

- 反复调用同一个工具
- 不断尝试错误的操作

设置 `max_iterations=30`，最多执行 30 轮，避免无限循环。

## 七、与 Cursor 的差距 🤔

我们的 Mini Cursor 还很简陋，和真正的 Cursor 相比：

| 功能     | Mini Cursor | Cursor             |
| -------- | ----------- | ------------------ |
| 工具数量 | 4 个        | 几十个             |
| 代码理解 | 基础        | 深度理解上下文     |
| 错误处理 | 简单        | 智能重试、自动修复 |
| 用户体验 | 命令行      | 图形界面、实时预览 |
| 性能优化 | 无          | 流式输出、增量更新 |

但核心原理是一样的：**Tool Calling + 大模型 = AI 编程助手**！

## 八、可以做哪些扩展？🌟

基于这个框架，你可以：

### 1. 添加更多工具

- Git 操作（commit、push、pull）
- 数据库操作（查询、更新）
- API 调用（发送 HTTP 请求）
- 代码分析（AST 解析、代码搜索）

### 2. 优化用户体验

- 流式输出：实时显示 AI 的思考过程
- 进度条：显示任务执行进度
- 错误重试：自动重试失败的操作

### 3. 增强 AI 能力

- 使用更强的模型（GPT-4、Claude）
- 添加记忆功能（记住用户偏好）
- 多轮对话优化（更好的上下文理解）

### 4. 安全性增强

- 命令白名单：只允许执行安全的命令
- 文件权限检查：防止误删重要文件
- 操作确认：危险操作需要用户确认

## 九、环境配置 ⚙️

### 安装依赖

```bash
# 使用 uv 安装依赖
uv sync
```

### 配置 .env

```env
OPENAI_API_KEY=your-api-key
OPENAI_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
MODEL_NAME=qwen-plus
```

**重要**：推荐使用 `qwen-plus` 模型，它对工具调用的支持更好！

## 十、总结 🎯

通过这个项目，我们学到了：

1. **Tool Calling 的原理**：大模型 + 工具 = 强大的 AI Agent
2. **如何设计工具**：清晰的接口、完善的错误处理
3. **如何构建 Agent**：消息循环、工具执行、结果反馈
4. **实践经验**：
   - 用 `working_directory` 而不是 `cd`
   - 设置 `temperature=0` 保证稳定性
   - 限制 `max_iterations` 防止死循环
   - 详细的提示词很重要

虽然我们的 Mini Cursor 还很简单，但它已经具备了 AI 编程助手的核心能力！

你可以在这个基础上继续扩展，添加更多工具，优化用户体验，甚至做出自己的 AI 编程助手！

**AI 时代，每个开发者都应该学会构建自己的 AI 工具！** 💪

---

## 项目地址

完整代码已上传：[GitHub - mini-cursor](https://github.com/zhangzhenchang/mini-cursor)

如果觉得有帮助，欢迎 Star ⭐️

---

## 参考资料

- [LangChain 官方文档](https://python.langchain.com/)
- [OpenAI Tool Calling 文档](https://platform.openai.com/docs/guides/function-calling)
- [阿里云 DashScope 文档](https://help.aliyun.com/zh/dashscope/)

---

**觉得有收获的话，点个赞再走吧！👍**
