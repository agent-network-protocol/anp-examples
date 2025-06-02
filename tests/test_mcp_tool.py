#!/usr/bin/env python3
"""
MCP Tool测试程序
测试MCP Tool连接高德地图MCP服务器的功能
"""

import asyncio
import json
import logging
from anp_examples.mcp_tool import MCPTool

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def test_mcp_tool():
    """测试MCP Tool功能"""
    
    # 初始化MCP Tool
    mcp_tool = MCPTool()
    
    # 高德地图MCP服务器配置（SSE方式）
    amap_config = {
        "@type": "ad:StructuredInterface",
        "protocol": "MCP",
        "url": "https://mcp.amap.com/sse?key=9d71135d3572ddc6dc18d350bd587bb3",
        "description": "AMAP MCP server for location services",
        "transport": "sse"
    }
    
    print("🚀 开始测试MCP Tool功能")
    print("=" * 50)
    
    # 测试1: 列出可用工具
    print("\n📝 测试1: 列出高德MCP服务器的可用工具")
    try:
        result = await mcp_tool.execute(
            config=amap_config,
            action="list_tools"
        )
        
        if result["status"] == "success":
            print(f"✅ 成功连接，发现 {result['count']} 个工具:")
            for i, tool in enumerate(result["tools"], 1):
                print(f"  {i}. {tool['name']}")
                if len(tool.get('description', '')) > 100:
                    print(f"     描述: {tool['description'][:100]}...")
                else:
                    print(f"     描述: {tool.get('description', 'No description')}")
        else:
            print(f"❌ 连接失败: {result.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ 测试1失败: {e}")
        return False
    
    # 测试2: 调用天气查询工具
    print("\n🌤️ 测试2: 调用天气查询工具")
    try:
        result = await mcp_tool.execute(
            config=amap_config,
            action="call_tool",
            tool_name="maps_weather",
            tool_args={"city": "北京"}
        )
        
        if result["status"] == "success":
            print("✅ 天气查询成功!")
            weather_data = result["result"]
            if isinstance(weather_data, dict) and "city" in weather_data:
                print(f"   城市: {weather_data['city']}")
                if "forecasts" in weather_data:
                    forecasts = weather_data["forecasts"]
                    if forecasts:
                        today = forecasts[0]
                        print(f"   今日天气: {today.get('dayweather', 'N/A')}")
                        print(f"   温度: {today.get('daytemp', 'N/A')}°C")
            else:
                print(f"   结果: {json.dumps(weather_data, ensure_ascii=False, indent=2)}")
        else:
            print(f"❌ 天气查询失败: {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ 测试2失败: {e}")
    
    # 测试3: 调用地理编码工具
    print("\n📍 测试3: 调用地理编码工具")
    try:
        result = await mcp_tool.execute(
            config=amap_config,
            action="call_tool",
            tool_name="maps_geo",
            tool_args={"address": "北京市天安门广场"}
        )
        
        if result["status"] == "success":
            print("✅ 地理编码成功!")
            geo_data = result["result"]
            if isinstance(geo_data, dict) and "return" in geo_data:
                locations = geo_data["return"]
                if locations and len(locations) > 0:
                    first_loc = locations[0]
                    print(f"   地址: {first_loc.get('country', '')}{first_loc.get('province', '')}{first_loc.get('city', '')}{first_loc.get('district', '')}")
                    print(f"   坐标: {first_loc.get('location', 'N/A')}")
            else:
                print(f"   结果: {json.dumps(geo_data, ensure_ascii=False, indent=2)}")
        else:
            print(f"❌ 地理编码失败: {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ 测试3失败: {e}")
    
    # 测试4: 调用搜索工具
    print("\n🔍 测试4: 调用POI搜索工具")
    try:
        result = await mcp_tool.execute(
            config=amap_config,
            action="call_tool",
            tool_name="maps_text_search",
            tool_args={"keywords": "咖啡厅", "city": "北京"}
        )
        
        if result["status"] == "success":
            print("✅ POI搜索成功!")
            search_data = result["result"]
            if isinstance(search_data, dict) and "pois" in search_data:
                pois = search_data["pois"]
                print(f"   找到 {len(pois)} 个结果:")
                for i, poi in enumerate(pois[:3], 1):  # 只显示前3个
                    print(f"   {i}. {poi.get('name', 'N/A')}")
                    print(f"      地址: {poi.get('address', 'N/A')}")
                if len(pois) > 3:
                    print(f"   ... 还有 {len(pois) - 3} 个结果")
            else:
                print(f"   结果: {json.dumps(search_data, ensure_ascii=False, indent=2)}")
        else:
            print(f"❌ POI搜索失败: {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ 测试4失败: {e}")
    
    print("\n🎉 MCP Tool测试完成!")
    return True

async def test_stdio_transport():
    """测试stdio传输方式"""
    print("\n📡 测试stdio传输方式")
    
    mcp_tool = MCPTool()
    
    # stdio配置（需要本地安装amap-mcp-server）
    stdio_config = {
        "@type": "ad:StructuredInterface", 
        "protocol": "MCP",
        "url": "stdio://amap-mcp-server",
        "transport": "stdio",
        "command": "uvx",
        "args": ["amap-mcp-server"],
        "env": {"AMAP_MAPS_API_KEY": "9d71135d3572ddc6dc18d350bd587bb3"}
    }
    
    try:
        result = await mcp_tool.execute(
            config=stdio_config,
            action="list_tools"
        )
        
        if result["status"] == "success":
            print(f"✅ stdio连接成功，发现 {result['count']} 个工具")
        else:
            print(f"❌ stdio连接失败: {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ stdio测试失败: {e}")

async def main():
    """主函数"""
    print("🧪 MCP Tool 功能测试")
    print("=" * 50)
    
    # 测试SSE传输方式
    success = await test_mcp_tool()
    
    # 如果SSE成功，可以选择测试stdio方式
    if success:
        print("\n" + "=" * 50)
        await test_stdio_transport()

if __name__ == "__main__":
    asyncio.run(main()) 