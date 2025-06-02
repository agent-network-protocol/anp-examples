from typing import Optional, Dict, Any, List, Union
import os
import json
import logging
import asyncio
from pathlib import Path

# 设置增强日志配置 - 必须在其他导入之前
from anp_examples.utils.log_base import setup_enhanced_logging
setup_enhanced_logging(logging.DEBUG)

from openai import AsyncAzureOpenAI
from dotenv import load_dotenv
from anp_examples.anp_tool import ANPTool  # Import ANPTool
from anp_examples.mcp_tool import MCPTool  # Import MCPTool
from anp_examples.get_key_tool import GetKeyTool  # Import GetKeyTool
from openai import AsyncOpenAI,OpenAI
from config import validate_config, DASHSCOPE_API_KEY, DASHSCOPE_BASE_URL, DASHSCOPE_MODEL_NAME, OPENAI_API_KEY, \
    OPENAI_BASE_URL, OPENAI_MODEL

# Get the absolute path to the root directory
ROOT_DIR = Path(__file__).resolve().parent.parent

# Load environment variables
load_dotenv(ROOT_DIR / ".env")

from datetime import datetime

current_date = datetime.now().strftime("%Y-%m-%d")

validate_config()

SEARCH_AGENT_PROMPT_TEMPLATE = """You are an intelligent agent crawler. Your task is to start from the initial URL, explore and parse agent information through the Agent Network Protocol (ANP) and Model Context Protocol (MCP), and complete the user's task.

## Task Description
{task_description}

## Available Tools
1. **anp_tool**: For accessing ANP-compatible endpoints and agent description files
   - Used for HTTP requests to get JSON-LD agent descriptions
   - Can access REST APIs and structured data endpoints
   
2. **mcp_tool**: For connecting to MCP (Model Context Protocol) servers
   - Used when you encounter MCP server configurations in agent descriptions
   - Can discover available MCP tools and execute them
   - Supports SSE, stdio, and streamable-http transports

3. **get_key_tool**: For obtaining API keys from .env configuration file
   - Used to get any API key (like AMAP_KEY) from .env file
   - Simple and reliable key retrieval from environment configuration
   - Use when you need to access API services that require authentication

## MCP Tool Usage
When you find MCP server configurations like:
```json
{{
    "@type": "ad:StructuredInterface",
    "protocol": "MCP",
    "url": "https://mcp.amap.com/sse?key=YOUR_API_KEY",
    "description": "AMAP MCP server for location services"
}}
```

Use mcp_tool in two steps:
1. First, list available tools: `{{"config": mcp_config, "action": "list_tools"}}`
2. Then, call specific tools: `{{"config": mcp_config, "action": "call_tool", "tool_name": "tool_name", "tool_args": {{}}}}`

## Get Key Tool Usage
When you need to access API services that require keys:
1. Get AMAP key: `{{"key_name": "AMAP_KEY"}}`
2. Get other keys: `{{"key_name": "YOUR_KEY_NAME"}}`

The tool automatically locates the .env file in the project root directory.

## Your Responsibilities
1. Start crawling from the initial URL: {initial_url}
2. Use anp_tool to access agent description files and API endpoints.
3. When you find MCP server configurations, use mcp_tool to connect and interact with them.
4. When you need API keys, use get_key_tool to obtain them from .env file.
5. Analyze API documentation to understand API usage, parameters, and return values.
6. Build appropriate requests based on API documentation to find the needed information.
7. Record all URLs you've visited to avoid repeated crawling.
8. Summarize all relevant information you found and provide detailed recommendations.

## Workflow
1. Get the content of the initial URL and understand the agent's functionality.
2. Analyze the content to find all possible links, API documentation, and MCP server configurations.
3. For ANP endpoints: Parse API documentation to understand API usage.
4. For MCP servers: Connect using mcp_tool, discover available tools, and execute relevant functions.
5. For API services: Use get_key_tool to get required API keys from .env file.
6. Build requests according to task requirements to get the needed information.
7. Continue exploring relevant links until sufficient information is found.
8. Summarize the information and provide the most appropriate recommendations to the user.

## JSON-LD Data Parsing Tips
1. Pay attention to the @context field, which defines the semantic context of the data.
2. The @type field indicates the type of entity, helping you understand the meaning of the data.
3. The @id field is usually a URL that can be further accessed.
4. Look for fields such as serviceEndpoint, url, etc., which usually point to APIs or more data.
5. Look for "protocol": "MCP" which indicates MCP server configurations that need mcp_tool.
6. Look for API services that may require keys from get_key_tool.

Provide detailed information and clear explanations to help users understand the information you found and your recommendations.

## Date
Current date: {current_date}
"""

