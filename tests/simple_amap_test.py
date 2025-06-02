#!/usr/bin/env python3
"""
简化版高德地图MCP Server测试程序
测试基本的连接和工具调用功能
"""

import os
import asyncio
import json
import subprocess
import sys
from pathlib import Path
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def check_amap_key():
    """检查高德API Key是否配置"""
    amap_key = os.getenv('AMAP_KEY')
    if not amap_key:
        print("❌ 错误: 未找到AMAP_KEY环境变量")
        print("请在项目根目录的.env文件中设置:")
        print('AMAP_KEY="你的高德地图API密钥"')
        return None
    
    print(f"✅ 找到高德API Key: {amap_key[:8]}****")
    return amap_key

def check_dependencies():
    """检查必要的依赖"""
    print("🔍 检查依赖...")
    
    # 检查是否安装了mcp
    try:
        import mcp
        print("✅ MCP SDK 已安装")
    except ImportError:
        print("❌ 缺少 MCP SDK")
        print("请安装: pip install mcp")
        return False
    
    # 检查uvx是否可用
    try:
        result = subprocess.run(['uvx', '--version'], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ uvx 可用")
        else:
            print("❌ uvx 不可用，尝试安装 uv: pip install uv")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("❌ uvx 命令未找到，请安装 uv: pip install uv")
        return False
    
    return True

async def test_mcp_server():
    """测试MCP服务器连接"""
    amap_key = check_amap_key()
    if not amap_key:
        return False
    
    if not check_dependencies():
        return False
    
    try:
        from mcp import ClientSession, StdioServerParameters
        from mcp.client.stdio import stdio_client
        
        print("\n🚀 启动高德MCP服务器...")
        
        # 配置服务器参数
        server_params = StdioServerParameters(
            command="uvx",
            args=["amap-mcp-server"],
            env={"AMAP_MAPS_API_KEY": amap_key}
        )
        
        print("📡 连接到MCP服务器...")
        
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # 初始化会话
                print("🔄 初始化会话...")
                await session.initialize()
                print("✅ 会话初始化成功")
                
                # 获取服务器信息
                try:
                    server_info = await session.get_server_info()
                    print(f"📋 服务器信息: {server_info.name} v{server_info.version}")
                except Exception as e:
                    print(f"⚠️  无法获取服务器信息: {e}")
                
                # 列出可用工具
                print("📝 获取可用工具列表...")
                tools_result = await session.list_tools()
                tools = tools_result.tools
                
                print(f"✅ 发现 {len(tools)} 个可用工具:")
                for i, tool in enumerate(tools, 1):
                    print(f"  {i}. {tool.name}")
                    if hasattr(tool, 'description') and tool.description:
                        print(f"     描述: {tool.description}")
                
                # 测试几个基本工具
                await test_basic_tools(session, tools)
                
                return True
                
    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        print("请确保安装了正确的MCP SDK版本")
        return False
    except Exception as e:
        print(f"❌ 连接失败: {e}")
        return False

async def test_basic_tools(session, tools):
    """测试基本工具"""
    print("\n🧪 开始工具测试...")
    
    # 创建工具名称映射
    tool_map = {tool.name: tool for tool in tools}
    
    # 定义测试用例
    test_cases = [
        {
            "tool_name": "maps_weather",
            "description": "天气查询",
            "args": {"city": "北京"},
            "expected_keys": ["weather", "temperature", "city"]
        },
        {
            "tool_name": "maps_geo",
            "description": "地理编码",
            "args": {"address": "北京市天安门广场"},
            "expected_keys": ["location", "geocodes"]
        },
        {
            "tool_name": "maps_text_search",
            "description": "地点搜索",
            "args": {"keywords": "咖啡厅", "city": "北京"},
            "expected_keys": ["pois", "count"]
        }
    ]
    
    successful_tests = 0
    
    for test_case in test_cases:
        tool_name = test_case["tool_name"]
        description = test_case["description"]
        args = test_case["args"]
        
        if tool_name not in tool_map:
            print(f"⚠️  工具 '{tool_name}' 不可用，跳过 {description} 测试")
            continue
        
        try:
            print(f"\n🔬 测试 {description} ({tool_name})...")
            print(f"   参数: {json.dumps(args, ensure_ascii=False)}")
            
            # 调用工具
            result = await session.call_tool(tool_name, args)
            
            if hasattr(result, 'content') and result.content:
                print(f"✅ {description} 测试成功!")
                
                # 显示结果摘要
                for content_item in result.content:
                    if hasattr(content_item, 'text'):
                        try:
                            data = json.loads(content_item.text)
                            print(f"   📊 返回数据类型: {type(data).__name__}")
                            if isinstance(data, dict):
                                print(f"   📋 数据字段: {list(data.keys())}")
                            elif isinstance(data, list) and data:
                                print(f"   📋 列表长度: {len(data)}")
                                if isinstance(data[0], dict):
                                    print(f"   📋 首项字段: {list(data[0].keys())}")
                        except json.JSONDecodeError:
                            print(f"   📝 返回文本长度: {len(content_item.text)} 字符")
                
                successful_tests += 1
            else:
                print(f"⚠️  {description} 测试返回空结果")
                
        except Exception as e:
            print(f"❌ {description} 测试失败: {e}")
    
    print(f"\n📊 测试总结: {successful_tests}/{len(test_cases)} 个测试成功")

def install_dependencies():
    """安装必要的依赖"""
    print("📦 安装必要的依赖...")
    
    dependencies = [
        "python-dotenv",
        "mcp",
        "uv"
    ]
    
    for dep in dependencies:
        try:
            print(f"安装 {dep}...")
            subprocess.run([sys.executable, "-m", "pip", "install", dep], 
                         check=True, capture_output=True)
            print(f"✅ {dep} 安装成功")
        except subprocess.CalledProcessError as e:
            print(f"❌ {dep} 安装失败: {e}")
            return False
    
    return True

def main():
    """主函数"""
    print("🚀 高德地图MCP服务器测试程序")
    print("=" * 50)
    
    # 检查并安装依赖
    try:
        import mcp
        from dotenv import load_dotenv
    except ImportError:
        print("🔧 检测到缺少依赖，尝试自动安装...")
        if not install_dependencies():
            print("❌ 依赖安装失败，请手动安装:")
            print("pip install python-dotenv mcp uv")
            return
        
        # 重新导入
        try:
            import mcp
            from dotenv import load_dotenv
        except ImportError:
            print("❌ 依赖安装后仍无法导入，请检查Python环境")
            return
    
    # 运行测试
    try:
        result = asyncio.run(test_mcp_server())
        if result:
            print("\n🎉 所有测试完成!")
        else:
            print("\n❌ 测试失败，请检查配置")
    except KeyboardInterrupt:
        print("\n⏹️  测试被用户中断")
    except Exception as e:
        print(f"\n❌ 测试过程中发生未预期的错误: {e}")

if __name__ == "__main__":
    main() 