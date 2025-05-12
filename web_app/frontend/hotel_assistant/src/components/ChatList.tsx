import React, { useState } from 'react';
import { Button, Flex, Space, Spin, message } from 'antd';
import { Bubble, Prompts, Welcome } from '@ant-design/x';
import type { BubbleProps } from '@ant-design/x';
import { GPTVis } from '@antv/gpt-vis';
import {
  CopyOutlined,
  DislikeOutlined,
  EllipsisOutlined,
  LikeOutlined,
  ReloadOutlined,
  ShareAltOutlined,
  UserOutlined,
} from '@ant-design/icons';
import { useStyles } from '../styles/useStyles';
import { DESIGN_GUIDE, HOT_TOPICS } from '../constants/chatData';
import HotelCard from './HotelCard';
import { HotelInfo } from '../constants/hotelData';

interface ChatListProps {
  messages: any[];
  onSubmit: (val: string) => void;
  loading: boolean;
}

// 自定义渲染函数，处理酒店数据
const RenderCustomContent: BubbleProps['messageRender'] = (content) => {
  try {
    // 查找 Markdown 代码块中的 JSON 数据
    const jsonRegex = /```json\s*([\s\S]*?)\s*```/;
    const match = content.match(jsonRegex);
    
    if (match && match[1] && match.index !== undefined) {
      // 尝试解析 JSON 数据
      const jsonData = JSON.parse(match[1]);
      
      // 检查是否是酒店数据
      if (jsonData.type === 'hotels' && Array.isArray(jsonData.hotels)) {
        // 提取酒店数据前后的文本
        const beforeText = content.substring(0, match.index).trim();
        const afterText = content.substring(match.index + match[0].length).trim();
        
        // 渲染酒店卡片列表
        return (
          <div>
            {beforeText && <GPTVis>{beforeText}</GPTVis>}
            
            <div style={{ display: 'flex', flexDirection: 'row', gap: '16px', margin: '16px 0', overflowX: 'auto', paddingBottom: '8px' }}>
              {jsonData.hotels.map((hotel: HotelInfo) => (
                <HotelCard 
                  key={hotel.id}
                  hotel={hotel} 
                  onPayClick={(id) => {
                    message.success(`正在处理酒店 ${id} 的支付请求`);
                  }} 
                />
              ))}
            </div>
            
            {afterText && <GPTVis>{afterText}</GPTVis>}
          </div>
        );
      }
    }
    
    // 如果不是酒店数据或解析失败，则使用默认的 Markdown 渲染
    return <GPTVis>{content}</GPTVis>;
  } catch (error) {
    console.error('Error rendering custom content:', error);
    return <GPTVis>{content}</GPTVis>;
  }
};

const ChatList: React.FC<ChatListProps> = ({ messages, onSubmit, loading }) => {
  const { styles } = useStyles();
  
  return (
    <div className={styles.chatList}>
      {messages?.length ? (
        /* 🌟 消息列表 */
        <Bubble.List
          items={messages?.map((i) => {
            return {
              ...i.message,
              messageRender: RenderCustomContent,
              classNames: {
                content: i.status === 'loading' ? styles.loadingMessage : '',
              },
              typing: i.status === 'loading' ? { step: 5, interval: 20 } : false,
            }})}
          style={{ height: '100%' }}
          roles={{
            assistant: {
              placement: 'start',
              avatar: { icon: <UserOutlined />, style: { background: '#fde3cf' } },
              footer: (
                <div style={{ display: 'flex' }}>
                  <Button type="text" size="small" icon={<ReloadOutlined />} />
                  <Button type="text" size="small" icon={<CopyOutlined />} />
                  <Button type="text" size="small" icon={<LikeOutlined />} />
                  <Button type="text" size="small" icon={<DislikeOutlined />} />
                </div>
              ),
              loadingRender: () => <Spin size="small" />,
            },
            user: {
              placement: 'end',
              avatar: { icon: <UserOutlined />, style: { background: '#87d068' } },
            },
          }}
        />
      ) : (
        <Space direction="vertical" size={16} className={styles.placeholder}>
          <Welcome
            variant="borderless"
            icon="https://avatars.githubusercontent.com/u/199323856?s=48&v=4"
            title="ANP网络探索工具 | ANP Network Explorer"
            description="目标是成为智能体互联网时代的HTTP"
          />
          
          {/* 测试按钮 - 用于展示酒店卡片 */}
          <div style={{ display: 'flex', gap: '10px', marginTop: '20px' }}>
            <Button 
              type="primary" 
              onClick={() => onSubmit("查找酒店")}
            >
              查找酒店
            </Button>
          </div>
        </Space>
      )}
    </div>
  );
};

export default ChatList;
