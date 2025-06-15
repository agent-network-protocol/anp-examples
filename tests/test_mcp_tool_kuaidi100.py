#!/usr/bin/env python3
"""
MCP Tool测试程序
测试MCP Tool连接快递100MCP服务器的功能
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
    
    # 快递100MCP服务器配置（SSE方式）
    kuaidi_config = {
        "@type": "ad:StructuredInterface",
        "protocol": "MCP",
        "url": "http://api.kuaidi100.com/mcp/sse?key=x",
        "description": "kuaidi100 MCP server for express tracking services",
        "transport": "sse"
    }
    
    print("🚀 开始测试MCP Tool功能")
    print("=" * 50)
    
    # 测试1: 列出可用工具
    print("\n📝 测试1: 列出快递100MCP服务器的可用工具")
    try:
        result = await mcp_tool.execute(
            config=kuaidi_config,
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
    
    # 测试2: 根据快递单号，返回对应的实时物流轨迹信息
    print("\n🌤️ 测试2: 根据快递单号，返回对应的实时物流轨迹信息")
    try:
        result = await mcp_tool.execute(
            config=kuaidi_config,
            action="call_tool",
            tool_name="query_trace",
            tool_args={"kuaidiName": "shentong", "kuaidiNum": "773359326147147"}
        )
        
        if result["status"] == "success":
            print("✅ 快递查询成功!")
            result_data = result["result"]
            if isinstance(result_data, dict) and "state" in result_data:
                print(f"   快递单当前状态: {result_data['state']}")
                if "data" in result_data:
                    data = result_data["data"]
                    print(f" 查询结果: {data}")
            else:
                print(f"   结果: {json.dumps(result_data, ensure_ascii=False, indent=2)}")
        else:
            print(f"❌ 快递查询失败: {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ 测试2失败: {e}")
    
    
    print("\n🎉 MCP Tool测试完成!")
    return True

async def main():
    """主函数"""
    print("🧪 MCP Tool 功能测试")
    print("=" * 50)
    
    # 测试SSE传输方式
    success = await test_mcp_tool()

if __name__ == "__main__":
    asyncio.run(main()) 