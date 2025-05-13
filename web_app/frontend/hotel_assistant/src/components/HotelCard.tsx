import React, { useState, useEffect } from 'react';
import { Button, Card, Typography, Skeleton, Tag, message } from 'antd';
import { createStyles } from 'antd-style';
import { EnvironmentOutlined, StarOutlined, HomeOutlined } from '@ant-design/icons';
import dayjs from 'dayjs';
import { RoomInfo, ChatResponse } from '../hooks/useChat';
import { createAndPayHotelOrder } from '../services/hotelService';
import HotelOrderForm from './HotelOrderForm';
import PayQrModal from './PayQrModal';

const { Title, Text } = Typography;

interface HotelCardProps {
  room: RoomInfo;
  onPayClick: (roomTypeId: string) => void;
  apiData?: ChatResponse; // Add API data prop
}

// 创建组件样式
const useStyles = createStyles(({ token, css }) => {
  return {
    hotelCard: css`
      width: 240px;
      min-height: 400px;
      display: flex;
      flex-direction: column;
      border-radius: ${token.borderRadiusLG}px;
      overflow: hidden;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
      background-color: white;
      position: relative;
      transition: transform 0.3s, box-shadow 0.3s;
      &:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.12);
      }
    `,
    imageContainer: css`
      width: 100%;
      height: 160px;
      position: relative;
      overflow: hidden;
    `,
    hotelImage: css`
      width: 100%;
      height: 100%;
      object-fit: cover;
      transition: transform 0.5s;
      &:hover {
        transform: scale(1.05);
      }
    `,
    infoContainer: css`
      padding: 16px;
      display: flex;
      flex-direction: column;
      flex: 1;
      height: 100%;
    `,
    hotelName: css`
      font-size: 18px !important;
      font-weight: 600;
      margin-bottom: 4px !important;
      line-height: 1.3;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
      text-overflow: ellipsis;
    `,
    address: css`
      color: ${token.colorTextSecondary};
      font-size: 12px;
      display: flex;
      align-items: center;
      gap: 4px;
      margin-bottom: 12px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    `,
    infoRow: css`
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 12px;
    `,
    priceContainer: css`
      display: flex;
      flex-direction: column;
    `,
    priceLabel: css`
      color: ${token.colorTextSecondary};
      font-size: 12px;
    `,
    price: css`
      font-size: 20px;
      font-weight: 600;
      color: ${token.colorPrimary};
    `,
    ratingContainer: css`
      display: flex;
      align-items: center;
      gap: 4px;
      background-color: ${token.colorPrimaryBg};
      padding: 4px 8px;
      border-radius: 16px;
    `,
    rating: css`
      font-weight: 600;
      color: ${token.colorPrimary};
    `,
    buttonContainer: css`
      margin-top: auto;
    `,
    availabilityTag: css`
      position: absolute;
      top: 12px;
      right: 12px;
      z-index: 10;
      font-weight: 500;
      border-radius: 16px;
      padding: 2px 12px;
    `,
  };
});

