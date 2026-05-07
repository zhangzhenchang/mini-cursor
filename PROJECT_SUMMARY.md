# Mini Cursor CLI - Python 版本

一个基于 Python 和 LangChain 的 AI 驱动项目管理助手，成功从 JavaScript 版本迁移而来。

## ✅ 完成状态

**项目已成功完成并测试通过！**

- ✅ 代码从 JavaScript 转换为 Python
- ✅ 使用 LangChain 1.0 最新 API
- ✅ 使用 uv 作为包管理器
- ✅ 遵循 Python 最佳工程实践
- ✅ 工具调用功能正常工作
- ✅ Agent 循环正确执行
- ✅ 成功创建并运行 React TodoList 应用

## 📁 项目结构

```
mini-cursor-cli/
├── src/
│   ├── __init__.py          # 包初始化
│   ├── tools.py             # 工具定义（4个工具）
│   └── mini_cursor.py       # 主程序（Agent 循环）
├── .env                     # 环境变量配置
├── .gitignore              # Git 忽略规则
├── pyproject.toml          # 项目配置（uv）
├── README.md               # 项目文档
└── react-todo-app/         # 测试生成的 React 应用 ✅
```

## 🛠️ 核心功能

### 工具 (src/tools.py)

1. **read_file** - 读取文件内容
2. **write_file** - 写入文件（自动创建目录）
3. **execute_command** - 执行系统命令（支持 working_directory）
4. **list_directory** - 列出目录内容

### Agent (src/mini_cursor.py)

- 异步实现，使用 `asyncio`
- 最多 30 次迭代循环
- 自动工具调用和结果处理
- 清晰的[REDACTED]

## 🎯 测试结果

### 测试 1: 简单任务 ✅
```bash
uv run python test_mini.py
```
- 成功列出目录
- 成功创建 hello.txt 文件
- Agent 正确完成任务

### 测试 2: 完整 React 应用 ✅
```bash
uv run python src/mini_cursor.py
```

**执行的操作：**
1. ✅ 创建 Vite + React + TypeScript 项目
2. ✅ 写入完整的 App.tsx（TodoList 功能）
   - 添加、删除、编辑、标记完成
   - 分类筛选（全部/进行中/已完成）
   - 统计信息显示
   - localStorage 数据持久化
3. ✅ 写入 App.css（美观样式）
   - 渐变背景（蓝到紫）
   - 卡片阴影、圆角
   - 悬停效果和动画
4. ✅ 列出目录确认
5. ✅ 安装依赖 (pnpm install)
6. ✅ 启动开发服务器 (pnpm run dev)

**结果：** 应用成功运行在 http://localhost:5176/

## 🔑 关键改进

### 相比原始代码的优化

1. **模型选择**
   - 使用 `qwen-plus` 而不是 `qwen-coder-turbo`
   - qwen-plus 对工具调用的支持更好

2. **代码简化**
   - 移除了不必要的 colorama 依赖
   - 简化了工具调用逻辑
   - 使用 `os.listdir` 而不是 `Path.iterdir()`

3. **类型注解**
   - 使用 Python 3.10+ 的 `str | None` 语法
   - 清晰的函数签名

## 📝 使用方法

### 安装依赖
```bash
uv sync
```

### 运行主程序
```bash
uv run python src/mini_cursor.py
```

### 自定义任务
编辑 `src/mini_cursor.py` 中的 `CASE1` 变量，定义你的任务。

## 🐛 调试经验

### 问题 1: 模型不调用工具
**原因：** qwen-coder-turbo 倾向于输出文本描述而不是调用工具  
**解决：** 切换到 qwen-plus 模型

### 问题 2: [REDACTED]过于复杂
**原因：** 过长的提示词让模型困惑  
**解决：** 简化提示词，保持核心规则

### 问��� 3: 工具调用验证
**方法：** 创建简单测试脚本验证工具调用是否工作

## 📦 依赖项

```toml
dependencies = [
    "langchain>=0.3.0",
    "langchain-openai>=0.2.0",
    "langchain-core>=0.3.0",
    "python-dotenv>=1.0.0",
]
```

## 🎓 Python 最佳实践

✅ 类型注解  
✅ 文档字符串  
✅ 异步编程  
✅ 模块化设计  
✅ 环境变量管理  
✅ 错误处理  
✅ 清晰的命名  

## �� 下一步

可以扩展的功能：
- 添加更多工具（git 操作、API 调用等）
- 支持多轮对话
- 添加日志记录
- 实现任务队列
- 添加单元测试

## 📄 许可证

MIT

---

**项目状态：** ✅ 完成并测试通过  
**最后更新：** 2026-05-07  
**测试环境：** macOS, Python 3.12, uv 包管理器
