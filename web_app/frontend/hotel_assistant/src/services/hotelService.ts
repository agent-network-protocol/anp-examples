interface CreateHotelOrderParams {
  hotelID: number | string;
  ratePlanID: string;
  roomNum: number;
  checkInDate: string;
  checkOutDate: string;
  guestNames: string[];
  orderAmount: number;
  contactName: string;
  contactMobile: string;
  arriveTime?: string;
  contactEmail?: string;
  orderRemark?: string;
  callBackUrl?: string;
  paymentType: number;
}

interface HotelOrderResponse {
  success: boolean;
  msg: string;
  data: {
    orderNo: string;
    paymentInfo: {
      paymentUrl?: string;
      qrCodeUrl?: string;
      qrCodeImageUrl?: string;
    };
  } | null;
}

interface GetHotelOrderDetailParams {
  customerOrderNo: string;
}

interface HotelOrderDetailResponse {
  success: boolean;
  msg: string;
  data: any;
}

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/';
const USE_MOCK = import.meta.env.VITE_USE_MOCK === 'true';

export const createAndPayHotelOrder = async (params: CreateHotelOrderParams): Promise<HotelOrderResponse> => {
  // 独立mock开关
  // if (USE_MOCK) {
  //   return {
  //     "success": true,
  //     "msg": "酒店订单创建并支付成功",
  //     "data": {
  //       "orderNo": "202505140017450000000084",
  //       "paymentInfo": {
  //         // "customerOrderNo": "202505140017450000000084",
  //         "qrCodeImageUrl": "https://agent-connect.ai/agents/travel/hotel/static/qrcodes/202505140017450000000084.png",
  //         // "paymentType": 2,
  //         // "orderAmount": "143.00"
  //       }
  //     }
  //   }
  // }
  try {
    const response = await fetch(`${API_BASE_URL}/api/travel/hotel/order/create_and_pay`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(params),
    });
    const data = await response.json();
    return data;
  } catch (error: any) {
    throw error;
  }
};

export const getHotelOrderDetail = async (params: GetHotelOrderDetailParams): Promise<HotelOrderDetailResponse> => {
  // if (USE_MOCK) {
  //   return {
  //     "success": true,
  //     "msg": "查询酒店订单详情成功",
  //     "data": {
  //       "numberOfRooms": 1,
  //       "numberOfNights": 1,
  //       "arriveTime": null,
  //       "checkInDate": "2025-05-15 00:00:00",
  //       "checkOutDate": "2025-05-16 00:00:00",
  //       "guestNames": "常高伟",
  //       "remark": "",
  //       "orderAmount": 143.0,
  //       "orderStatus": 2,
  //       "payStatus": 1,
  //       "payTime": "2025-05-14 00:18:09",
  //       "paymentType": 1,
  //       "transactionNo": "202505140018096076631414",
  //       "refundAmount": null,
  //       "refundSuccessTime": null,
  //       "refundTransactionNo": null,
  //       "refundTransactionMethods": 0,
  //       "hotelId": 10042200,
  //       "hotelName": "杭之逸酒店(杭州未来科技城海创园店)",
  //       "hotelAddress": "仓前街道向往路1008号(乐富海邦园)",
  //       "roomTypeName": "优选大床房",
  //       "bedTypeName": "大床",
  //       "ratePlanId": "H4sIAAAAAAAEAEWQTUsCQRjHv0oMHRWenRxd95qXIEJEui7TOtbitCuzviQVdAm0Mj1lhw4dhKgOXSIyhL6Ms+Wpr9Azu0kwPMz85v/8n5dj0lRhx68JRZxChqgdfiiIQxbz2+XZQE8f9MdF3P8kGdJc/bwP9fg5njwi2xO1aq9paKpE1PWDWtj9o/Hd4OtpgjSq8JYoSx5slRALGQb7bpEW7GJho+gCAF1PWXI1wc2BbeVZLg8uuB0wtZTgjTqPWsZ3co8NLKdj5B4PPCErbYkF6epZEpGHOgqUZYFlLbZm2Q6AHgz1+fD7daZHN/Fb/2d+tZhd6vG1mWn0kkK0rCshNhOfbWw7alX9ZPJ/t2rihsfsRfmeKAtV4j3UWMxGJo7KXHHiBG0psaUD4TV2uWwbEwsgRynACTCLmZBHvR90QnRJt2aSTn8BcgtnVpcBAAA=",
  //       "pricePerDay": "143",
  //       "breakfastCountPerDay": null,
  //       "breakfastDesc": "无早餐",
  //       "cancelPolicyType": 2,
  //       "cancelDesc": "2025-05-15 18:00前免费取消，之后不可取消",
  //       "freeCancelLatestTime": "2025-05-15 18:00:00",
  //       "confirmationNumber": null,
  //       "contactName": "常高伟",
  //       "contactMobile": "13800000000",
  //       "contactEmail": null,
  //       "payLimitTime": "2025-05-14 00:47:45",
  //       "unFinishedReason": null,
  //       "createTime": "2025-05-14 00:17:45",
  //       "customerOrderNo": "202505140017450000000084"
  //     }
  //   }
  // }
  try {
    const response = await fetch(`${API_BASE_URL}/api/travel/hotel/order/get_detail`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(params),
    });
    const data = await response.json();
    return data;
  } catch (error: any) {
    throw error;
  }
};

// Notification types
export interface Notification {
  id: string;
  type: string;
  title: string;
  content: string;
  timestamp: string;
  read: boolean;
}

export interface NotificationsResponse {
  has_notification: boolean;
  notifications: Notification[];
}

// Get notifications API function
export const getNotifications = async (): Promise<NotificationsResponse> => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/travel/hotel/notifications`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    const data = await response.json();
    return data;
  } catch (error: any) {
    console.error('Error fetching notifications:', error);
    // Return empty notifications in case of error
    return {
      has_notification: false,
      notifications: [],
    };
  }
}; 