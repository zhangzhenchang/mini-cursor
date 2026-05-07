# Mini Cursor CLI

一个基于 Python 和 LangChain 的 Mini Cursor 实现，能够自动执行文件操作、命令执行等任务。

## 功能特性

- 🤖 AI 驱动的任务执行
- 📁 文件读写操作
- 💻 命令执行（支持指定工作目录）
- 📂 目录列表查看
- 🔄 自动迭代直到任务完成

## 技术栈

- Python 3.10+
- LangChain 1.0
- OpenAI API (兼容 DashScope)
- uv (包管理)

## 快速开始

### 1. 安装依赖

使用 uv 安装依赖：

```bash
uv sync
```

### 2. 配置环境变量

`.env` 文件已存在，确保包含以下配置：

```env
OPENAI_API_KEY=your-api-key
OPENAI_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
MODEL_NAME=qwen-plus
```

**重要：** 使用 `qwen-plus` 模型以获得更好的工具调用支持。

### 3. 运行程序

```bash
# 运行主程序（创建 React TodoList 应用）
uv run python src/mini_cursor.py

# 运行快速测试
uv run python test_quick.py
```

## 项目结构

```
mini-cursor-cli/
├── src/
│   ├── __init__.py          # 包初始化
│   ├── tools.py             # 工具定义（文件操作、命令执行等）
│   └── mini_cursor.py       # 主程序入口
├── .env                     # 环境变量配置
├── pyproject.toml           # 项目配置和依赖
└── README.md                # 项目文档
```

## 工具说明

### read_file

读取指定路径的文件内容。

### write_file

向指定路径写入文件内容，自动创建目录。

### execute_command

执行系统命令，支持指定工作目录。

**重要提示**：使用 `working_directory` 参数时，不要在命令中使用 `cd`。

### list_directory

列出指定目录下的所有文件和文件夹。

## 开发指南

### 代码规范

项目遵循 Python 最佳实践：

- 使用类型注解
- 完整的文档字符串
- 清晰的变量命名
- 模块化设计

### 添加新工具

在 `src/tools.py` 中使用 `@tool` 装饰器定义新工具：

```python
@tool
def your_tool(param: str) -> str:
    """工具描述.

    Args:
        param: 参数描述

    Returns:
        返回值描述
    """
    # 实现逻辑
    pass
```

然后将工具添加到 `ALL_TOOLS` 列表中。

## 许可证

MIT
