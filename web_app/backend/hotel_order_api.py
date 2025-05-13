import logging
import requests
from pathlib import Path
import os
import json
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union
import sys

# Import hotel_crawler function
sys_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if sys_path not in sys.path:
    sys.path.append(sys_path)
from anp_examples.hotel_crawler import hotel_crawler

# Get project root directory
BASE_DIR = Path(__file__).resolve().parent.parent
ROOT_DIR = Path(__file__).resolve().parent.parent.parent

# Get DID paths
did_document_path = str(ROOT_DIR / "use_did_test_public/did.json")
private_key_path = str(ROOT_DIR / "use_did_test_public/key-1_private.pem")


# 创建路由器
router = APIRouter()

# 定义创建酒店订单请求模型
class GuestName(BaseModel):
    name: str

# 定义酒店订单支付请求模型
class PayHotelOrderRequest(BaseModel):
    customerOrderNo: str = Field(..., description="商户订单号，用于标识要支付的订单")
    paymentType: int = Field(..., description="支付方式(2=支付宝, 3=微信)", ge=2, le=3)

# 定义创建并支付酒店订单请求模型
class CreateAndPayHotelOrderRequest(BaseModel):
    # 包含创建订单的所有字段
    hotelID: int = Field(..., description="酒店ID")
    ratePlanID: str = Field(..., description="产品（价格计划）ID")
    roomNum: int = Field(..., description="房间数量")
    checkInDate: str = Field(..., description="入住日期（格式：yyyy-MM-dd）")
    checkOutDate: str = Field(..., description="离店日期（格式：yyyy-MM-dd）")
    guestNames: List[str] = Field(..., description="房客姓名，每个房间预留一个房客姓名")
    orderAmount: float = Field(..., description="订单总金额")
    contactName: str = Field(..., description="订单联系人姓名")
    contactMobile: str = Field(..., description="订单联系人手机号")
    arriveTime: Optional[str] = Field(None, description="最晚到店时间，如：2020-07-27 16:00")
    contactEmail: Optional[str] = Field(None, description="订单联系人邮箱")
    orderRemark: Optional[str] = Field(None, description="用户备注信息")
    callBackUrl: Optional[str] = Field(None, description="订单状态变更异步回调地址")
    
    # 支付相关字段
    paymentType: int = Field(..., description="支付方式(2=支付宝, 3=微信)", ge=2, le=3)

# 定义响应模型
class CreateAndPayHotelOrderResponse(BaseModel):
    success: bool = Field(..., description="请求是否成功")
    msg: str = Field(..., description="请求结果消息")
    data: Optional[dict] = Field(None, description="响应数据")

# 定义酒店订单详情请求模型
class HotelOrderDetailRequest(BaseModel):
    customerOrderNo: str = Field(..., description="酒店预订的订单号，用于查询订单详情")

# 定义酒店订单详情响应模型
class HotelOrderDetailResponse(BaseModel):
    success: bool = Field(..., description="请求是否成功")
    msg: str = Field(..., description="请求结果消息")
    data: Optional[Dict[str, Any]] = Field(None, description="订单详情数据")
    
# 定义酒店查询请求模型
class HotelQueryRequest(BaseModel):
    query: str = Field(..., description="用户查询的内容，例如：'我想在北京找一家三星级以上的酒店'")
    agent_url: Optional[str] = Field("https://agent-search.ai/ad.json", description="代理URL")
    max_documents: Optional[int] = Field(20, description="最大查询文档数量")

# 定义酒店查询响应模型
class HotelQueryResponse(BaseModel):
    summary: str = Field(..., description="查询结果的简要总结")
    content: Union[List[Dict[str, Any]], str] = Field(..., description="推荐的酒店房型列表或错误信息")
    # 添加额外字段以支持前端所需功能
    checkInDate: Optional[str] = Field(None, description="入住日期")
    checkOutDate: Optional[str] = Field(None, description="离店日期")
    contactName: Optional[str] = Field(None, description="联系人姓名")
    contactMobile: Optional[str] = Field(None, description="联系人手机号")
    guestNames: Optional[List[str]] = Field(None, description="入住人姓名列表")
    roomNum: Optional[int] = Field(None, description="房间数量")