const HotelCard: React.FC<HotelCardProps> = ({ room, onPayClick, apiData }) => {
  // 保留后端返回的数据，只在缺失时才提供默认值
  // Preserve data from backend API, only provide defaults if fields are missing
  if (apiData) {
    // Only add default values if fields are missing
    const today = dayjs();
    apiData = {
      ...apiData,
      // Preserve existing data, only use defaults if needed
      contactName: apiData.contactName || '常高伟',
      contactMobile: apiData.contactMobile || '13800000000',
      checkInDate: apiData.checkInDate || today.format('YYYY-MM-DD'),
      checkOutDate: apiData.checkOutDate || today.add(1, 'day').format('YYYY-MM-DD'),
      guestNames: apiData.guestNames || ['常高伟'],
    };
  }
  const { styles } = useStyles();
  const [loading, setLoading] = useState(true);
  const [bookingLoading, setBookingLoading] = useState(false);
  const [formVisible, setFormVisible] = useState(false);
  const [payModal, setPayModal] = useState<{visible: boolean, orderNo: string, qrCodeUrl: string} | null>(null);

  useEffect(() => {
    // 模拟数据加载
    const timer = setTimeout(() => {
      setLoading(false);
    }, 1000);
    return () => clearTimeout(timer);
  }, []);

  // 打开表单弹窗
  const handleBooking = () => {
    setFormVisible(true);
  };

  // 表单提交回调
  const handleOrderSubmit = async (formValues: any) => {
    setFormVisible(false);
    setBookingLoading(true);
    try {
      // 打印一下表单值以便调试
      console.log('Form values:', formValues);
      
      // 直接使用字符串格式的日期，因为表单中使用的是Input而不是DatePicker
      // 打印房间数据以便调试
      console.log('Room data:', { 
        roomTypeId: room.roomTypeId,
        ratePlanID: room.ratePlanID
      });
      
      const response = await createAndPayHotelOrder({
        hotelID: room.hotel.hotelID,
        ratePlanID: room.ratePlanID, // 修正：使用正确的ratePlanID而不是roomTypeId
        roomNum: 1,
        checkInDate: formValues.checkInDate, // 已经是字符串，不需要format
        checkOutDate: formValues.checkOutDate, // 已经是字符串，不需要format
        guestNames: [formValues.guestName],
        orderAmount: room.pricePerNight,
        contactName: formValues.contactName,
        contactMobile: formValues.contactMobile,
        paymentType: 2,
      });
      // 打印服务端返回的支付信息
      console.log('Payment response data:', response.data);
      console.log('Payment info fields:', response.data?.paymentInfo ? Object.keys(response.data.paymentInfo) : 'no paymentInfo');
      
      if (response.success) {
        // 正确处理字段名不匹配问题，服务端返回的是qrCodeImageUrl而不是qrCodeUrl
        const qrCodeUrl = response.data?.paymentInfo?.qrCodeImageUrl || response.data?.paymentInfo?.qrCodeUrl || '';
        console.log('QR code URL:', qrCodeUrl);
        
        setPayModal({
          visible: true,
          orderNo: response.data?.orderNo || '',
          qrCodeUrl: qrCodeUrl,
        });
      } else {
        message.error(response.msg || '预订失败');
      }
    } catch (error) {
      console.error('预订失败:', error);
      message.error('预订失败，请稍后重试');
    } finally {
      setBookingLoading(false);
    }
  };

  // 关闭支付弹窗
  const handlePayModalClose = () => {
    setPayModal(null);
  };

  if (loading) {
    return (
      <Card className={styles.hotelCard} bordered={false}>
        <div style={{ height: '100%' }}>
          <Skeleton.Image active style={{ width: '180px', height: '160px' }} />
          <div style={{ padding: '16px' }}>
            <Skeleton.Input active style={{ width: '80%', marginBottom: '8px' }} size="small" />
            <Skeleton.Input active style={{ width: '60%', marginBottom: '16px' }} size="small" />
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '16px' }}>
              <Skeleton.Input active style={{ width: '40%' }} size="small" />
              <Skeleton.Input active style={{ width: '20%' }} size="small" />
            </div>
            <div style={{ display: 'flex', gap: '8px', marginBottom: '16px' }}>
              <Skeleton.Button active style={{ width: '30%' }} size="small" />
              <Skeleton.Button active style={{ width: '30%' }} size="small" />
            </div>
            <Skeleton.Button active style={{ width: '100%', marginTop: '20px' }} />
          </div>
        </div>
      </Card>
    );
  }

  return (
    <>
      <Card className={styles.hotelCard} bordered={false} bodyStyle={{ padding: 0, display: 'flex', flexDirection: 'column', height: '100%' }}>
        {/* 可用状态标签 */}
        {room.available ? (
          <Tag color="success" className={styles.availabilityTag}>可预订</Tag>
        ) : (
          <Tag color="error" className={styles.availabilityTag}>已满</Tag>
        )}
        {/* 酒店图片 */}
        <div className={styles.imageContainer}>
          <img 
            className={styles.hotelImage}
            src={room.images}
            alt={room.hotel.hotelName}
          />
        </div>
        {/* 酒店信息 */}
        <div className={styles.infoContainer}>
          {/* 酒店名称 */}
          <Title level={5} className={styles.hotelName}>
            {room.hotel.hotelName}
          </Title>
          {/* 地址 */}
          <div className={styles.address}>
            <EnvironmentOutlined /> {room.hotel.address}
          </div>
          {/* 价格和评分 */}
          <div className={styles.infoRow}>
            <div className={styles.priceContainer}>
              <Text className={styles.priceLabel}>价格/晚</Text>
              <Text className={styles.price}>¥{room.pricePerNight}</Text>
            </div>
            <div className={styles.ratingContainer}>
              <StarOutlined />
              <span className={styles.rating}>{room.hotel.rating}</span>
            </div>
          </div>
          {/* 房型信息 */}
          <div style={{ marginBottom: 8 }}>
            <div style={{
              fontWeight: 600,
              fontSize: 16,
              color: '#1677ff',
              marginBottom: 2,
              display: 'flex',
              alignItems: 'center',
              gap: 4
            }}>
              <HomeOutlined style={{ color: '#1677ff' }} />
              {room.roomType}
            </div>
            <div style={{
              fontSize: 13,
              color: '#666',
              background: '#f5f5f5',
              borderRadius: 12,
              padding: '2px 10px',
              display: 'inline-block'
            }}>
              {room.bedType}
            </div>
          </div>
          {/* 预订按钮 */}
          <div className={styles.buttonContainer}>
            <Button 
              type="primary" 
              onClick={handleBooking}
              disabled={!room.available}
              loading={bookingLoading}
            >
              立即预订
            </Button>
          </div>
        </div>
      </Card>
      {/* 下单表单弹窗 */}
      <HotelOrderForm
        visible={formVisible}
        room={room}
        onCancel={() => setFormVisible(false)}
        onSubmit={handleOrderSubmit}
        loading={bookingLoading}
        apiData={apiData} // Pass API data to the form
      />
      {/* 支付二维码弹窗 */}
      {payModal && (
        <PayQrModal
          visible={payModal.visible}
          orderNo={payModal.orderNo}
          qrCodeUrl={payModal.qrCodeUrl}
          onClose={handlePayModalClose}
        />
      )}
    </>
  );
};

export default HotelCard;