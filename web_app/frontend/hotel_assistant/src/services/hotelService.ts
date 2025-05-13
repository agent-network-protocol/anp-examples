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
      // Add the field used by the backend API
      qrCodeImageUrl?: string;
      customerOrderNo?: string;
      paymentType?: number;
      orderAmount?: string;
    };
  } | null;
}

interface GetHotelOrderDetailParams {
  customerOrderNo: string;
}

interface HotelOrderDetailResponse {
  success: boolean;
  msg: string;
  data: {
    // Basic order information
    customerOrderNo: string;
    orderAmount: number;
    createTime: string;
    payLimitTime?: string;
    
    // Hotel and room details
    hotelId: number;
    hotelName: string;
    hotelAddress: string;
    roomTypeName: string;
    bedTypeName: string;
    ratePlanId: string;
    pricePerDay: string;
    
    // Check-in information
    checkInDate: string;
    checkOutDate: string;
    numberOfNights: number;
    numberOfRooms: number;
    guestNames: string | string[];
    
    // Contact information
    contactName: string;
    contactMobile: string;
    contactEmail?: string;
    
    // Payment status
    payStatus: number; // 0: unpaid, 1: paid
    orderStatus: number; // Order status code
    paymentType: number; // Payment method code
    payTime?: string; // Payment time if paid
    
    // Other fields
    breakfastDesc?: string;
    cancelDesc?: string;
    freeCancelLatestTime?: string;
    arriveTime?: string;
    remark?: string;
  } | null;
}

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/';
const USE_MOCK = import.meta.env.VITE_USE_MOCK === 'true';

export const createAndPayHotelOrder = async (params: CreateHotelOrderParams): Promise<HotelOrderResponse> => {
  // // 独立mock开关
  // if (USE_MOCK) {
  //   return {
  //     success: true,
  //     msg: '酒店订单创建并支付成功',
  //     data: {
  //       orderNo: 'MOCK202406010001',
  //       paymentInfo: {
  //         paymentUrl: 'https://mock-payment-url.com/pay/MOCK202406010001',
  //         qrCodeUrl: 'https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=MOCK202406010001',
  //       },
  //     },
  //   };
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
  //     success: true,
  //     msg: '查询酒店订单详情成功',
  //     data: {
  //       orderNo: params.customerOrderNo,
  //       hotelName: '全季酒店(北京三里屯店)',
  //       hotelAddress: '北京市朝阳区三里屯路5号',
  //       roomType: '标准大床房',
  //       checkInDate: '2025-05-20',
  //       checkOutDate: '2025-05-22',
  //       roomNum: 1,
  //       guestNames: ['张三'],
  //       contactName: '张三',
  //       contactMobile: '13800138000',
  //       orderAmount: 698.00,
  //       orderStatus: '已支付',
  //       paymentType: '支付宝',
  //       createTime: '2025-05-11 16:27:30',
  //     },
  //   };
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