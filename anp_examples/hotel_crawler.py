from typing import Optional, Dict, Any, List, Union, Tuple, Set
import re
import os
import json
import asyncio
import logging
import httpx
from pathlib import Path
from openai import AsyncAzureOpenAI
from dotenv import load_dotenv
from anp_examples.utils.log_base import set_log_color_level
from anp_examples.anp_tool import ANPTool  # Import ANPTool

# Get project root directory
ROOT_DIR = Path(__file__).resolve().parent.parent

# Load environment variables
load_dotenv(ROOT_DIR / ".env")

from datetime import datetime

current_date = datetime.now().strftime("%Y-%m-%d")

# User memory and preferences
class UserMemory:
    """Class to store user memory and preferences"""
    def __init__(self):
        # Default user information
        self.default_name = "常高伟"
        self.default_phone = "13800000000"
        self.default_payment_method = "支付宝"
        self.default_room_preference = "大床房"
        
        # User preferences (can be updated based on interactions)
        # self.preferred_hotel_chains = ["全季酒店"]
        self.preferred_hotel_chains = [""]
        self.preferred_locations = []
        self.price_range = {"min": 0, "max": 1000}
        self.preferred_amenities = [""]
        self.previous_bookings = []
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert user memory to dictionary format"""
        return {
            "default_info": {
                "name": self.default_name,
                "phone": self.default_phone,
                "payment_method": self.default_payment_method,
                "room_preference": self.default_room_preference
            },
            "preferences": {
                "hotel_chains": self.preferred_hotel_chains,
                "locations": self.preferred_locations,
                "price_range": self.price_range,
                "amenities": self.preferred_amenities
            },
            "booking_history": self.previous_bookings
        }

# Initialize user memory
user_memory = UserMemory()

HOTEL_BOOKING_PROMPT_TEMPLATE = """
You are an intelligent hotel booking assistant. Your goal is to help users book hotel rooms by finding information about hotels and available rooms, and helping them complete the booking process.

## Current Task
{task_description}

## Important Notes
1. You will receive an initial URL ({initial_url}), which is an agent description file.
2. You need to understand the structure, functionality, and API usage methods of this agent.
3. You need to continuously discover and access new URLs and API endpoints to find hotel information.
4. You can use anp_tool to get the content of any URL.
5. This tool can handle various response formats, including:
   - JSON format: Will be directly parsed into JSON objects.
   - YAML format: Will return text content, and you need to analyze its structure.
   - Other text formats: Will return raw text content.
6. Read each document to find information or API endpoints related to the task.
7. You need to decide the search path yourself, don't wait for user instructions.
8. Note: You can access up to 10 URLs, and must end the search after reaching this limit.

## User Memory and Preferences
{user_memory_section}

## Search Strategy
1. First get the content of the initial URL to understand the hotel booking API structure.
2. Identify all URLs and links in the document, especially fields like serviceEndpoint, url, @id, etc.
3. Analyze API documentation to understand how to search for hotels, check room availability, and make bookings.
4. Build appropriate requests based on API documentation to find the information needed for the booking.
5. Record all URLs you've visited to avoid repeated access.
6. Summarize all relevant information you found and provide detailed recommendations.

## Workflow
1. Get the content of the initial URL and understand the hotel booking functionality.
2. Analyze the content to find all possible links and API documentation.
3. Parse API documentation to understand API usage.
4. Build requests according to task requirements to get the needed hotel and room information.
5. Continue exploring relevant links until sufficient information is found.
6. Summarize the information and provide the most appropriate recommendations to the user.

## JSON-LD Data Parsing Tips
1. Pay attention to the @context field, which defines the semantic context of the data.
2. The @type field indicates the type of entity, helping you understand the meaning of the data.
3. The @id field is usually a URL that can be further accessed.
4. Look for fields such as serviceEndpoint, url, etc., which usually point to APIs or more data.

Provide detailed information and clear explanations to help users understand the hotel options and booking process.

## Date
Current date: {current_date}


