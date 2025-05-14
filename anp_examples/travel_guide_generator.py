from typing import Optional, Dict, Any, List, Union, Set, Tuple
import re
import os
import json
import asyncio
import logging
import time
import datetime
from pathlib import Path
from openai import AsyncAzureOpenAI
from dotenv import load_dotenv
from anp_examples.utils.log_base import set_log_color_level
from anp_examples.anp_tool import ANPTool  # Import ANPTool
from anp_examples.simple_example import simple_crawl  # Import simple_crawl function

# Get project root directory
ROOT_DIR = Path(__file__).resolve().parent.parent

# Load environment variables
load_dotenv(ROOT_DIR / ".env")

# Get current date
current_date = datetime.datetime.now().strftime("%Y-%m-%d")

# Get DID document and private key paths
did_document_path = str(ROOT_DIR / "use_did_test_public/did.json")
private_key_path = str(ROOT_DIR / "use_did_test_public/key-1_private.pem")

# Travel guide prompt prefix - this will be combined with order details
TRAVEL_GUIDE_PREFIX = """
请为酒店客人生成一份详细的出行指南，包括以下内容：
1. 酒店设施与服务介绍
2. 交通选项（从机场/火车站到酒店，公共交通，出租车等）
3. 周边景点和地标（步行可达和短途旅行）
4. 当地美食推荐（著名当地菜，热门餐厅）
5. 购物区域（商场，市场，精品店）
6. 实用信息（紧急联系方式，实用短语等）
7. 基于住宿时长的行程建议

请用Markdown格式输出，包括:
- 欢迎介绍
- 清晰的章节标题
- 适当的列表
- 突出显示的实用提示
- 结尾附上进一步咨询的联系方式
- 最高使用三级目录，否则字体差距太大不美观

指南应该详尽但简洁，提供有价值的信息而不使客人感到信息过载。
"""

