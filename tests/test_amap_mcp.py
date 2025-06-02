#!/usr/bin/env python3
"""
高德地图MCP Server测试程序
使用官方MCP SDK测试高德地图MCP服务器的功能
"""

import os
import asyncio
import json
import logging
from pathlib import Path
from dotenv import load_dotenv
from typing import Dict, Any

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 加载环境变量
load_dotenv()

class AmapMCPTester:
    """高德地图MCP服务器测试类"""
    
    def __init__(self):
        """初始化测试器"""
        self.amap_key = os.getenv('AMAP_KEY')
        if not self.amap_key:
            raise ValueError("未找到AMAP_KEY环境变量，请在.env文件中设置AMAP_KEY")
        
        # MCP客户端（根据实际可用的传输方式选择）
        self.mcp_client = None
        self.available_tools = []
    
    async def test_stdio_connection(self):
        """测试stdio连接方式"""
        try:
            from mcp import ClientSession, StdioServerParameters
            from mcp.client.stdio import stdio_client
            
            # 配置MCP服务器参数
            server_params = StdioServerParameters(
                command="uvx",
                args=["amap-mcp-server"],
                env={"AMAP_MAPS_API_KEY": self.amap_key}
            )
            
            logger.info("正在连接高德MCP服务器（stdio模式）...")
            
            async with stdio_client(server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    # 初始化会话
                    await session.initialize()
                    
                    # 列出可用工具
                    tools_result = await session.list_tools()
                    self.available_tools = tools_result.tools
                    
                    logger.info(f"成功连接，发现 {len(self.available_tools)} 个工具:")
                    for tool in self.available_tools:
                        logger.info(f"  - {tool.name}: {tool.description}")
                    
                    # 执行测试用例
                    await self.run_test_cases(session)
                    
        except ImportError as e:
            logger.error(f"缺少MCP SDK依赖: {e}")
            logger.info("请安装MCP SDK: pip install mcp")
            return False
        except Exception as e:
            logger.error(f"stdio连接失败: {e}")
            return False
        
        return True
    
    async def test_sse_connection(self, sse_url: str = "https://mcp.amap.com/sse"):
        """测试SSE连接方式"""
        try:
            import aiohttp
            from mcp import ClientSession
            from mcp.client.sse import sse_client
            
            # 构建完整的SSE URL，包含API key
            full_url = f"{sse_url}?key={self.amap_key}"
            
            logger.info(f"正在连接高德MCP服务器（SSE模式）: {full_url}")
            
            async with sse_client(full_url) as (read, write):
                async with ClientSession(read, write) as session:
                    # 初始化会话
                    await session.initialize()
                    
                    # 列出可用工具
                    tools_result = await session.list_tools()
                    self.available_tools = tools_result.tools
                    
                    logger.info(f"成功连接，发现 {len(self.available_tools)} 个工具:")
                    for tool in self.available_tools:
                        logger.info(f"  - {tool.name}: {tool.description}")
                    
                    # 执行测试用例
                    await self.run_test_cases(session)
                    
        except ImportError as e:
            logger.error(f"缺少SSE相关依赖: {e}")
            logger.info("请安装依赖: pip install aiohttp")
            return False
        except Exception as e:
            logger.error(f"SSE连接失败: {e}")
            return False
        
        return True
    
    async def run_test_cases(self, session):
        """运行测试用例"""
        test_cases = [
            {
                "name": "天气查询测试",
                "tool": "maps_weather",
                "args": {"city": "北京"}
            },
            {
                "name": "地理编码测试",
                "tool": "maps_geo", 
                "args": {"address": "北京市朝阳区阜通东大街6号"}
            },
            {
                "name": "逆地理编码测试",
                "tool": "maps_regeocode",
                "args": {"location": "116.481488,39.990464"}
            },
            {
                "name": "关键词搜索测试",
                "tool": "maps_text_search",
                "args": {"keywords": "咖啡厅", "city": "北京"}
            },
            {
                "name": "周边搜索测试", 
                "tool": "maps_around_search",
                "args": {"location": "116.481488,39.990464", "keywords": "餐厅", "radius": "1000"}
            },
            {
                "name": "步行路径规划测试",
                "tool": "maps_direction_walking_by_address",
                "args": {
                    "origin_address": "北京市朝阳区阜通东大街6号",
                    "destination_address": "北京市海淀区上地十街10号"
                }
            }
        ]
        
        for test_case in test_cases:
            await self.run_single_test(session, test_case)
    
    async def run_single_test(self, session, test_case: Dict[str, Any]):
        """运行单个测试用例"""
        tool_name = test_case["tool"]
        test_name = test_case["name"]
        args = test_case["args"]
        
        # 检查工具是否可用
        available_tool_names = [tool.name for tool in self.available_tools]
        if tool_name not in available_tool_names:
            logger.warning(f"⚠️  {test_name}: 工具 '{tool_name}' 不可用，跳过测试")
            return
        
        try:
            logger.info(f"🧪 开始测试: {test_name}")
            logger.info(f"   工具: {tool_name}")
            logger.info(f"   参数: {json.dumps(args, ensure_ascii=False)}")
            
            # 调用工具
            result = await session.call_tool(tool_name, args)
            
            if hasattr(result, 'content') and result.content:
                logger.info(f"✅ {test_name} 成功!")
                
                # 解析并美化输出结果
                for content_item in result.content:
                    if hasattr(content_item, 'text'):
                        try:
                            # 尝试解析JSON并美化输出
                            data = json.loads(content_item.text)
                            logger.info(f"   结果: {json.dumps(data, ensure_ascii=False, indent=2)}")
                        except (json.JSONDecodeError, TypeError):
                            # 如果不是JSON，直接输出文本
                            logger.info(f"   结果: {content_item.text}")
            else:
                logger.warning(f"⚠️  {test_name}: 未返回内容")
                
        except Exception as e:
            logger.error(f"❌ {test_name} 失败: {e}")
        
        logger.info("-" * 60)
    
    async def interactive_test(self):
        """交互式测试模式"""
        print("\n=== 高德地图MCP服务器交互式测试 ===")
        print("可用工具:")
        for i, tool in enumerate(self.available_tools, 1):
            print(f"{i}. {tool.name}: {tool.description}")
        
        while True:
            try:
                print("\n请选择要测试的工具 (输入数字，0退出):")
                choice = input("> ").strip()
                
                if choice == "0":
                    break
                
                tool_index = int(choice) - 1
                if 0 <= tool_index < len(self.available_tools):
                    tool = self.available_tools[tool_index]
                    await self.manual_tool_test(tool)
                else:
                    print("无效选择，请重新输入")
                    
            except (ValueError, KeyboardInterrupt):
                break
    
    async def manual_tool_test(self, tool):
        """手动工具测试"""
        print(f"\n测试工具: {tool.name}")
        print(f"描述: {tool.description}")
        
        if hasattr(tool, 'inputSchema') and tool.inputSchema:
            print("参数说明:")
            schema = tool.inputSchema
            if 'properties' in schema:
                for prop_name, prop_info in schema['properties'].items():
                    required = prop_name in schema.get('required', [])
                    required_text = "(必需)" if required else "(可选)"
                    description = prop_info.get('description', '无描述')
                    print(f"  - {prop_name} {required_text}: {description}")
        
        print("\n请输入参数 (JSON格式):")
        try:
            args_input = input("> ").strip()
            if args_input:
                args = json.loads(args_input)
            else:
                args = {}
            
            # 这里需要实际的session，暂时只是演示
            print(f"将调用工具: {tool.name}, 参数: {json.dumps(args, ensure_ascii=False)}")
            
        except json.JSONDecodeError:
            print("JSON格式错误，请重新输入")
        except KeyboardInterrupt:
            return

async def main():
    """主函数"""
    print("🚀 高德地图MCP服务器测试程序")
    print("=" * 50)
    
    try:
        tester = AmapMCPTester()
        
        # 首先尝试stdio连接
        print("\n📡 尝试stdio连接...")
        if await tester.test_stdio_connection():
            print("✅ stdio连接测试完成!")
        else:
            print("❌ stdio连接失败，尝试SSE连接...")
            
            # 如果stdio失败，尝试SSE连接
            if await tester.test_sse_connection():
                print("✅ SSE连接测试完成!")
            else:
                print("❌ 所有连接方式都失败了")
                return
        
    except Exception as e:
        logger.error(f"测试过程中发生错误: {e}")
        return
    
    print("\n🎉 测试完成!")

if __name__ == "__main__":
    asyncio.run(main()) 