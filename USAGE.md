# Mini Cursor CLI - 使用指南

## 快速开始

### 1. 安装依赖
```bash
uv sync
```

### 2. 运行测试
```bash
# 快速测试（创建 test.txt）
uv run python test_quick.py

# 完整测试（创建 React TodoList 应用）
uv run python src/mini_cursor.py
```

## 自定义任务

编辑 `src/mini_cursor.py` 中的 `CASE1` 变量：

```python
CASE1 = """你的任务描述：
1. 第一步
2. 第二步
3. 第三步
"""
```

## 可用工具

1. **read_file** - 读取文件
   ```python
   read_file(file_path="path/to/file.txt")
   ```

2. **write_file** - 写入文件
   ```python
   write_file(file_path="path/to/file.txt", content="内容")
   ```

3. **execute_command** - 执行命令
   ```python
   execute_command(command="ls -la", working_directory="./project")
   ```

4. **list_directory** - 列出目录
   ```python
   list_directory(directory_path="./")
   ```

## 注意事项

- 使用 `qwen-plus` 模型（工具调用更可靠）
- `execute_command` 使用 `working_directory` 时不要在 `command` 中使用 `cd`
- 所有操作都是异步的

## 故障排除

### 模型不调用工具
确保 `.env` 中使用 `MODEL_NAME=qwen-plus`

### 导入错误
确保使用 `uv run` 而不是直接 `python`

### 工具调用失败
检查工具参数是否正确，查看控制台输出
