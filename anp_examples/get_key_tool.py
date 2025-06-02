import os
import logging
from typing import Dict, Any, Optional
from pathlib import Path
from dotenv import load_dotenv


class GetKeyTool:
    name: str = "get_key_tool"
    description: str = """从项目根目录的.env文件获取API密钥的通用工具。
1. 自动定位项目根目录下的.env文件
2. 支持获取指定的API密钥
3. 自动加载.env文件
4. 提供密钥遮蔽保护隐私
"""
    parameters: dict = {
        "type": "object",
        "properties": {
            "key_name": {
                "type": "string",
                "description": "要获取的环境变量名称，如 AMAP_KEY",
                "default": "AMAP_KEY"
            }
        },
        "required": ["key_name"]
    }

    def __init__(self):
        """初始化密钥获取工具"""
        # 自动获取项目根目录
        self.project_root = self._find_project_root()
        self.env_file_path = self.project_root / ".env"
        
    def _find_project_root(self) -> Path:
        """自动查找项目根目录"""
        # 从当前文件开始向上查找，直到找到包含.env文件的目录或到达根目录
        current_path = Path(__file__).resolve()
        
        # 向上遍历目录
        for parent in current_path.parents:
            env_file = parent / ".env"
            if env_file.exists():
                return parent
        
        # 如果没有找到.env文件，返回当前工作目录的父目录（通常是项目根目录）
        return Path(__file__).resolve().parent.parent
        
    async def execute(
        self,
        key_name: str = "AMAP_KEY"
    ) -> Dict[str, Any]:
        """
        从项目根目录的.env文件获取指定的API密钥

        Args:
            key_name (str): 环境变量名称

        Returns:
            Dict[str, Any]: 操作结果
        """
        
        try:
            return await self._get_key_from_env_file(key_name)
                
        except Exception as e:
            logging.error(f"密钥获取工具执行失败: {str(e)}")
            return {"error": f"执行失败: {str(e)}", "status": "error"}

    async def _get_key_from_env_file(self, key_name: str) -> Dict[str, Any]:
        """从.env文件获取API密钥"""
        
        try:
            # 检查.env文件是否存在
            if not self.env_file_path.exists():
                return {
                    "error": f".env文件不存在: {self.env_file_path}",
                    "status": "error",
                    "key_name": key_name,
                    "env_file": str(self.env_file_path),
                    "project_root": str(self.project_root)
                }
            
            # 加载.env文件
            load_dotenv(self.env_file_path)
            
            # 获取指定的环境变量
            api_key = os.getenv(key_name)
            
            if api_key:
                return {
                    "status": "success",
                    "key_name": key_name,
                    "api_key": api_key,
                    "masked_key": self._mask_api_key(api_key),
                    "env_file": str(self.env_file_path),
                    "project_root": str(self.project_root),
                    "message": f"成功从项目根目录的.env文件获取{key_name}"
                }
            else:
                return {
                    "error": f"在.env文件中未找到环境变量: {key_name}",
                    "status": "error",
                    "key_name": key_name,
                    "env_file": str(self.env_file_path),
                    "project_root": str(self.project_root),
                    "suggestion": f"请在{self.env_file_path}文件中添加: {key_name}=your_api_key"
                }
                
        except Exception as e:
            return {
                "error": f"读取.env文件失败: {str(e)}",
                "status": "error",
                "key_name": key_name,
                "env_file": str(self.env_file_path),
                "project_root": str(self.project_root)
            }

    def _mask_api_key(self, api_key: str) -> str:
        """遮蔽API密钥以保护隐私"""
        if not api_key:
            return ""
        
        if len(api_key) <= 8:
            return "*" * len(api_key)
        
        return api_key[:4] + "*" * (len(api_key) - 8) + api_key[-4:] 