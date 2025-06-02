#!/usr/bin/env python3
"""
安装高德MCP测试所需的依赖
"""

import subprocess
import sys
import os

def run_command(cmd, description):
    """运行命令并处理结果"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=120)
        if result.returncode == 0:
            print(f"✅ {description}成功")
            return True
        else:
            print(f"❌ {description}失败:")
            print(f"错误输出: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print(f"❌ {description}超时")
        return False
    except Exception as e:
        print(f"❌ {description}异常: {e}")
        return False

def main():
    print("🚀 安装高德MCP测试依赖")
    print("=" * 40)
    
    # 基础Python依赖
    python_deps = [
        "python-dotenv",
        "asyncio-compat",
    ]
    
    # 安装Python依赖
    for dep in python_deps:
        if not run_command(f"pip install {dep}", f"安装{dep}"):
            print(f"⚠️  {dep}安装失败，但可能不影响主要功能")
    
    # 安装MCP SDK
    mcp_commands = [
        ("pip install mcp", "安装MCP SDK"),
        ("pip install uv", "安装UV包管理器"),
    ]
    
    success_count = 0
    for cmd, desc in mcp_commands:
        if run_command(cmd, desc):
            success_count += 1
    
    print(f"\n📊 安装结果: {success_count}/{len(mcp_commands)} 个主要依赖安装成功")
    
    # 验证安装
    print("\n🔍 验证安装...")
    
    try:
        import mcp
        print("✅ MCP SDK 验证成功")
    except ImportError:
        print("❌ MCP SDK 验证失败")
    
    try:
        from dotenv import load_dotenv
        print("✅ python-dotenv 验证成功")
    except ImportError:
        print("❌ python-dotenv 验证失败")
    
    # 检查uvx
    try:
        result = subprocess.run(['uvx', '--version'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("✅ uvx 命令可用")
        else:
            print("❌ uvx 命令不可用")
    except:
        print("❌ uvx 命令未找到")
    
    print("\n🎯 接下来请:")
    print("1. 在.env文件中设置您的高德API密钥:")
    print("   AMAP_KEY=\"您的高德API密钥\"")
    print("2. 运行测试程序:")
    print("   python simple_amap_test.py")

if __name__ == "__main__":
    main() 