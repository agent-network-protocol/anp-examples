# 酒店订单API接口文档

本文档提供了酒店订单相关API的详细描述，包括创建并支付酒店订单、查询酒店订单详情等功能。

## 目录

- [酒店房型查询](#酒店房型查询)
- [创建并支付酒店订单](#创建并支付酒店订单)
- [查询酒店订单详情](#查询酒店订单详情)

## 酒店房型查询

该接口用于查询酒店房型信息，根据用户输入的查询条件返回推荐的酒店房型。

### 接口地址

```
POST /api/travel/hotel/query
```

### 请求参数

| 参数名 | 类型 | 是否必须 | 描述 |
| ----- | ---- | ------- | --- |
| query | string | 是 | 用户查询的内容，例如："我想在北京找一家三星级以上的酒店" |
| agent_url | string | 否 | 代理URL，默认为"https://agent-search.ai/ad.json" |
| max_documents | int | 否 | 最大查询文档数量，默认为20 |

### 请求示例

```json
{
  "query": "我想在北京三里屯附近找一家经济型酒店，价格在300-500元之间",
  "agent_url": "https://agent-search.ai/ad.json",
  "max_documents": 20
}
```

### 响应参数

| 参数名 | 类型 | 描述 |
| ----- | ---- | --- |
| summary | string | 查询结果的简要总结 |
| content | array | 推荐的酒店房型列表，最多返回三个房型 |

### 成功响应示例

```json
{
  "summary": "这是我们为你推荐的位于北京三里屯附近的经济型酒店房型",
  "content": [
    {
      "roomTypeId": "RT12345",
      "roomType": "标准大床房",
      "bedType": "大床",
      "pricePerNight": 399,
      "images": "https://example.com/images/room1.jpg",
      "available": true,
      "hotel": {
        "hotelId": "H98765",
        "hotelName": "全季酒店(北京三里屯店)",
        "address": "北京市朝阳区三里屯路5号",
        "rating": 4.5,
        "price": "¥350-¥500"
      }
    },
    {
      "roomTypeId": "RT12346",
      "roomType": "舒适双床房",
      "bedType": "双床",
      "pricePerNight": 429,
      "images": "https://example.com/images/room2.jpg",
      "available": true,
      "hotel": {
        "hotelId": "H98766",
        "hotelName": "如家酒店(北京工体店)",
        "address": "北京市朝阳区工人体育场北路2号",
        "rating": 4.2,
        "price": "¥300-¥450"
      }
    }
  ]
}
```

### 失败响应示例

```json
{
  "summary": "很抱歉，查询过程中出现错误",
  "content": "无法完成酒店查询：连接超时"
}
```

### 处理逻辑

1. 调用酒店查询接口，根据用户输入进行智能搜索
2. 分析搜索结果，推荐最佳匹配的酒店房型（最多三个）
3. 返回格式化的酒店房型信息

## 创建并支付酒店订单

该接口用于创建酒店订单并完成支付，包括创建订单和支付两个步骤。

### 接口地址

```
POST /api/travel/hotel/order/create_and_pay
```

### 请求参数

| 参数名 | 类型 | 是否必须 | 描述 |
| ----- | ---- | ------- | --- |
| hotelID | int | 是 | 酒店ID |
| ratePlanID | string | 是 | 产品（价格计划）ID |
| roomNum | int | 是 | 房间数量 |
| checkInDate | string | 是 | 入住日期（格式：yyyy-MM-dd） |
| checkOutDate | string | 是 | 离店日期（格式：yyyy-MM-dd） |
| guestNames | array | 是 | 房客姓名，每个房间预留一个房客姓名 |
| orderAmount | float | 是 | 订单总金额 |
| contactName | string | 是 | 订单联系人姓名 |
| contactMobile | string | 是 | 订单联系人手机号 |
| arriveTime | string | 否 | 最晚到店时间，如：2020-07-27 16:00 |
| contactEmail | string | 否 | 订单联系人邮箱 |
| orderRemark | string | 否 | 用户备注信息 |
| callBackUrl | string | 否 | 订单状态变更异步回调地址 |
| paymentType | int | 是 | 支付方式(2=支付宝, 3=微信) |

### 请求示例

```json
{
  "hotelID": 12345,
  "ratePlanID": "RPL98765",
  "roomNum": 1,
  "checkInDate": "2025-05-20",
  "checkOutDate": "2025-05-22",
  "guestNames": ["张三"],
  "orderAmount": 698.00,
  "contactName": "张三",
  "contactMobile": "13800138000",
  "arriveTime": "2025-05-20 14:00",
  "contactEmail": "zhangsan@example.com",
  "orderRemark": "希望安排高层安静房间",
  "callBackUrl": "https://example.com/callback",
  "paymentType": 2
}
```

### 响应参数

| 参数名 | 类型 | 描述 |
| ----- | ---- | --- |
| success | boolean | 请求是否成功 |
| msg | string | 请求结果消息 |
| data | object | 响应数据 |
| data.orderNo | string | 订单号 |
| data.paymentInfo | object | 支付信息 |

### 成功响应示例

```json
{
  "success": true,
  "msg": "酒店订单创建并支付成功",
  "data": {
    "orderNo": "HO202505111627001",
    "paymentInfo": {
      "paymentUrl": "https://payment.example.com/pay/HO202505111627001",
      "qrCodeUrl": "https://payment.example.com/qrcode/HO202505111627001"
    }
  }
}
```

### 失败响应示例

```json
{
  "success": false,
  "msg": "创建酒店订单失败: 库存不足",
  "data": null
}
```

或

```json
{
  "success": false,
  "msg": "支付酒店订单失败: 支付超时",
  "data": {
    "orderNo": "HO202505111627001",
    "createOrderSuccess": true,
    "payOrderSuccess": false
  }
}
```

### 处理逻辑

1. 调用创建酒店订单接口
2. 如果创建成功，调用支付接口
3. 返回支付结果信息

## 查询酒店订单详情

该接口用于查询已创建的酒店订单详情。

### 接口地址

```
POST /api/travel/hotel/order/get_detail
```

### 请求参数

| 参数名 | 类型 | 是否必须 | 描述 |
| ----- | ---- | ------- | --- |
| customerOrderNo | string | 是 | 酒店预订的订单号，用于查询订单详情 |

### 请求示例

```json
{
  "customerOrderNo": "HO202505111627001"
}
```

### 响应参数

| 参数名 | 类型 | 描述 |
| ----- | ---- | --- |
| success | boolean | 请求是否成功 |
| msg | string | 请求结果消息 |
| data | object | 订单详情数据 |

### 成功响应示例

```json
{
  "success": true,
  "msg": "查询酒店订单详情成功",
  "data": {
    "orderNo": "HO202505111627001",
    "hotelName": "示例酒店",
    "hotelAddress": "北京市海淀区示例路123号",
    "roomType": "豪华大床房",
    "checkInDate": "2025-05-20",
    "checkOutDate": "2025-05-22",
    "roomNum": 1,
    "guestNames": ["张三"],
    "contactName": "张三",
    "contactMobile": "13800138000",
    "orderAmount": 698.00,
    "orderStatus": "已支付",
    "paymentType": "支付宝",
    "createTime": "2025-05-11 16:27:30"
  }
}
```

### 失败响应示例

```json
{
  "success": false,
  "msg": "查询酒店订单详情失败: 订单不存在",
  "data": null
}
```

### 处理逻辑

1. 调用酒店订单详情接口
2. 返回订单详情信息

## 错误码说明

当API调用出现错误时，会返回相应的错误信息和状态码：

| HTTP状态码 | 说明 |
| --------- | --- |
| 200 | 请求成功，但业务处理可能失败，具体见响应的success字段 |
| 400 | 请求参数错误 |
| 500 | 服务器内部错误 |

## 注意事项

1. 所有日期格式均为`yyyy-MM-dd`
2. 最晚到店时间格式为`yyyy-MM-dd HH:mm`
3. 支付方式目前仅支持支付宝(2)和微信(3)
4. 创建订单后，若支付失败，订单将保持未支付状态
5. 回调URL必须能够接收POST请求，并处理订单状态变更通知
