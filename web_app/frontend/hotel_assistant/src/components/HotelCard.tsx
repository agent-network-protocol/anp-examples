import React, { useState, useEffect } from 'react';
import { Button, Card, Typography, Skeleton, Tag, message } from 'antd';
import { createStyles } from 'antd-style';
import { EnvironmentOutlined, StarOutlined, HomeOutlined } from '@ant-design/icons';
import { RoomInfo } from '../hooks/useChat';
import { createAndPayHotelOrder } from '../services/hotelService';
import HotelOrderForm from './HotelOrderForm';
import PayQrModal from './PayQrModal';

const { Title, Text } = Typography;

interface HotelCardProps {
  room: RoomInfo;
  onPayClick: (roomTypeId: string) => void;
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

const HotelCard: React.FC<HotelCardProps> = ({ room, onPayClick }) => {
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
      const response = await createAndPayHotelOrder({
        hotelID: room.hotel.hotelId,
        ratePlanID: room.roomTypeId,
        roomNum: 1,
        checkInDate: formValues.checkInDate.format('YYYY-MM-DD'),
        checkOutDate: formValues.checkOutDate.format('YYYY-MM-DD'),
        guestNames: [formValues.guestName],
        orderAmount: room.pricePerNight,
        contactName: formValues.guestName,
        contactMobile: formValues.contactMobile,
        paymentType: 2,
      });
      if (response.success) {
        setPayModal({
          visible: true,
          orderNo: response.data?.orderNo || '',
          qrCodeUrl: response.data?.paymentInfo.qrCodeUrl || '',
        });
      } else {
        message.error(response.msg || '预订失败');
      }
    } catch (error) {
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