# Global variable
initial_url = "https://agent-search.ai/ad.json"


# Define available tools
def get_available_tools(anp_tool_instance, mcp_tool_instance, get_key_tool_instance):
    """Get the list of available tools"""
    return [
        {
            "type": "function",
            "function": {
                "name": "anp_tool",
                "description": anp_tool_instance.description,
                "parameters": anp_tool_instance.parameters,
            },
        },
        {
            "type": "function",
            "function": {
                "name": "mcp_tool",
                "description": mcp_tool_instance.description,
                "parameters": mcp_tool_instance.parameters,
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_key_tool",
                "description": get_key_tool_instance.description,
                "parameters": get_key_tool_instance.parameters,
            },
        }
    ]


async def handle_tool_call(
    tool_call: Any,
    messages: List[Dict],
    anp_tool: ANPTool,
    mcp_tool: MCPTool,
    get_key_tool: GetKeyTool,
    crawled_documents: List[Dict],
    visited_urls: set,
) -> None:
    """Handle tool call"""
    function_name = tool_call.function.name
    function_args = json.loads(tool_call.function.arguments)

    if function_name == "anp_tool":
        url = function_args.get("url")
        method = function_args.get("method", "GET")
        headers = function_args.get("headers", {})
        params = function_args.get("params", {})
        body = function_args.get("body")

        try:
            # Use ANPTool to get URL content
            result = await anp_tool.execute(
                url=url, method=method, headers=headers, params=params, body=body
            )
            logging.info(f"ANPTool response [url: {url}]")

            # Record visited URLs and obtained content
            visited_urls.add(url)
            crawled_documents.append({"url": url, "method": method, "content": result})

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result, ensure_ascii=False),
                }
            )
        except Exception as e:
            logging.error(f"Error using ANPTool for URL {url}: {str(e)}")

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(
                        {
                            "error": f"Failed to use ANPTool for URL: {url}",
                            "message": str(e),
                        }
                    ),
                }
            )
    
    elif function_name == "mcp_tool":
        config = function_args.get("config", {})
        action = function_args.get("action", "list_tools")
        tool_name = function_args.get("tool_name")
        tool_args = function_args.get("tool_args", {})

        try:
            # Use MCPTool to interact with MCP server
            result = await mcp_tool.execute(
                config=config, action=action, tool_name=tool_name, tool_args=tool_args
            )
            logging.info(f"MCPTool response [action: {action}, config: {config.get('url', 'unknown')}]")

            # Record MCP server interactions
            mcp_url = config.get("url", "unknown")
            visited_urls.add(mcp_url)
            crawled_documents.append({
                "url": mcp_url,
                "method": "MCP",
                "action": action,
                "tool_name": tool_name,
                "content": result
            })

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result, ensure_ascii=False),
                }
            )
        except Exception as e:
            logging.error(f"Error using MCPTool: {str(e)}")

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(
                        {
                            "error": f"Failed to use MCPTool",
                            "config": config,
                            "action": action,
                            "message": str(e),
                        }
                    ),
                }
            )

    elif function_name == "get_key_tool":
        key_name = function_args.get("key_name", "AMAP_KEY")

        try:
            # Use GetKeyTool to get API key from project root .env file
            result = await get_key_tool.execute(key_name=key_name)
            logging.info(f"GetKeyTool response [key_name: {key_name}]")

            # Record API key operations (without logging the actual key)
            crawled_documents.append({
                "url": "get_key_tool",
                "method": "KEY_OPERATION",
                "key_name": key_name,
                "content": {
                    "status": result.get("status"),
                    "masked_key": result.get("masked_key"),
                    "message": result.get("message"),
                    "project_root": result.get("project_root")
                }
            })

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result, ensure_ascii=False),
                }
            )
        except Exception as e:
            logging.error(f"Error using GetKeyTool: {str(e)}")

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(
                        {
                            "error": f"Failed to use GetKeyTool",
                            "key_name": key_name,
                            "message": str(e),
                        }
                    ),
                }
            )