@router.post("/api/travel/hotel/order/create_and_pay", response_model=CreateAndPayHotelOrderResponse)
async def create_and_pay_hotel_order(request: CreateAndPayHotelOrderRequest):
    """
    创建并支付酒店订单接口
    
    1. 首先调用创建酒店订单接口
    2. 如果创建成功，调用支付接口
    3. 返回支付结果信息
    """
    logging.info("Received create and pay hotel order request")
    
    try:
        # 1. 创建酒店订单
        create_order_url = "https://agent-connect.ai/agents/travel/hotel/api/create_order/ph"
        
        # 准备创建订单的请求数据
        create_order_data = {
            "hotelID": request.hotelID,
            "ratePlanID": request.ratePlanID,
            "roomNum": request.roomNum,
            "checkInDate": request.checkInDate,
            "checkOutDate": request.checkOutDate,
            "guestNames": request.guestNames,
            "orderAmount": request.orderAmount,
            "contactName": request.contactName,
            "contactMobile": request.contactMobile
        }
        
        # 添加可选字段
        if request.arriveTime:
            create_order_data["arriveTime"] = request.arriveTime
        if request.contactEmail:
            create_order_data["contactEmail"] = request.contactEmail
        if request.orderRemark:
            create_order_data["orderRemark"] = request.orderRemark
        if request.callBackUrl:
            create_order_data["callBackUrl"] = request.callBackUrl
            
        logging.info("Calling create hotel order API with data: %s", create_order_data)
        
        # 发送创建订单请求
        create_order_response = requests.post(create_order_url, json=create_order_data)
        create_order_result = create_order_response.json()
        
        logging.info("Create hotel order API response: %s", create_order_result)
        
        # 检查创建订单是否成功
        if not create_order_result.get("success", False):
            logging.error("Failed to create hotel order: %s", create_order_result.get("msg", "Unknown error"))
            return {
                "success": False,
                "msg": f"创建酒店订单失败: {create_order_result.get('msg', '未知错误')}",
                "data": None
            }
        
        # 获取订单号
        order_no = create_order_result.get("data", {}).get("orderNo")
        
        if not order_no:
            logging.error("Order number not found in create order response")
            return {
                "success": False,
                "msg": "创建订单成功但未获取到订单号",
                "data": None
            }
            
        # 2. 支付酒店订单
        pay_order_url = "https://agent-connect.ai/agents/travel/hotel/api/pay_order/ph"
        
        # 准备支付订单的请求数据
        pay_order_data = {
            "customerOrderNo": order_no,
            "paymentType": request.paymentType
        }
        
        logging.info("Calling pay hotel order API with data: %s", pay_order_data)
        
        # 发送支付订单请求
        pay_order_response = requests.post(pay_order_url, json=pay_order_data)
        pay_order_result = pay_order_response.json()
        
        logging.info("Pay hotel order API response: %s", pay_order_result)
        
        # 检查支付是否成功
        if not pay_order_result.get("success", False):
            logging.error("Failed to pay hotel order: %s", pay_order_result.get("msg", "Unknown error"))
            return {
                "success": False,
                "msg": f"支付酒店订单失败: {pay_order_result.get('msg', '未知错误')}",
                "data": {
                    "orderNo": order_no,
                    "createOrderSuccess": True,
                    "payOrderSuccess": False
                }
            }
        
        # 3. 返回成功结果
        return {
            "success": True,
            "msg": "酒店订单创建并支付成功",
            "data": {
                "orderNo": order_no,
                "paymentInfo": pay_order_result.get("data", {})
            }
        }
        
    except Exception as e:
        logging.error(f"Error in create and pay hotel order: {str(e)}")
        raise HTTPException(status_code=500, detail=f"处理酒店订单创建和支付请求时发生错误: {str(e)}")

