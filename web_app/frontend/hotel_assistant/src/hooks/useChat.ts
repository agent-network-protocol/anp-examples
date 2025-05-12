import { useState } from 'react';
import { message } from 'antd';
import { SAMPLE_HOTELS } from '../constants/hotelData';

// 定义新的数据结构接口
export interface ChatResponse {
  summary: string;
  content: RoomInfo[] | string;
}

// 定义房间信息接口
export interface RoomInfo {
  roomTypeId: string;
  roomType: string;
  bedType: string;
  pricePerNight: number;
  images: string;
  available: boolean;
  hotel: {
    hotelId: string;
    hotelName: string;
    address: string;
    rating: number;
    price: string;
  };
}

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/';

export const useChat = () => {
  const [messages, setMessages] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  // 处理消息查询
  const handleSender = async (query: string) => {
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE_URL}/api/travel/hotel/query`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query }),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      let data = await response.json() as ChatResponse;
      console.log('------', data);
      data = {
        "checkInDate": "2025-05-13",
        "checkOutDate": "2025-05-14",
        "contactMobile": "13800000000",
        "contactName": "常高伟",
        "content": [
          {
            "available": true,
            "bedType": "1张1.5米大床",
            "hotel": {
              "address": "望京湖光中街8号1幢1-5层",
              "hotelID": "10000753",
              "hotelName": "全季酒店(北京望京店)",
              "price": "¥488-¥595",
              "rating": 5.0
            },
            "images": "https://pavo.elongstatic.com/i/Hotel1080_800/nw_KqIWAwZdfi.jpg",
            "orderAmount": 488.0,
            "pricePerNight": 488.0,
            "ratePlanID": "H4sIAAAAAAAEAEWQz0rDQBDGX0UWj63sJt005movgkgpxWtY062GrknZ9I9FPWpbtbYnc/HQQ0H0IqKo1YIv00315Cs4SSrCMuz+Zuab2e8I1aXfcitcIiufQXKbHXBkITW5Ve/nUe8TZVB9yaJxV3XP5h+vwHZ5pdypx5So2Zis0cXjU9oDybbrVfz2Mh/d9Bf3IdCgxBq8KJi3WQDMhe/t2QYmRDdN08YYG6spS65xsKmW041107Cx3SLxUMlZrcqCRiwbjqPw7nsyAu4wz+Gi1BQwT/t7FnjgQJ2GNZrFNEv0FWJaGKv+QJ0Ovp6nangdvfR+Zpfz6YUaXc3fBmr4kEKQrErONxKdLdg6aJTdxIJ/tXKiBic2SLoOL3JZYB2ooTkNGD8sMsmQ5TWFgJX2uVPbYaKZOAafw3mqH2NKkpCDetdr+aCSmhY3nfwCeV412JoBAAA=",
            "roomType": "大床房",
            "roomTypeId": "395312"
          },
          {
            "available": true,
            "bedType": "1张1.8米大床",
            "hotel": {
              "address": "望京湖光中街8号1幢1-5层",
              "hotelID": "10000753",
              "hotelName": "全季酒店(北京望京店)",
              "price": "¥488-¥595",
              "rating": 5.0
            },
            "images": "https://pavo.elongstatic.com/i/Hotel1080_800/nw_KqIZsiqdIk.jpg",
            "orderAmount": 524.0,
            "pricePerNight": 524.0,
            "ratePlanID": "H4sIAAAAAAAEAHVQTU/CQBD9Lw03ienyIZWEg6FCUCCI6MFLs7QLNF3bZltoi3rzgCQIF8WDiYaQEDXRGBNjUOOfoUX+hVs+jl4mM/Pem7x5J4xOtIYsIcLEY0GG5OExYuLM7OlmOh65w5E7bnutHybI6EuEtmUklRzdH4D7dQ/Wuenr24JKQUtWJc1a4t7txfSxT7dGEZqogKGa4ekaYU2tChssAGGO4wSWZUGghrFt2LIF1abg7JcjoGg59o6Y1ZO5WrIc2t7cSyQC/wGCDVMZ/iAlQaOgGFGzmpcdsamk0/qRsuZkzd0tYiZ5qZoDRiYhhPwfCIJKBRomtROafH57/YfZsEcBEaoiwsU6pv7BauSRIVLi7/PA7VzNBue08Vo9t33n9i4nHx23++J2r733FtVXCELJuShLXzbMkuzHptYxphkSWUQFRHjo0GtRzjeC7AIkcMUQa0hUDiGuz9OlwbCxaPiUjYJ5iVC+rDY0emURsC86+wPQG6vgwwEAAA==",
            "roomType": "高级大床房",
            "roomTypeId": "395308"
          },
          {
            "available": true,
            "bedType": "1张1.8米大床",
            "hotel": {
              "address": "望京湖光中街8号1幢1-5层",
              "hotelID": "10000753",
              "hotelName": "全季酒店(北京望京店)",
              "price": "¥488-¥595",
              "rating": 5.0
            },
            "images": "https://pavo.elongstatic.com/i/Hotel1080_800/nw_KqIVuNnTOM.jpg",
            "orderAmount": 595.0,
            "pricePerNight": 595.0,
            "ratePlanID": "H4sIAAAAAAAEADVPXUvCYBT+L++1yTt18+O23QQRItL92zzScG3yzmmS3VWY4QeELSgoRJASighErOjP7N3av+hs6s3hnOeL85M+eI1EWtaRogSH49RcQOPwCSJ/HtTA4u1uLpTeQ/yeGl9Hth94ekSH0JyPFZ6J0G86v42iG8BGY1Y6bEkx+P7Gsvnj/WMuQbFuO2Whv+OThevESIupVeBPKNnf2SggrO5pC9S5jKqVUpXpOTV0F8HqNe83UN/76ScLn5WSIhMEdA+yKb6Mj254l8Ax8/Hsdy/5oOb7AJQmGsvcohzfxvC8Hb3Jwl3wGqK8JgN2VaB9DeM2qlZZyfNvGhsIyoAyixDvolme5LCugBE7LXPDtk3EMRv2Q2/6qMkamBU3pUo2tRprdcloNNFq3TkXn/4e8t/BkAQAA=",
            "roomType": "零压-高级大床房",
            "roomTypeId": "9570709"
          }
        ],
        "guestNames": [
          "顾客名字"
        ],
        "summary": "根据您的偏好，我们为您推荐位于北京望京的全季酒店(北京望京店)，这是一家华住集团旗下的舒适型中档酒店，提供免费Wi-Fi、大床房及多项贴心服务，交通便利，周边配套完善。我们为您精选了三种大床房房型，房价区间488–595元，均为预付即订即住，部分含早餐，满足您对大床房和高性价比的需求。"
      };
      // 根据返回的数据结构处理消息
      setMessages(prev => [
        ...prev,
        { role: 'user', content: query },
        {
          role: 'assistant',
          content: data,
          isHotelData: Array.isArray(data.content)
        }
      ]);
    } catch (error) {
      console.error('Error:', error);
      message.error('请求失败，请稍后重试。');

      // 使用示例数据进行测试
      const mockData: ChatResponse = {
        summary: "这是我们为你推荐的位于北京三里屯附近的经济型酒店房型",
        content: [
          {
            roomTypeId: "RT12345",
            roomType: "标准大床房",
            bedType: "大床",
            pricePerNight: 399,
            images: "https://images.unsplash.com/photo-1566073771259-6a8506099945?ixlib=rb-4.0.3&auto=format&fit=crop&w=1170&q=80",
            available: true,
            hotel: {
              hotelId: "H98765",
              hotelName: "全季酒店(北京三里屯店)",
              address: "北京市朝阳区三里屯路5号",
              rating: 4.5,
              price: "¥350-¥500"
            }
          },
          {
            roomTypeId: "RT12346",
            roomType: "舒适双床房",
            bedType: "双床",
            pricePerNight: 429,
            images: "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?ixlib=rb-4.0.3&auto=format&fit=crop&w=1170&q=80",
            available: true,
            hotel: {
              hotelId: "H98766",
              hotelName: "如家酒店(北京工体店)",
              address: "北京市朝阳区工人体育场北路2号",
              rating: 4.2,
              price: "¥300-¥450"
            }
          }
        ]
      };

      setMessages(prev => [
        ...prev,
        { role: 'user', content: query },
        {
          role: 'assistant',
          content: mockData,
          isHotelData: Array.isArray(mockData.content)
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  // 提交消息
  const onSubmit = (val: string) => {
    if (!val) return;

    if (loading) {
      message.error('请求正在进行中，请等待请求完成。');
      return;
    }

    handleSender(val);
  };

  return {
    loading,
    messages,
    setMessages,
    onSubmit,
  };
};