async def simple_crawl(
    user_input: str,
    task_type: str = "general",
    did_document_path: Optional[str] = None,
    private_key_path: Optional[str] = None,
    max_documents: int = 10,
    initial_url: str = "https://agent-search.ai/ad.json",
) -> Dict[str, Any]:
    """
    Simplified crawling logic: let the model decide the crawling path autonomously

    Args:
        user_input: Task description input by the user
        task_type: Task type
        did_document_path: DID document path
        private_key_path: Private key path
        max_documents: Maximum number of documents to crawl
        initial_url: Initial URL to start crawling from

    Returns:
        Dictionary containing the crawl results
    """
    # Initialize variables
    visited_urls = set()
    crawled_documents = []

    # Initialize ANPTool
    anp_tool = ANPTool(
        did_document_path=did_document_path, private_key_path=private_key_path
    )

    # Initialize MCPTool
    mcp_tool = MCPTool()

    # Initialize GetKeyTool
    get_key_tool = GetKeyTool()

    # Initialize Azure OpenAI client
    # client = AsyncAzureOpenAI(
    #     api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    #     api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    #     azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    #     azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
    # )

    # 根据 MODEL_PROVIDER 环境变量选择不同的客户端
    model_provider = os.getenv("MODEL_PROVIDER", "dashscope").lower()

    if model_provider == "dashscope":
        client = AsyncOpenAI(
            api_key=DASHSCOPE_API_KEY,
            base_url=DASHSCOPE_BASE_URL
        )
        model_name = DASHSCOPE_MODEL_NAME
    elif model_provider == "openai":
        # 检测是否为Azure OpenAI并相应配置
        if 'openai.azure.com' in OPENAI_BASE_URL.lower():
            print("检测到Azure OpenAI配置，使用Azure兼容模式")
            client = AsyncOpenAI(
                api_key=OPENAI_API_KEY,
                base_url=OPENAI_BASE_URL,
                default_headers={"api-key": OPENAI_API_KEY},  # Azure特有的认证header
                default_query={"api-version": "2024-02-01"},   # Azure必需的API版本
            )
        else:
            print("检测到标准OpenAI配置")
            client = AsyncOpenAI(
                api_key=OPENAI_API_KEY,
                base_url=OPENAI_BASE_URL
            )
        model_name = OPENAI_MODEL
    else:
        raise ValueError(f"Unsupported MODEL_PROVIDER: {model_provider}")

    # Get initial URL content
    try:
        initial_content = await anp_tool.execute(url=initial_url)
        visited_urls.add(initial_url)
        crawled_documents.append(
            {"url": initial_url, "method": "GET", "content": initial_content}
        )

        logging.info(f"Successfully obtained initial URL: {initial_url}")
    except Exception as e:
        logging.error(f"Failed to obtain initial URL {initial_url}: {str(e)}")
        return {
            "content": f"Failed to obtain initial URL: {str(e)}",
            "type": "error",
            "visited_urls": [],
            "crawled_documents": [],
        }

    # Create initial message
    formatted_prompt = SEARCH_AGENT_PROMPT_TEMPLATE.format(
        task_description=user_input, 
        initial_url=initial_url, 
        current_date=current_date
    )

    messages = [
        {"role": "system", "content": formatted_prompt},
        {"role": "user", "content": user_input},
        {
            "role": "system",
            "content": f"I have obtained the content of the initial URL. Here is the description data of the search agent:\n\n```json\n{json.dumps(initial_content, ensure_ascii=False, indent=2)}\n```\n\nPlease analyze this data, understand the functions and API usage of the search agent. Find the links you need to visit, and use the anp_tool to get more information to complete the user's task.",
        },
    ]

    # Start conversation loop
    current_iteration = 0

    while current_iteration < max_documents:
        current_iteration += 1
        logging.info(f"Starting crawl iteration {current_iteration}/{max_documents}")

        # Check if the maximum number of documents to crawl has been reached
        if len(crawled_documents) >= max_documents:
            logging.info(
                f"Reached the maximum number of documents to crawl {max_documents}, stopping crawl"
            )
            # Add a message to inform the model that the maximum number of crawls has been reached
            messages.append(
                {
                    "role": "system",
                    "content": f"You have crawled {len(crawled_documents)} documents, reaching the maximum crawl limit of {max_documents}. Please make a final summary based on the information obtained.",
                }
            )

        # Get model response
        completion = await client.chat.completions.create(
            model = model_name,
            messages = messages,
            tools = get_available_tools(anp_tool, mcp_tool, get_key_tool),
            tool_choice = "auto",
        )

        response_message = completion.choices[0].message
        messages.append(
            {
                "role": "assistant",
                "content": response_message.content,
                "tool_calls": response_message.tool_calls,
            }
        )

        # debug code
        logging.info(f"Model response: {response_message.content}")
        logging.info(f"Tool calls: {response_message.tool_calls}")

        # Check if the conversation should end
        if not response_message.tool_calls:
            logging.info("The model did not request any tool calls, ending crawl")
            break

        # Handle tool calls
        for tool_call in response_message.tool_calls:
            await handle_tool_call(
                tool_call, messages, anp_tool, mcp_tool, get_key_tool, crawled_documents, visited_urls
            )

            # If the maximum number of documents to crawl is reached, stop handling tool calls
            if len(crawled_documents) >= max_documents:
                break

        # If the maximum number of documents to crawl is reached, make a final summary
        if (
            len(crawled_documents) >= max_documents
            and current_iteration < max_documents
        ):
            logging.info(
                f"Reached the maximum number of documents to crawl {max_documents}, making final summary"
            )
            continue

    # Create result
    result = {
        "content": response_message.content,
        "type": "text",
        "visited_urls": [doc["url"] for doc in crawled_documents],
        "crawled_documents": crawled_documents,
        "task_type": task_type,
    }

    return result


