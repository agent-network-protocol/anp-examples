# MCP Tool 使用指南

## 概述

MCP Tool是一个用于连接和交互MCP (Model Context Protocol) 服务器的工具，与ANP Tool并列提供智能代理间的通信能力。它支持多种传输方式，可以自动发现和调用MCP服务器提供的各种功能。

## 功能特性

- 🔌 **多传输方式支持**: SSE、stdio、streamable-http
- 🔍 **自动工具发现**: 自动列出MCP服务器提供的所有工具
- 🛠️ **工具调用**: 支持调用任何MCP工具并传递参数
- 📡 **智能配置解析**: 自动解析MCP服务器配置
- 🚀 **异步操作**: 完全异步支持，高性能

## 支持的传输方式

### 1. SSE (Server-Sent Events)
适用于HTTP-based的MCP服务器
```json
{
    "@type": "ad:StructuredInterface",
    "protocol": "MCP",
    "url": "https://mcp.amap.com/sse?key=YOUR_API_KEY",
    "transport": "sse"
}
```

### 2. Stdio
适用于本地命令行MCP服务器
```json
{
    "@type": "ad:StructuredInterface",
    "protocol": "MCP",
    "url": "stdio://amap-mcp-server",
    "transport": "stdio",
    "command": "uvx",
    "args": ["amap-mcp-server"],
    "env": {"AMAP_MAPS_API_KEY": "YOUR_API_KEY"}
}
```

### 3. Streamable HTTP
适用于标准HTTP API的MCP服务器
```json
{
    "@type": "ad:StructuredInterface",
    "protocol": "MCP",
    "url": "https://api.example.com/mcp",
    "transport": "streamable-http"
}
```

## 使用方法

### 基本使用

```python
from anp_examples.mcp_tool import MCPTool

# 初始化MCP Tool
mcp_tool = MCPTool()

# MCP服务器配置
config = {
    "@type": "ad:StructuredInterface",
    "protocol": "MCP",
    "url": "https://mcp.amap.com/sse?key=YOUR_API_KEY",
    "description": "AMAP MCP server"
}

# 1. 列出可用工具
result = await mcp_tool.execute(
    config=config,
    action="list_tools"
)

# 2. 调用特定工具
result = await mcp_tool.execute(
    config=config,
    action="call_tool",
    tool_name="maps_weather",
    tool_args={"city": "北京"}
)
```

### 在Agent中使用

当模型发现MCP服务器配置时，会自动使用mcp_tool：

```python
# 模型会自动识别这种配置并使用mcp_tool
{
    "name": "mcp_tool",
    "arguments": {
        "config": {
            "@type": "ad:StructuredInterface",
            "protocol": "MCP",
            "url": "https://mcp.amap.com/sse?key=YOUR_API_KEY"
        },
        "action": "list_tools"
    }
}
```

## MCP Tool参数说明

### config (必需)
MCP服务器配置对象：
- `@type`: 接口类型，通常为 "ad:StructuredInterface"
- `protocol`: 协议类型，必须为 "MCP"
- `url`: MCP服务器URL (必需)
- `transport`: 传输方式 ("sse"|"stdio"|"streamable-http")
- `description`: 服务器描述

### action (可选)
要执行的操作：
- `"list_tools"`: 列出可用工具 (默认)
- `"call_tool"`: 调用特定工具

### tool_name (调用工具时必需)
要调用的MCP工具名称

### tool_args (可选)
传递给MCP工具的参数对象

## 示例：高德地图MCP服务器

```python
# 高德地图MCP配置
amap_config = {
    "@type": "ad:StructuredInterface",
    "protocol": "MCP",
    "url": "https://mcp.amap.com/sse?key=YOUR_AMAP_KEY",
    "description": "AMAP MCP server for location services"
}

# 查看可用工具
tools_result = await mcp_tool.execute(
    config=amap_config,
    action="list_tools"
)

# 天气查询
weather_result = await mcp_tool.execute(
    config=amap_config,
    action="call_tool",
    tool_name="maps_weather",
    tool_args={"city": "北京"}
)

# 地理编码
geo_result = await mcp_tool.execute(
    config=amap_config,
    action="call_tool",
    tool_name="maps_geo",
    tool_args={"address": "北京市天安门广场"}
)

# POI搜索
search_result = await mcp_tool.execute(
    config=amap_config,
    action="call_tool",
    tool_name="maps_text_search",
    tool_args={"keywords": "咖啡厅", "city": "北京"}
)
```

## 错误处理

MCP Tool会自动处理各种错误情况：

```python
result = await mcp_tool.execute(config=config, action="list_tools")

if result["status"] == "success":
    # 成功情况
    tools = result["tools"]
    print(f"发现 {result['count']} 个工具")
else:
    # 错误情况
    error_msg = result["error"]
    print(f"连接失败: {error_msg}")
```

## 常见的MCP工具类型

### 地图服务
- `maps_weather`: 天气查询
- `maps_geo`: 地理编码（地址转坐标）
- `maps_regeo`: 逆地理编码（坐标转地址）
- `maps_text_search`: POI搜索
- `maps_around_search`: 周边搜索
- `maps_route_plan`: 路径规划

### 开发工具
- `code_search`: 代码搜索
- `file_edit`: 文件编辑
- `terminal_exec`: 终端执行

### 数据服务
- `database_query`: 数据库查询
- `api_call`: API调用
- `data_transform`: 数据转换

## 安装依赖

使用MCP Tool需要安装以下依赖：

```bash
pip install mcp aiohttp
```

对于特定的MCP服务器，可能需要额外的依赖：

```bash
# 对于AMAP MCP服务器
pip install uvx
uvx amap-mcp-server
```

## 运行测试

```bash
python test_mcp_tool.py
```

## 与ANP Tool的区别

| 特性 | ANP Tool | MCP Tool |
|------|----------|----------|
| 协议 | Agent Network Protocol | Model Context Protocol |
| 传输 | HTTP/HTTPS | SSE/stdio/HTTP |
| 认证 | DID Web Authentication | 服务器特定认证 |
| 用途 | 代理间通信 | 工具和服务调用 |
| 数据格式 | JSON-LD | JSON |

## 最佳实践

1. **先列出工具**: 总是先使用 `list_tools` 了解可用功能
2. **错误处理**: 检查 `status` 字段处理错误情况
3. **参数验证**: 确保传递正确的工具参数
4. **缓存会话**: 对于频繁调用，MCP Tool会自动缓存连接
5. **日志记录**: 启用日志以便调试连接问题

## 扩展和定制

MCP Tool支持扩展以添加新的传输方式或服务器特定的逻辑：

```python
class CustomMCPTool(MCPTool):
    async def _handle_custom_transport(self, config, action, tool_name, tool_args):
        # 实现自定义传输逻辑
        pass
``` 