async def generate_travel_guide(order_detail: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate a travel guide based on hotel booking details using simple_crawl function
    
    Args:
        order_detail: Dictionary containing hotel booking details
        
    Returns:
        Dictionary containing the generated travel guide as a notification
    """
    try:
        # Extract hotel booking information
        hotel_id = order_detail.get('data', {}).get('hotelId', 'Unknown ID')
        hotel_name = order_detail.get('data', {}).get('hotelName', 'Unknown Hotel')
        hotel_address = order_detail.get('data', {}).get('hotelAddress', 'Unknown Address')
        check_in_date = order_detail.get('data', {}).get('checkInDate', 'Unknown Date')
        check_out_date = order_detail.get('data', {}).get('checkOutDate', 'Unknown Date')
        room_type = order_detail.get('data', {}).get('roomTypeName', 'Unknown Room Type')
        
        # Format date display
        try:
            check_in_date_obj = datetime.datetime.strptime(check_in_date, '%Y-%m-%d %H:%M:%S')
            check_in_formatted = check_in_date_obj.strftime('%Y年%m月%d日')
            check_out_date_obj = datetime.datetime.strptime(check_out_date, '%Y-%m-%d %H:%M:%S')
            check_out_formatted = check_out_date_obj.strftime('%Y年%m月%d日')
        except:
            check_in_formatted = check_in_date
            check_out_formatted = check_out_date
        
        # Extract location from address
        hotel_location = hotel_address.split('市')[0] if '市' in hotel_address else hotel_address.split('区')[0] if '区' in hotel_address else hotel_address
        
        # Calculate stay duration in days
        try:
            check_in_obj = datetime.datetime.strptime(check_in_date, '%Y-%m-%d %H:%M:%S')
            check_out_obj = datetime.datetime.strptime(check_out_date, '%Y-%m-%d %H:%M:%S')
            stay_duration = (check_out_obj - check_in_obj).days
            stay_duration_text = f"{stay_duration}晚" if stay_duration > 0 else "1晚"
        except:
            stay_duration_text = "短期"
        
        # Construct user query for simple_crawl
        query = f"{TRAVEL_GUIDE_PREFIX}\n\n酒店信息：\n- 酒店ID: {hotel_id}\n- 酒店名称: {hotel_name}\n- 酒店地址: {hotel_address}\n- 入住日期: {check_in_formatted}\n- 退房日期: {check_out_formatted}\n- 房型: {room_type}\n- 住宿时长: {stay_duration_text}\n\n请特别关注酒店所在的{hotel_location}地区！"
        
        logging.info(f"Generating travel guide for hotel: {hotel_name} in {hotel_location}")
        
        # Use simple_crawl to generate travel guide
        result = await simple_crawl(
            user_input=query,
            task_type="travel_guide",
            did_document_path=did_document_path,
            private_key_path=private_key_path,
            max_documents=10,  # Limit to 10 documents for reasonable response time
            initial_url="https://agent-search.ai/ad.json"  # Use default search agent URL
        )
        
        # Parse markdown from the response if needed
        guide_content = result.get("content", "")
        
        # Create notification object
        current_time = datetime.datetime.now().isoformat()
        notification = {
            "id": f"guide_{int(time.time())}",
            "type": "出行指南",
            "title": f"{hotel_name}出行指南",
            "content": guide_content,
            "hotelId": hotel_id,  # Include hotel ID in the notification
            "timestamp": current_time,
            "read": False,
            "visited_urls": result.get("visited_urls", []),  # Include URLs that were visited
            "crawled_documents": len(result.get("crawled_documents", []))  # Number of documents crawled
        }
        
        logging.info(f"Successfully generated travel guide for {hotel_name}")
        return notification
        
    except Exception as e:
        logging.error(f"Error generating travel guide: {str(e)}")
        # Create error notification
        current_time = datetime.datetime.now().isoformat()
        error_notification = {
            "id": f"guide_error_{int(time.time())}",
            "type": "系统通知",
            "title": "出行指南生成失败",
            "content": f"很抱歉，无法为您生成{order_detail.get('data', {}).get('hotelName', '酒店')}的出行指南。请稍后再试。",
            "hotelId": order_detail.get('data', {}).get('hotelId', 'Unknown ID'),
            "timestamp": current_time,
            "read": False
        }
        return error_notification


async def main():
    """Test function for travel guide generation"""
    # Using real hotel order data for testing
    sample_order = {
        'data': {
            'numberOfRooms': 1,
            'numberOfNights': 1, 
            'arriveTime': None, 
            'checkInDate': '2025-05-15 00:00:00', 
            'checkOutDate': '2025-05-16 00:00:00', 
            'guestNames': '常高伟', 
            'remark': '', 
            'orderAmount': 143.0, 
            'orderStatus': 2, 
            'payStatus': 1, 
            'payTime': '2025-05-14 13:23:04', 
            'paymentType': 1, 
            'transactionNo': '202505141323040076631002', 
            'refundAmount': None, 
            'refundSuccessTime': None, 
            'refundTransactionNo': None, 
            'refundTransactionMethods': 0, 
            'hotelId': 10042200, 
            'hotelName': '杭之逸酒店(杭州未来科技城海创园店)', 
            'hotelAddress': '仓前街道向往路1008号(乐富海邦园)', 
            'roomTypeName': '优选大床房', 
            'bedTypeName': '大床', 
            'ratePlanId': 'H4sIAAAAAAAEAEWQTUsCQRjHv0oMHRWenRxd95qXIEJEui7TOtbitCuzviQVdAm0Mj1lhw4dhKgOXSIyhL6Ms+Wpr9Azu0kwPMz85v/8n5dj0lRhx68JRZxChqgdfiiIQxbz2+XZQE8f9MdF3P8kGdJc/bwP9fg5njwi2xO1aq9paKpE1PWDWtj9o/Hd4OtpgjSq8JYoSx5slRALGQb7bpEW7GJho+gCAF1PWXI1wc2BbeVZLg8uuB0wtZTgjTqPWsZ3co8NLKdj5B4PPCErbYkF6epZEpGHOgqUZYFlLbZm2Q6AHgz1+fD7daZHN/Fb/2d+tZhd6vG1mWn0kkK0rCshNhOfbWw7alX9ZPJ/t2rihsfsRfmeKAtV4j3UWMxGJo7KXHHiBG0psaUD4TV2uWwbEwsgRynACTCLmZBHvR90QnRJt2aSTn8BcgtnVpcBAAA=', 
            'pricePerDay': '143', 
            'breakfastCountPerDay': None, 
            'breakfastDesc': '无早餐', 
            'cancelPolicyType': 2, 
            'cancelDesc': '2025-05-15 18:00前免费取消，之后不可取消', 
            'freeCancelLatestTime': '2025-05-15 18:00:00', 
            'confirmationNumber': None, 
            'contactName': '常高伟', 
            'contactMobile': '13800000000', 
            'contactEmail': None, 
            'payLimitTime': '2025-05-14 13:51:43', 
            'unFinishedReason': None, 
            'createTime': '2025-05-14 13:21:43', 
            'customerOrderNo': '202505141321420000000093'
        }, 
        'success': True, 
        'msg': '请求成功'
    }
    
    # Generate travel guide
    logging.info("Starting travel guide generation test...")
    logging.info(f"Using sample order for hotel: {sample_order['data']['hotelName']}")
    
    # Call the generator
    guide = await generate_travel_guide(order_detail=sample_order)
    
    # Display results
    logging.info("Travel Guide Generated:")
    logging.info(f"Title: {guide['title']}")
    logging.info(f"Type: {guide['type']}")
    logging.info(f"Hotel ID: {guide['hotelId']}")
    
    # Show preview of content
    content_preview = guide['content'][:500] + "..." if len(guide['content']) > 500 else guide['content']
    logging.info("Content preview:")
    logging.info(content_preview)
    
    # Show information about visited URLs
    if "visited_urls" in guide:
        logging.info(f"URLs visited: {len(guide['visited_urls'])}")
        for url in guide.get("visited_urls", [])[:5]:  # Show first 5 URLs
            logging.info(f"  - {url}")
    
    if "crawled_documents" in guide:
        logging.info(f"Crawled documents: {guide['crawled_documents']}")
    
    logging.info(f"Generated travel guide notification with ID: {guide['id']}")
    return guide

if __name__ == "__main__":
    set_log_color_level(logging.DEBUG)
    asyncio.run(main())
