# 高德地图MCP Server测试程序

这个项目提供了一个简单的测试程序来验证高德地图MCP Server的功能。

## 🎯 功能特性

- ✅ 支持stdio和SSE两种连接方式
- ✅ 自动检测和安装依赖
- ✅ 测试多种高德地图API功能
- ✅ 详细的错误诊断和日志输出
- ✅ 从`.env`文件安全读取API密钥

## 📋 支持的功能测试

- 🌤️ 天气查询 (`maps_weather`)
- 📍 地理编码 (`maps_geo`) 
- 🔄 逆地理编码 (`maps_regeocode`)
- 🔍 关键词搜索 (`maps_text_search`)
- 📍 周边搜索 (`maps_around_search`)
- 🚶 步行路径规划 (`maps_direction_walking_by_address`)

## 🚀 快速开始

### 1. 准备环境

确保您有以下环境：
- Python 3.8+
- pip包管理器

### 2. 获取高德API密钥

1. 访问 [高德开放平台](https://console.amap.com/dev/key/app)
2. 注册账号并创建应用
3. 获取您的API Key

### 3. 配置环境变量

在项目根目录创建`.env`文件：

```bash
# 高德地图API密钥
AMAP_KEY="你的高德地图API密钥"
```

### 4. 安装依赖

运行依赖安装脚本：

```bash
python install_mcp_deps.py
```

或手动安装：

```bash
pip install python-dotenv mcp uv
```

### 5. 运行测试

```bash
python simple_amap_test.py
```

## 📖 使用说明

### 基本测试程序

`simple_amap_test.py` 是一个简化的测试程序，包含以下功能：

- **自动检测依赖**：检查必要的Python包和系统工具
- **连接测试**：测试与高德MCP服务器的连接
- **工具列表**：获取并显示所有可用的MCP工具
- **功能测试**：自动测试常用的高德地图API功能

### 高级测试程序

`test_amap_mcp.py` 是一个功能更完整的测试程序，支持：

- **多种连接方式**：stdio和SSE连接
- **交互式测试**：手动选择和测试特定工具
- **详细日志**：完整的调试信息和错误诊断

## 🔧 故障排除

### 常见问题

1. **AMAP_KEY未找到**
   ```
   ❌ 错误: 未找到AMAP_KEY环境变量
   ```
   解决：确保`.env`文件存在且包含正确的API密钥

2. **MCP SDK缺失**
   ```
   ❌ 缺少 MCP SDK
   ```
   解决：运行 `pip install mcp`

3. **uvx命令未找到**
   ```
   ❌ uvx 命令未找到
   ```
   解决：运行 `pip install uv`

4. **连接超时**
   ```
   ❌ 连接失败: 超时
   ```
   解决：检查网络连接，或使用SSE连接方式

### 调试模式

如果需要更详细的调试信息，可以修改测试程序中的日志级别：

```python
logging.basicConfig(level=logging.DEBUG)
```

## 📚 API文档参考

- [高德MCP Server官方文档](https://lbs.amap.com/api/mcp-server/gettingstarted)
- [高德开放平台API文档](https://lbs.amap.com/api/)
- [MCP协议规范](https://modelcontextprotocol.io/)

## 🔗 相关链接

- [高德MCP Server GitHub](https://github.com/sugarforever/amap-mcp-server)
- [高德开放平台](https://lbs.amap.com/)
- [MCP协议官网](https://modelcontextprotocol.io/)

## 📝 示例输出

```bash
🚀 高德地图MCP服务器测试程序
==================================================
✅ 找到高德API Key: f1a2b3c4****
🔍 检查依赖...
✅ MCP SDK 已安装
✅ uvx 可用

🚀 启动高德MCP服务器...
📡 连接到MCP服务器...
🔄 初始化会话...
✅ 会话初始化成功
📋 服务器信息: amap-mcp-server v1.0.0
📝 获取可用工具列表...
✅ 发现 15 个可用工具:
  1. maps_weather
     描述: 根据城市名称查询天气
  2. maps_geo
     描述: 地理编码服务
  ...

🧪 开始工具测试...

🔬 测试 天气查询 (maps_weather)...
   参数: {"city": "北京"}
✅ 天气查询 测试成功!
   📊 返回数据类型: dict
   📋 数据字段: ['status', 'count', 'info', 'lives']

📊 测试总结: 3/3 个测试成功

🎉 所有测试完成!
```

## 📄 许可证

本项目遵循 MIT 许可证。详见 LICENSE 文件。 