@router.post("/api/travel/hotel/order/get_detail", response_model=HotelOrderDetailResponse)
async def get_hotel_order_detail(request: HotelOrderDetailRequest):
    """
    查询酒店订单详情接口
    
    1. 调用酒店订单详情接口
    2. 返回订单详情信息
    """
    logging.info("Received get hotel order detail request")
    
    try:
        # 调用酒店订单详情接口
        order_detail_url = "https://agent-connect.ai/agents/travel/hotel/api/get_order_detail/ph"
        
        # 准备查询订单详情的请求数据
        order_detail_data = {
            "customerOrderNo": request.customerOrderNo
        }
        
        logging.info("Calling get hotel order detail API with data: %s", order_detail_data)
        
        # 发送查询订单详情请求
        order_detail_response = requests.post(order_detail_url, json=order_detail_data)
        order_detail_result = order_detail_response.json()
        
        logging.info("Get hotel order detail API response: %s", order_detail_result)
        
        # 检查查询订单详情是否成功
        if not order_detail_result.get("success", False):
            logging.error("Failed to get hotel order detail: %s", order_detail_result.get("msg", "Unknown error"))
            return {
                "success": False,
                "msg": f"查询酒店订单详情失败: {order_detail_result.get('msg', '未知错误')}",
                "data": None
            }
        
        # 返回成功结果
        return {
            "success": True,
            "msg": "查询酒店订单详情成功",
            "data": order_detail_result.get("data", {})
        }
        
    except Exception as e:
        logging.error(f"Error in get hotel order detail: {str(e)}")
        raise HTTPException(status_code=500, detail=f"处理酒店订单详情查询请求时发生错误: {str(e)}")


