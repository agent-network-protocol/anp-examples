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
import { ChatResponse, RoomInfo } from '../hooks/useChat';

interface ChatListProps {
  messages: any[];
  onSubmit: (val: string) => void;
  loading: boolean;
}

// 自定义渲染函数，处理酒店数据
const RenderHotelData = (data: ChatResponse) => {
  try {
    // 如果 content 是数组，则渲染酒店卡片列表
    if (Array.isArray(data.content)) {
      return (
        <div>
          <div style={{ margin: '0 0 16px 0' }}>
            <GPTVis>{data.summary}</GPTVis>
          </div>
          
          <div style={{ display: 'flex', flexDirection: 'row', gap: '16px', margin: '16px 0', overflowX: 'auto', paddingBottom: '8px' }}>
            {data.content.map((room: RoomInfo) => (
              <HotelCard 
                key={room.roomTypeId}
                room={room} 
                onPayClick={(roomTypeId) => {
                  message.success(`正在处理房型 ${roomTypeId} 的预订请求`);
                }} 
              />
            ))}
          </div>
        </div>
      );
    } else {
      // 如果 content 不是数组，只展示 summary
      return <GPTVis>{data.summary}</GPTVis>;
    }
  } catch (error) {
    console.error('Error rendering hotel data:', error);
    return <GPTVis>数据渲染出错</GPTVis>;
  }
};

// 处理消息内容的渲染
const processMessageContent = (message: any) => {
  // 如果是酒店数据
  if (message.isHotelData && typeof message.content === 'object' && message.content !== null) {
    return RenderHotelData(message.content);
  }
  
  // 如果是普通文本
  if (typeof message.content === 'string') {
    return message.content;
  }
  
  // 其他情况，转为字符串
  return JSON.stringify(message.content);
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
              role: i.role,
              content: processMessageContent(i),
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
            title="您好，我是您的酒店助手"
            description="我是一个基于ANP协议的酒店助手，可以为您提供酒店信息、预订、支付等服务。"
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
