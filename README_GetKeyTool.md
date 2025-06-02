# GetKeyTool 使用指南

## 概述

GetKeyTool 是一个简单高效的通用API密钥获取工具，专门从项目根目录的 `.env` 文件中读取配置的环境变量。工具会自动定位项目根目录，无需手动指定文件路径。

## 功能特性

- 🔑 **简单易用**: 只需要指定密钥名称即可获取
- 📍 **自动定位**: 自动查找项目根目录下的 `.env` 文件
- 🛡️ **隐私保护**: 自动遮蔽密钥以保护隐私
- ⚡ **高效可靠**: 专注功能，性能优异
- 🔧 **通用性强**: 可获取任何类型的API密钥

## 基本用法

### Python代码中使用

```python
from anp_examples.get_key_tool import GetKeyTool

# 初始化工具（自动定位项目根目录）
tool = GetKeyTool()

# 获取AMAP_KEY
result = await tool.execute(key_name="AMAP_KEY")

if result["status"] == "success":
    api_key = result["api_key"]
    print(f"获取到密钥: {result['masked_key']}")
    print(f"项目根目录: {result['project_root']}")
else:
    print(f"获取失败: {result['error']}")
```

### Agent中使用

当模型需要获取API密钥时，会自动调用此工具：

```python
# 模型会生成这样的工具调用
{
    "name": "get_key_tool",
    "arguments": {
        "key_name": "AMAP_KEY"
    }
}
```

## 参数说明

### key_name (必需)
要获取的环境变量名称
- 类型: `string`
- 默认值: `"AMAP_KEY"`
- 示例: `"AMAP_KEY"`, `"OPENAI_API_KEY"`, `"ANTHROPIC_API_KEY"`

## 自动路径检测

工具会自动执行以下步骤来定位 `.env` 文件：

1. **向上搜索**: 从当前文件位置开始，向上遍历目录
2. **查找.env**: 寻找包含 `.env` 文件的目录
3. **设为根目录**: 将找到的目录设为项目根目录
4. **备选方案**: 如果未找到，使用当前文件的父目录的父目录

## 使用示例

### 1. 获取AMAP密钥

```python
# 获取AMAP_KEY（默认）
result = await tool.execute(key_name="AMAP_KEY")

# 使用默认参数的简化调用
result = await tool.execute()
```

### 2. 获取其他API密钥

```python
# 获取OpenAI API密钥
result = await tool.execute(key_name="OPENAI_API_KEY")

# 获取阿里云API密钥
result = await tool.execute(key_name="DASHSCOPE_API_KEY")
```

### 3. 检查项目路径

```python
tool = GetKeyTool()
print(f"项目根目录: {tool.project_root}")
print(f".env文件路径: {tool.env_file_path}")
```

## 返回格式

### 成功响应
```json
{
    "status": "success",
    "key_name": "AMAP_KEY",
    "api_key": "actual_api_key_value",
    "masked_key": "9d71************************7bb3",
    "env_file": "/path/to/project/.env",
    "project_root": "/path/to/project",
    "message": "成功从项目根目录的.env文件获取AMAP_KEY"
}
```

### 失败响应
```json
{
    "error": "在.env文件中未找到环境变量: AMAP_KEY",
    "status": "error",
    "key_name": "AMAP_KEY",
    "env_file": "/path/to/project/.env",
    "project_root": "/path/to/project",
    "suggestion": "请在/path/to/project/.env文件中添加: AMAP_KEY=your_api_key"
}
```

## .env 文件配置

在项目根目录创建 `.env` 文件：

```bash
# 高德地图API密钥
AMAP_KEY=your_amap_api_key_here

# OpenAI API密钥
OPENAI_API_KEY=your_openai_key_here

# 其他API密钥
DASHSCOPE_API_KEY=your_dashscope_key
ANTHROPIC_API_KEY=your_anthropic_key
```

## 项目结构示例

```
your_project/
├── .env                    # 配置文件（自动检测）
├── anp_examples/
│   ├── get_key_tool.py    # 工具文件
│   └── simple_example.py  # 使用示例
└── test_get_key_tool.py   # 测试文件
```

## 常见使用场景

### 1. 地图服务
```python
# 获取高德地图密钥
result = await tool.execute(key_name="AMAP_KEY")
```

### 2. AI服务
```python
# 获取AI服务密钥
openai_result = await tool.execute(key_name="OPENAI_API_KEY")
dashscope_result = await tool.execute(key_name="DASHSCOPE_API_KEY")
```

### 3. 第三方服务
```python
# 获取其他第三方服务密钥
result = await tool.execute(key_name="YOUR_SERVICE_API_KEY")
```

## 错误处理

```python
result = await tool.execute(key_name="AMAP_KEY")

if result["status"] == "success":
    # 成功获取密钥
    api_key = result["api_key"]
    masked_key = result["masked_key"]
    project_root = result["project_root"]
    print(f"获取成功: {masked_key}")
    print(f"项目根目录: {project_root}")
else:
    # 处理错误
    error_msg = result["error"]
    suggestion = result.get("suggestion", "")
    print(f"获取失败: {error_msg}")
    if suggestion:
        print(f"建议: {suggestion}")
```

## 测试

运行测试程序：

```bash
python test_get_key_tool.py
```

测试内容包括：
- 自动项目根目录检测
- 从 `.env` 文件获取各种密钥
- 错误情况处理
- 路径检测验证

## 最佳实践

1. **项目结构**: 确保 `.env` 文件在项目根目录
2. **环境变量命名**: 使用清晰的命名规范，如 `SERVICE_API_KEY`
3. **文件安全**: 确保 `.env` 文件不被提交到版本控制系统
4. **错误处理**: 始终检查返回状态并处理失败情况
5. **密钥保护**: 利用工具提供的 `masked_key` 字段进行日志记录

## 与其他工具的集成

GetKeyTool 与 ANP Tool 和 MCP Tool 完美配合：

```python
# 1. 获取API密钥（自动定位.env文件）
key_result = await get_key_tool.execute(key_name="AMAP_KEY")

# 2. 使用密钥配置MCP服务器
if key_result["status"] == "success":
    mcp_config = {
        "@type": "ad:StructuredInterface",
        "protocol": "MCP",
        "url": f"https://mcp.amap.com/sse?key={key_result['api_key']}"
    }
    
    # 3. 连接MCP服务器
    mcp_result = await mcp_tool.execute(config=mcp_config, action="list_tools")
```

## 故障排除

### 问题：找不到.env文件
- **解决方案**: 确保 `.env` 文件在项目根目录
- **检查方法**: 运行测试查看检测到的路径

### 问题：找不到指定的密钥
- **解决方案**: 检查 `.env` 文件中是否包含该环境变量
- **格式**: `KEY_NAME=value`（无空格）

### 问题：路径检测不正确
- **解决方案**: 确保项目结构符合预期，或检查文件权限

这种简化的设计让工具更加可靠和易用，用户无需关心文件路径配置。 