@router.post("/api/travel/hotel/query", response_model=HotelQueryResponse)
async def query_hotel(request: HotelQueryRequest):
    """
    酒店房型查询接口
    
    1. 调用酒店查询接口，根据用户输入进行智能搜索
    2. 分析搜索结果，推荐最佳匹配的酒店房型（最多三个）
    3. 返回格式化的酒店房型信息
    """
    logging.info("Received hotel query request: %s", request.query)

    mock = '''
{
    "checkInDate": "2025-05-15",
    "checkOutDate": "2025-05-16",
    "contactMobile": "13800000000",
    "contactName": "常高伟",
    "content": [
        {
            "available": true,
            "bedType": "大床",
            "hotel": {
                "address": "仓前街道向往路1008号(乐富海邦园)",
                "hotelID": "10042200",
                "hotelName": "杭之逸酒店(杭州未来科技城海创园店)",
                "price": "¥219起",
                "rating": "5.0"
            },
            "images": "https://pavo.elongstatic.com/i/Hotel1080_800/nw_1jlFDLjh2wM.jpg",
            "orderAmount": 143.0,
            "pricePerNight": 143.0,
            "ratePlanID": "H4sIAAAAAAAEAEWQTUsCQRjHv0oMHRWenRxd95qXIEJEui7TOtbitCuzviQVdAm0Mj1lhw4dhKgOXSIyhL6Ms+Wpr9Azu0kwPMz85v/8n5dj0lRhx68JRZxChqgdfiiIQxbz2+XZQE8f9MdF3P8kGdJc/bwP9fg5njwi2xO1aq9paKpE1PWDWtj9o/Hd4OtpgjSq8JYoSx5slRALGQb7bpEW7GJho+gCAF1PWXI1wc2BbeVZLg8uuB0wtZTgjTqPWsZ3co8NLKdj5B4PPCErbYkF6epZEpGHOgqUZYFlLbZm2Q6AHgz1+fD7daZHN/Fb/2d+tZhd6vG1mWn0kkK0rCshNhOfbWw7alX9ZPJ/t2rihsfsRfmeKAtV4j3UWMxGJo7KXHHiBG0psaUD4TV2uWwbEwsgRynACTCLmZBHvR90QnRJt2aSTn8BcgtnVpcBAAA=",
            "roomType": "优选大床房",
            "roomTypeId": "562616256"
        },
        {
            "available": true,
            "bedType": "1张大床",
            "hotel": {
                "address": "仓前街道向往路1008号(乐富海邦园)",
                "hotelID": "10042200",
                "hotelName": "杭之逸酒店(杭州未来科技城海创园店)",
                "price": "¥219起",
                "rating": "5.0"
            },
            "images": "https://pavo.elongstatic.com/i/Hotel1080_800/nw_1jlFe2Lzila.jpg",
            "orderAmount": 164.0,
            "pricePerNight": 164.0,
            "ratePlanID": "H4sIAAAAAAAEADVQTUsCQRj+L4vHDjOzjrN6zUsQISJdl2kdcXFcZXbXjz4g6AMVTC+2lyARIepQ0CEqov5Ms+a/6F0/LsM7z8c7zzwnRlM1Wm5ZKCPHdgx1wOvCyBmL1+/leV/PH/TnIO79GDtGc8PoyXUcXS36H/HFFOAjUS51mwmB9dd0bQC47XrlRnvDxHf9xVMEqF/kgShI7u3lAa5K2fHrwg1C7tmYUGJRkxFkm5SyNMUsVTm2swRZDGGc2g6A4Ewmi0xmMsuyURJBCV6rcD9InoqmcfS4nI8Bd7jnCFkMJWTA22te+A7o/p5nejhZzi5hiHtjPbjX45vf96EevejRbfzWA39FCbG7Mu1DbD8ouUkBXigltKFcRxSEyvNu8nWLgF50ClzxrcKpCqd2yGW46gahNCEInSKKaXJkQO96rQZsWZeUmM7+AR1NfPGNAQAA",
            "roomType": "精选大床房",
            "roomTypeId": "482524738"
        },
        {
            "available": true,
            "bedType": "1张大床",
            "hotel": {
                "address": "仓前街道向往路1008号(乐富海邦园)",
                "hotelID": "10042200",
                "hotelName": "杭之逸酒店(杭州未来科技城海创园店)",
                "price": "¥219起",
                "rating": "5.0"
            },
            "images": "https://pavo.elongstatic.com/i/Hotel1080_800/nw_1jlHmNjCuaY.jpg",
            "orderAmount": 184.0,
            "pricePerNight": 184.0,
            "ratePlanID": "H4sIAAAAAAAEAD2QyUoDQRCG36XxmEPPOGuu5iKIhBC8hnamgkPGSejJYlxOLiSBLJc4l4BDCIg5KF5ERfBl7I55C6uzeGmqv6r/r+WC1Hi1GfjASdbOEH7IToFkye/rXPQHYvYoPnuy800ypLbJiPGdTG4X3Q95nSI+Br/YrqmEJr7StQBxK4j8amuTkZPuYp4gjQusDvmQRfs5xOXzkm24pq6bRsnVNY1Squ0g/I+3gSKW5bi7jm07TomqthxYpcziurJPUpk8LWcj5B6LPAgLjRD7attvDmJP7fQ8Ff3xcnqDgeyMRO9BjAY/730xfBHDe/nWQX2ZA+ytRAc4alwvBmrpqBGGeAEeeJAHnmNtdNOpgfVwlmecbSu8E/AqRyxsrO5BqaHrlF5SUzPVY2F9EDWr6LI+jBJd/QF/ETJugQEAAA==",
            "roomType": "豪华大床房",
            "roomTypeId": "482524739"
        }
    ],
    "guestNames": [
        "常高伟"
    ],
    "roomNum": 1,
    "summary": "这是我们为您推荐的位于杭州未来科技城的杭之逸酒店(杭州未来科技城海创园店)，以下是三款可订的大床房型，性价比高且有充足空房。"
}
    
    '''

    # 将模拟数据转换为字典
    mock_data = json.loads(mock)
    return mock_data

    
    try:

        # Use agent URL provided by user or default URL
        initial_url = (
            request.agent_url
            if request.agent_url
            else "https://agent-search.ai/ad.json"
        )
        
        logging.info(f"The query is {request.query}")

        # Call hotel_crawler function
        result = await hotel_crawler(
            user_input=request.query
            # task_type="hotel_booking",
            # did_document_path=did_document_path,
            # private_key_path=private_key_path,
            # max_documents=20,
            # initial_url=initial_url
        )
        
        logging.info("Hotel crawler query completed successfully")
            
        # Return the successful result
        if isinstance(result, dict) and 'summary' in result and 'content' in result:
            # 如果结果已经包含必需字段，直接返回
            return result
        else:
            # 确保返回符合模型要求的结构
            return {
                "summary": result.get("summary", "暂未找到合适的房型"),
                "content": result.get("content", []),
                "contactName": result.get("contactName", ""),
                "contactMobile": result.get("contactMobile", ""),
                "checkInDate": result.get("checkInDate", ""),
                "checkOutDate": result.get("checkOutDate", ""),
                "guestNames": result.get("guestNames", [""]),
                "roomNum": result.get("roomNum", 1)
            }
        
    except Exception as e:
        logging.error(f"Error in hotel query: {str(e)}")
        return {
            "summary": "很抱歉，处理查询请求时出现系统错误",
            "content": f"处理酒店查询请求时发生错误: {str(e)}"
        }