async def main():
    """Main function"""

    # Get DID path
    current_dir = Path(__file__).parent
    base_dir = current_dir.parent
    did_document_path = str(base_dir / "use_did_test_public/did.json")
    private_key_path = str(base_dir / "use_did_test_public/key-1_private.pem")

    from datetime import datetime, timedelta

    # Get the current date plus 3 days
    booking_date = (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d")

    # Test task
    # task = {
    #     "input": f"I need to book a hotel in Hangzhou: {booking_date}, for 1 day, coordinates (120.026208, 30.279212). Please handle it step by step: First, choose a good hotel yourself, then help me choose a room. Finally, tell me the details of your choice.",
    #     "type": "hotel_booking",
    # }

    # task = {
    #     "input": "明天到北京游玩，帮我看一下顺义区空港吉祥花园小区附近2km以内都有什么商场。",
    #     "type": "general",
    # }

    # task = {
    #     "input": "明天到北京国贸出差，帮我列一下步行1km以内的3星级酒店",
    #     "type": "general",
    # }

    task = {
        "input": "公司在阿里云云谷园区，附近有什么好吃的湘菜推荐",
        "type": "general",
    }

    task = {
        "input": "帮我预订一间北京望京地区今晚的三星级酒店",
        "type": "hotel_booking",
    }

    print(f"\n=== Test Task: {task['type']} ===")
    print(f"User Input: {task['input']}")

    # Use simplified crawling logic
    result = await simple_crawl(
        task["input"],
        task["type"],
        did_document_path=did_document_path,
        private_key_path=private_key_path,
        max_documents=20,  # Crawl up to 20 documents
    )

    # Print result
    print("\n=== Search Agent Response ===")
    print(result["content"])
    print("\n=== Visited URLs ===")
    for url in result.get("visited_urls", []):
        print(url)
    print(
        f"\n=== Crawled a total of {len(result.get('crawled_documents', []))} documents ==="
    )


if __name__ == "__main__":
    asyncio.run(main())
