// 酒店信息接口
export interface HotelInfo {
  id: string;
  name: string;
  address: string;
  price: number;
  rating: number;
  images: string[];
  description: string;
  amenities: string[];
}

// 示例酒店数据
export const SAMPLE_HOTELS = [
  {
    id: 'hotel-001',
    name: '海景豪华酒店',
    address: '北京市朝阳区建国路88号',
    price: 888,
    rating: 4.8,
    images: [
      'https://images.unsplash.com/photo-1566073771259-6a8506099945?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1170&q=80',
      'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1170&q=80',
      'https://images.unsplash.com/photo-1611892440504-42a792e24d32?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1170&q=80'
    ],
    description: '位于市中心的五星级豪华酒店，拥有壮观的城市景观和一流的服务。',
    amenities: ['免费WiFi', '游泳池', '健身中心', '餐厅', '会议室', '停车场', '24小时前台']
  },
  {
    id: 'hotel-002',
    name: '商务精品酒店',
    address: '上海市浦东新区陆家嘴环路1088号',
    price: 668,
    rating: 4.5,
    images: [
      'https://images.unsplash.com/photo-1578683010236-d716f9a3f461?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1170&q=80',
      'https://images.unsplash.com/photo-1590490360182-c33d57733427?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1074&q=80',
      'https://images.unsplash.com/photo-1566665797739-1674de7a421a?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1074&q=80'
    ],
    description: '为商务旅行者设计的精品酒店，提供高效的服务和舒适的住宿体验。',
    amenities: ['免费WiFi', '商务中心', '会议室', '健身房', '餐厅', '洗衣服务']
  },
  {
    id: 'hotel-003',
    name: '度假温泉酒店',
    address: '杭州市西湖区龙井路123号',
    price: 1288,
    rating: 4.9,
    images: [
      'https://images.unsplash.com/photo-1571896349842-33c89424de2d?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1080&q=80',
      'https://images.unsplash.com/photo-1584132967334-10e028bd69f7?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1170&q=80',
      'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1170&q=80'
    ],
    description: '坐落于西湖边的豪华度假酒店，拥有私人温泉和美丽的园林景观。',
    amenities: ['温泉', '游泳池', 'SPA中心', '健身房', '餐厅', '酒吧', '儿童乐园', '免费WiFi']
  }
];