## Output Format
Your Output should be a single JSON string with the following structure:
{{
  "summary": "这是我们为你推荐的酒店(类似这样的描述，使用中文)",
  "contactName": "联系人姓名", 
  "contactMobile": "联系人电话",
  "checkInDate": "入住日期",
  "checkOutDate": "离开日期",
  "guestNames": ["入住人姓名"],
  "roomNum": 1,
  "content": [
    {{
      "roomTypeId": "房型ID",
      "ratePlanID": "RPL98765",
      "roomType": "房型名称",
      "bedType": "床型",
      "pricePerNight": 每晚价格,
      "orderAmount": 698.00,
      "images": "图片URL，每个房间给图片",
      "available": true/false,
      "hotel": {{
        "hotelID": "酒店唯一ID",
        "hotelName": "酒店名称",
        "address": "酒店地址",
        "rating": "评分",
        "price": "价格范围"
      }}
    }},
    {{
      // 第二个房型，最多只返回三个房型
    }},
    {{
      // 第三个房型，最多只返回三个房型
    }}
  ]
}}

Note: 
- The summary content must be in Chinese.
- ensure the generated JSON is valid, formatted correctly, and can be directly parsed by a JSON parser.
- The returned JSON should not include triple backticks, return pure JSON only
- Try to use room types with images so you can see what the hotel looks like.

