import asyncio
import json
import aiohttp
import os
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional, List
import logging
from urllib.parse import urlparse, parse_qs
import tempfile

class MCPTool:
    name: str = "mcp_tool"
    description: str = """Connect to and interact with MCP (Model Context Protocol) servers.
1. When using, you need to input MCP server configuration including URL and protocol details.
2. The tool will connect to the MCP server, discover available tools, and execute requested functions.
3. Supports various MCP transport methods including SSE, stdio, and streamable-http.
4. Can automatically discover and list available MCP tools for the user to choose from.
"""
    parameters: dict = {
        "type": "object",
        "properties": {
            "config": {
                "type": "object",
                "description": "(required) MCP server configuration",
                "properties": {
                    "@type": {
                        "type": "string",
                        "description": "Interface type, typically 'ad:StructuredInterface'",
                        "default": "ad:StructuredInterface"
                    },
                    "protocol": {
                        "type": "string",
                        "description": "Protocol type, should be 'MCP'",
                        "default": "MCP"
                    },
                    "url": {
                        "type": "string",
                        "description": "(required) MCP server URL"
                    },
                    "transport": {
                        "type": "string",
                        "description": "Transport method: sse, stdio, or streamable-http",
                        "enum": ["sse", "stdio", "streamable-http"],
                        "default": "sse"
                    },
                    "description": {
                        "type": "string",
                        "description": "Description of the MCP server"
                    }
                },
                "required": ["url"]
            },
            "action": {
                "type": "string",
                "description": "Action to perform: 'list_tools' to discover available tools, or 'call_tool' to execute a specific tool",
                "enum": ["list_tools", "call_tool"],
                "default": "list_tools"
            },
            "tool_name": {
                "type": "string",
                "description": "(required for call_tool action) Name of the MCP tool to call"
            },
            "tool_args": {
                "type": "object",
                "description": "(optional for call_tool action) Arguments to pass to the MCP tool",
                "default": {}
            }
        },
        "required": ["config"]
    }

    def __init__(self):
        """Initialize MCPTool"""
        self._session_cache = {}  # Cache MCP sessions for reuse
        
    async def execute(
        self,
        config: Dict[str, Any],
        action: str = "list_tools",
        tool_name: Optional[str] = None,
        tool_args: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Execute MCP operations

        Args:
            config (Dict[str, Any]): MCP server configuration
            action (str): Action to perform ('list_tools' or 'call_tool')
            tool_name (str, optional): Name of the MCP tool to call (for call_tool action)
            tool_args (Dict[str, Any], optional): Arguments for the MCP tool

        Returns:
            Dict[str, Any]: Operation result
        """
        
        if tool_args is None:
            tool_args = {}
            
        try:
            # Validate config
            if not isinstance(config, dict) or "url" not in config:
                return {"error": "Invalid config: 'url' is required", "status": "error"}
            
            url = config["url"]
            transport = config.get("transport", "sse")
            
            logging.info(f"MCP operation: {action} on {url} using {transport} transport")
            
            # Determine transport method from URL if not specified
            if transport == "sse" or "sse" in url:
                return await self._handle_sse_transport(config, action, tool_name, tool_args)
            elif transport == "stdio":
                return await self._handle_stdio_transport(config, action, tool_name, tool_args)
            elif transport == "streamable-http":
                return await self._handle_streamable_http_transport(config, action, tool_name, tool_args)
            else:
                # Try to auto-detect transport from URL
                if "sse" in url.lower():
                    return await self._handle_sse_transport(config, action, tool_name, tool_args)
                elif url.startswith("http"):
                    return await self._handle_streamable_http_transport(config, action, tool_name, tool_args)
                else:
                    return {"error": f"Unsupported transport method: {transport}", "status": "error"}
                    
        except Exception as e:
            logging.error(f"MCP tool execution failed: {str(e)}")
            return {"error": f"MCP tool execution failed: {str(e)}", "status": "error"}

    async def _handle_sse_transport(
        self, 
        config: Dict[str, Any], 
        action: str, 
        tool_name: Optional[str], 
        tool_args: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle SSE transport"""
        try:
            from mcp import ClientSession
            from mcp.client.sse import sse_client
            
            url = config["url"]
            
            logging.info(f"Connecting to MCP server via SSE: {url}")
            
            async with sse_client(url) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    
                    if action == "list_tools":
                        return await self._list_tools(session)
                    elif action == "call_tool":
                        return await self._call_tool(session, tool_name, tool_args)
                    else:
                        return {"error": f"Unknown action: {action}", "status": "error"}
                        
        except ImportError:
            return {"error": "MCP SSE client not available. Please install: pip install mcp", "status": "error"}
        except Exception as e:
            logging.error(f"SSE transport failed: {str(e)}")
            return {"error": f"SSE transport failed: {str(e)}", "status": "error"}

    async def _handle_stdio_transport(
        self, 
        config: Dict[str, Any], 
        action: str, 
        tool_name: Optional[str], 
        tool_args: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle stdio transport"""
        try:
            from mcp import ClientSession, StdioServerParameters
            from mcp.client.stdio import stdio_client
            
            # Extract server command from URL or config
            # For stdio, the URL might contain server command info
            server_config = self._parse_stdio_config(config)
            
            server_params = StdioServerParameters(
                command=server_config["command"],
                args=server_config["args"],
                env=server_config.get("env", {})
            )
            
            logging.info(f"Starting MCP server via stdio: {server_params.command} {' '.join(server_params.args)}")
            
            async with stdio_client(server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    
                    if action == "list_tools":
                        return await self._list_tools(session)
                    elif action == "call_tool":
                        return await self._call_tool(session, tool_name, tool_args)
                    else:
                        return {"error": f"Unknown action: {action}", "status": "error"}
                        
        except ImportError:
            return {"error": "MCP stdio client not available. Please install: pip install mcp", "status": "error"}
        except Exception as e:
            logging.error(f"Stdio transport failed: {str(e)}")
            return {"error": f"Stdio transport failed: {str(e)}", "status": "error"}

    async def _handle_streamable_http_transport(
        self, 
        config: Dict[str, Any], 
        action: str, 
        tool_name: Optional[str], 
        tool_args: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle streamable HTTP transport"""
        try:
            url = config["url"]
            
            # For streamable HTTP, we make standard HTTP requests to MCP endpoints
            async with aiohttp.ClientSession() as session:
                if action == "list_tools":
                    return await self._http_list_tools(session, url)
                elif action == "call_tool":
                    return await self._http_call_tool(session, url, tool_name, tool_args)
                else:
                    return {"error": f"Unknown action: {action}", "status": "error"}
                    
        except Exception as e:
            logging.error(f"Streamable HTTP transport failed: {str(e)}")
            return {"error": f"Streamable HTTP transport failed: {str(e)}", "status": "error"}

    def _parse_stdio_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Parse stdio configuration from URL or config"""
        url = config["url"]
        
        # Check if config contains explicit stdio parameters
        if "command" in config:
            return {
                "command": config["command"],
                "args": config.get("args", []),
                "env": config.get("env", {})
            }
        
        # Try to extract from URL (simple parsing)
        if "amap" in url.lower():
            # Default for AMAP MCP server
            api_key = self._extract_api_key_from_url(url)
            return {
                "command": "uvx",
                "args": ["amap-mcp-server"],
                "env": {"AMAP_MAPS_API_KEY": api_key} if api_key else {}
            }
        
        # Generic fallback
        return {
            "command": "uvx",
            "args": ["mcp-server"],
            "env": {}
        }

    def _extract_api_key_from_url(self, url: str) -> Optional[str]:
        """Extract API key from URL parameters"""
        try:
            parsed = urlparse(url)
            params = parse_qs(parsed.query)
            
            # Look for common API key parameter names
            for key_param in ["key", "api_key", "apikey", "token"]:
                if key_param in params and params[key_param]:
                    return params[key_param][0]
            
            return None
        except Exception:
            return None

    async def _list_tools(self, session) -> Dict[str, Any]:
        """List available tools from MCP session"""
        try:
            tools_result = await session.list_tools()
            tools = tools_result.tools
            
            tool_list = []
            for tool in tools:
                tool_info = {
                    "name": tool.name,
                    "description": getattr(tool, "description", "No description available")
                }
                
                # Add input schema if available
                if hasattr(tool, "inputSchema") and tool.inputSchema:
                    tool_info["parameters"] = tool.inputSchema
                
                tool_list.append(tool_info)
            
            return {
                "status": "success",
                "action": "list_tools",
                "tools": tool_list,
                "count": len(tool_list)
            }
            
        except Exception as e:
            logging.error(f"Failed to list tools: {str(e)}")
            return {"error": f"Failed to list tools: {str(e)}", "status": "error"}

    async def _call_tool(self, session, tool_name: str, tool_args: Dict[str, Any]) -> Dict[str, Any]:
        """Call a specific tool via MCP session"""
        try:
            if not tool_name:
                return {"error": "tool_name is required for call_tool action", "status": "error"}
            
            logging.info(f"Calling MCP tool: {tool_name} with args: {tool_args}")
            
            result = await session.call_tool(tool_name, tool_args)
            
            if hasattr(result, "content") and result.content:
                content_list = []
                for content_item in result.content:
                    if hasattr(content_item, "text"):
                        try:
                            # Try to parse as JSON
                            parsed_content = json.loads(content_item.text)
                            content_list.append(parsed_content)
                        except json.JSONDecodeError:
                            # If not JSON, keep as text
                            content_list.append(content_item.text)
                
                return {
                    "status": "success",
                    "action": "call_tool",
                    "tool_name": tool_name,
                    "result": content_list[0] if len(content_list) == 1 else content_list
                }
            else:
                return {
                    "status": "success",
                    "action": "call_tool",
                    "tool_name": tool_name,
                    "result": "No content returned"
                }
                
        except Exception as e:
            logging.error(f"Failed to call tool {tool_name}: {str(e)}")
            return {"error": f"Failed to call tool {tool_name}: {str(e)}", "status": "error"}

    async def _http_list_tools(self, session: aiohttp.ClientSession, url: str) -> Dict[str, Any]:
        """List tools via HTTP (for streamable HTTP transport)"""
        try:
            # Streamable HTTP typically uses POST to /mcp endpoint
            mcp_url = url.rstrip("/") + "/list_tools" if not url.endswith("/list_tools") else url
            
            async with session.post(mcp_url, json={"method": "tools/list"}) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "status": "success",
                        "action": "list_tools",
                        "tools": data.get("tools", []),
                        "count": len(data.get("tools", []))
                    }
                else:
                    return {"error": f"HTTP {response.status}: {await response.text()}", "status": "error"}
                    
        except Exception as e:
            logging.error(f"HTTP list tools failed: {str(e)}")
            return {"error": f"HTTP list tools failed: {str(e)}", "status": "error"}

    async def _http_call_tool(
        self, 
        session: aiohttp.ClientSession, 
        url: str, 
        tool_name: str, 
        tool_args: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Call tool via HTTP (for streamable HTTP transport)"""
        try:
            if not tool_name:
                return {"error": "tool_name is required for call_tool action", "status": "error"}
            
            # Streamable HTTP typically uses POST to /mcp endpoint
            mcp_url = url.rstrip("/") + "/call_tool" if not url.endswith("/call_tool") else url
            
            payload = {
                "method": "tools/call",
                "params": {
                    "name": tool_name,
                    "arguments": tool_args
                }
            }
            
            async with session.post(mcp_url, json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "status": "success",
                        "action": "call_tool",
                        "tool_name": tool_name,
                        "result": data.get("result", data)
                    }
                else:
                    return {"error": f"HTTP {response.status}: {await response.text()}", "status": "error"}
                    
        except Exception as e:
            logging.error(f"HTTP call tool failed: {str(e)}")
            return {"error": f"HTTP call tool failed: {str(e)}", "status": "error"} 