import React, { useState, useEffect } from 'react';
import { Button, Card, Avatar, Typography, Space, Divider, Skeleton } from 'antd';
import { createStyles } from 'antd-style';
import { EnvironmentOutlined, StarOutlined, DollarOutlined } from '@ant-design/icons';

const { Title, Text } = Typography;

// 定义酒店信息接口
interface HotelInfo {
  id: string;
  name: string;
  address: string;
  price: number;
  rating: number;
  images: string[];
  description: string;
  amenities: string[];
}

interface HotelCardProps {
  hotel: HotelInfo;
  onPayClick: (hotelId: string) => void;
}

// 创建组件样式
const useStyles = createStyles(({ token, css }) => {
  return {
    hotelCard: css`
      width: 200px;
      height: 400px;
      flex-shrink: 0;
      border-radius: ${token.borderRadiusLG}px;
      overflow: hidden;
      box-shadow: ${token.boxShadow};
      background-color: white;
      padding: 16px;
      display: flex;
      flex-direction: column;
      align-items: center;
      text-align: center;
    `,
    avatar: css`
      margin-bottom: 12px;
      width: 80px;
      height: 80px;
    `,
    nameContainer: css`
      height: 40px;
      display: flex;
      flex-direction: column;
      justify-content: center;
    `,
    name: css`
      margin-bottom: 4px !important;
      font-weight: 600;
      font-size: 16px !important;
    `,
    addressContainer: css`
      height: 30px;
      display: flex;
      align-items: center;
      justify-content: center;
    `,
    address: css`
      color: ${token.colorTextSecondary};
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 4px;
      font-size: 12px;
    `,
    infoRow: css`
      display: flex;
      justify-content: center;
      gap: 16px;
      margin: 12px 0;
      width: 100%;
      height: 40px;
    `,
    infoItem: css`
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
    `,
    infoLabel: css`
      color: ${token.colorTextSecondary};
      font-size: 10px;
    `,
    infoValue: css`
      font-weight: 500;
      font-size: 14px;
    `,
    amenitiesContainer: css`
      height: 40px;
      display: flex;
      align-items: center;
      justify-content: center;
      margin-bottom: 12px;
    `,
    amenities: css`
      display: flex;
      flex-wrap: wrap;
      justify-content: center;
      gap: 4px;
    `,
    amenity: css`
      background: ${token.colorBgLayout};
      padding: 2px 6px;
      border-radius: ${token.borderRadius}px;
      font-size: 10px;
    `,
    buttonContainer: css`
      margin-top: auto;
      width: 100%;
      padding-top: 12px;
    `,
    payButton: css`
      width: 100%;
    `,
  };
});

const HotelCard: React.FC<HotelCardProps> = ({ hotel, onPayClick }) => {
  const { styles } = useStyles();
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // 模拟数据加载
    const timer = setTimeout(() => {
      setLoading(false);
    }, 1000);

    return () => clearTimeout(timer);
  }, []);

  // 使用第一张图片作为头像
  const avatarImage = hotel.images[0];

  if (loading) {
    return (
      <Card className={styles.hotelCard} bordered={false}>
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', height: '100%' }}>
          <Skeleton.Avatar active size={80} shape="circle" style={{ marginBottom: '12px' }} />
          <Skeleton.Input style={{ width: '80%', marginBottom: '8px' }} active size="small" />
          <Skeleton.Input style={{ width: '60%', marginBottom: '16px' }} active size="small" />
          <div style={{ display: 'flex', justifyContent: 'space-between', width: '100%', marginBottom: '16px' }}>
            <Skeleton.Input style={{ width: '45%' }} active size="small" />
            <Skeleton.Input style={{ width: '45%' }} active size="small" />
          </div>
          <div style={{ display: 'flex', flexWrap: 'wrap', justifyContent: 'center', gap: '4px', marginBottom: '16px' }}>
            {[1, 2, 3, 4].map((_, index) => (
              <Skeleton.Button key={index} active size="small" style={{ width: '45%', marginBottom: '4px' }} />
            ))}
          </div>
          <Skeleton.Button active style={{ width: '100%', marginTop: 'auto' }} />
        </div>
      </Card>
    );
  }

  return (
    <Card className={styles.hotelCard} bordered={false}>
      {/* 酒店图片（圆形） */}
      <Avatar 
        className={styles.avatar} 
        size={80} 
        src={avatarImage}
        alt={hotel.name}
      />

      {/* 酒店名称 */}
      <div className={styles.nameContainer}>
        <Title level={4} className={styles.name}>
          {hotel.name}
        </Title>
      </div>

      {/* 地址 */}
      <div className={styles.addressContainer}>
        <Text className={styles.address}>
          <EnvironmentOutlined /> {hotel.address}
        </Text>
      </div>

      {/* 价格和评分 */}
      <div className={styles.infoRow}>
        <div className={styles.infoItem}>
          <Text className={styles.infoLabel}>价格</Text>
          <Text className={styles.infoValue}>
            <DollarOutlined /> {hotel.price}
          </Text>
        </div>
        <div className={styles.infoItem}>
          <Text className={styles.infoLabel}>评分</Text>
          <Text className={styles.infoValue}>
            <StarOutlined /> {hotel.rating}
          </Text>
        </div>
      </div>

      {/* 设施列表（最多显示4个） */}
      <div className={styles.amenitiesContainer}>
        <div className={styles.amenities}>
          {hotel.amenities.slice(0, 4).map((amenity, index) => (
            <span key={index} className={styles.amenity}>
              {amenity}
            </span>
          ))}
        </div>
      </div>

      {/* 预订按钮 */}
      <div className={styles.buttonContainer}>
        <Button 
          type="primary" 
          className={styles.payButton}
          onClick={() => onPayClick(hotel.id)}
        >
          立即预订
        </Button>
      </div>
    </Card>
  );
};

export default HotelCard;