"""

# Global variable
initial_url = "https://hotel-booking.ai/ad.json"


# Define available tools
def get_available_tools(anp_tool_instance):
    """Get the list of available tools"""
    return [
        {
            "type": "function",
            "function": {
                "name": "anp_tool",
                "description": anp_tool_instance.description,
                "parameters": anp_tool_instance.parameters,
            },
        }
    ]


async def handle_tool_call(
    tool_call: Any,
    messages: List[Dict],
    anp_tool: ANPTool,
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
            logging.info(f"ANPTool response ********  [url: {url}]")

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


async def hotel_crawler(
    user_input: str,
    task_type: str = "hotel_booking",
    did_document_path: Optional[str] = None,
    private_key_path: Optional[str] = None,
    max_documents: int = 20,
    initial_url: str = "https://agent-search.ai/ad.json",
) -> Dict[str, Any]:
    """
    Hotel booking logic: let the model decide the search path autonomously

    Args:
        user_input: Task description input by the user
        task_type: Task type
        did_document_path: DID document path
        private_key_path: Private key path
        max_documents: Maximum number of documents to access
        initial_url: Initial URL to start from

    Returns:
        Dictionary containing the hotel booking results
    """
    # Initialize variables
    visited_urls = set()
    crawled_documents = []

    # Initialize ANPTool
    anp_tool = ANPTool(
        did_document_path=did_document_path, private_key_path=private_key_path
    )

    # Initialize Azure OpenAI client
    client = AsyncAzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
    )

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

    # Format user memory section for prompt
    user_memory_section = (
        "The system has the following memory about the user's preferences and history:\n"
        f"1. Default Information:\n"
        f"   - Name: {user_memory.default_name}\n"
        f"   - Phone: {user_memory.default_phone}\n"
        f"   - Payment Method: {user_memory.default_payment_method}\n"
        f"   - Room Preference: {user_memory.default_room_preference}\n\n"
        f"2. Hotel Preferences:\n"
        f"   - Preferred Hotel Chains: {', '.join(user_memory.preferred_hotel_chains)}\n"
        f"   - Preferred Amenities: {', '.join(user_memory.preferred_amenities)}\n"
        f"   - Price Range: ¥{user_memory.price_range['min']} - ¥{user_memory.price_range['max']}\n"
    )
    
    # Add booking history if available
    if user_memory.previous_bookings:
        user_memory_section += "\n3. Previous Bookings:\n"
        for i, booking in enumerate(user_memory.previous_bookings, 1):
            user_memory_section += f"   {i}. {booking.get('hotel_name', 'Unknown Hotel')} on {booking.get('date', 'Unknown Date')}\n"
    
    # Create initial message
    formatted_prompt = HOTEL_BOOKING_PROMPT_TEMPLATE.format(
        task_description=user_input, 
        initial_url=initial_url, 
        current_date=current_date,
        user_memory_section=user_memory_section
    )

    messages = [
        {"role": "system", "content": formatted_prompt},
        {"role": "user", "content": user_input},
    ]

    # Initialize counters
    num_documents = 1  # Initial URL already counted
    max_retry = 3
    retry_count = 0

    # Start agent loop
    while num_documents < max_documents:
        try:
            # Call LLM API
            response = await client.chat.completions.create(
                model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
                # 移除temperature和top_p参数，使用默认值
                max_completion_tokens=4096,
                messages=messages,
                tools=get_available_tools(anp_tool),
                tool_choice="auto",
            )

            # Get model response
            assistant_message = response.choices[0].message
            # Make sure content is a string, not None
            content = assistant_message.content if assistant_message.content is not None else ""
            messages.append({
                "role": "assistant", 
                "content": content,
                "tool_calls": assistant_message.tool_calls
            })

            # Process tool calls
            tool_calls = assistant_message.tool_calls
            if not tool_calls:
                # No more tool calls, complete the process
                break

            # Handle tool calls
            for tool_call in tool_calls:
                await handle_tool_call(
                    tool_call, messages, anp_tool, crawled_documents, visited_urls
                )
                num_documents += 1

                # Check if maximum number of documents is reached
                if num_documents >= max_documents:
                    logging.info(f"Reached maximum number of documents: {max_documents}")
                    break

            retry_count = 0  # Reset retry count after successful API call

        except Exception as e:
            retry_count += 1
            logging.error(f"Error in API call: {str(e)}")

            if retry_count >= max_retry:
                logging.error(f"Maximum retries reached ({max_retry}). Aborting.")
                break

            await asyncio.sleep(1)  # Sleep before retrying

    # Final result generation
    try:
        final_response = await client.chat.completions.create(
            model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
            messages=[
                *messages,
                {
                    "role": "user",
                    "content": "Based on user preferences and the information you've collected, please provide detailed hotel booking information in a single JSON format.",
                },
            ],
        )

        final_content = final_response.choices[0].message.content
        logging.info("Final response generated:")
        logging.info(final_content)

        # 处理JSON响应数据
        parsed_content = parse_json_response(final_content)
        logging.info("Parsed response content:")
        if parsed_content:
            logging.info(json.dumps(parsed_content, ensure_ascii=False, indent=4, sort_keys=True))
            return parsed_content
        else:
            logging.error("Failed to parse response as JSON")
            logging.info(final_content)
            return {}
        
    except Exception as e:
        logging.error(f"Error generating final response: {str(e)}")
        return {} 

def parse_json_response(response_text):
    """
    解析响应文本，处理可能包含反引号的JSON字符串
    
    Args:
        response_text: AI返回的原始文本响应
        
    Returns:
        解析后的JSON对象，如果解析失败则返回None
    """
    if not isinstance(response_text, str):
        # 如果不是字符串，可能已经是字典对象
        return response_text
    
    # 尝试直接解析
    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        pass
    
    # 如果失败，尝试处理带有反引号的JSON
    json_pattern = r'```(?:json)?\s*({[\s\S]*?})\s*```'
    match = re.search(json_pattern, response_text)
    if match:
        json_str = match.group(1)
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            pass
    
    # 如果还是失败，找到第一个大括号和最后一个大括号之间的内容
    try:
        start_idx = response_text.find('{')
        end_idx = response_text.rfind('}')
        if start_idx != -1 and end_idx != -1 and start_idx < end_idx:
            json_str = response_text[start_idx:end_idx+1]
            return json.loads(json_str)
    except json.JSONDecodeError:
        pass
    
    # 所有方法都失败，返回空字典
    return {}

async def main():
    """Main function"""
    # Example usage
    query = "帮我预订北京望京的酒店，后天入住，1晚"
    query = "帮我预订杭州未来科技城的酒店，后天入住，1晚"
    
    # Simply display current user memory (without updating)
    logging.info("\nUser Memory Being Used:")
    logging.info(json.dumps(user_memory.to_dict(), ensure_ascii=False, indent=2))
    
    # Process hotel booking using pre-defined memory
    result = await hotel_crawler(user_input=query)
    
    # Display results
    logging.info("Search Result:")
    logging.info(result)

if __name__ == "__main__":
    set_log_color_level(logging.DEBUG)
    asyncio.run(main())