import React, { useEffect, useRef, useCallback } from 'react';
import { Button, Space, Typography, Collapse } from 'antd';
import type { CollapseProps } from 'antd';
import { Bubble, Welcome } from '@ant-design/x';
import MarkdownIt from 'markdown-it';
import {
  CopyOutlined,
  DislikeOutlined,
  LikeOutlined,
  ReloadOutlined,
  UserOutlined,
} from '@ant-design/icons';
import { useStyles } from '../styles/useStyles';
import HotelCard from './HotelCard';
import { ChatResponse, RoomInfo } from '../hooks/useChat';
import { getHotelOrderDetail } from '../services/hotelService';

interface ChatListProps {
  messages: any[];
  setMessages: React.Dispatch<React.SetStateAction<any[]>>;
}

// 自定义渲染函数，处理酒店数据
const RenderHotelData = (data: ChatResponse, setMessages: React.Dispatch<React.SetStateAction<any[]>>, messages: any[]) => {
  try {
    // 如果 content 是数组，则渲染酒店卡片列表
    if (Array.isArray(data.content)) {
      // 检查是否有待支付订单
      const hasPendingOrder = messages.some(
        msg => msg.type === 'order' && msg.content?.content?.orderStatus === '待支付'
      );
      const { content, summary, ...rest } = data
      return (
        <div>
          <div style={{ margin: '0 0 16px 0' }}>
            {renderMarkdown(data.summary)}
          </div>

          <div style={{ display: 'flex', flexDirection: 'row', gap: '16px', margin: '16px 0', overflowX: 'auto', paddingBottom: '8px' }}>
            {data.content.map((room: RoomInfo) => (
              <HotelCard
                key={room.roomTypeId}
                room={room}
                checkInData={rest}
                onPayClick={(orderMessage) => {
                  if (hasPendingOrder) {
                    setMessages(prev => [
                      ...prev,
                      {
                        role: 'assistant',
                        content: '您有未支付订单，请先完成支付',
                      }
                    ]);
                    return;
                  }
                  if (typeof orderMessage === 'object') {
                    setMessages(prev => [
                      ...prev,
                      {
                        role: 'assistant',
                        type: 'order',
                        content: orderMessage.content
                      }
                    ]);
                  }
                }}
              />
            ))}
          </div>
        </div>
      );
    } else {
      // 如果 content 不是数组，只展示 summary
      return renderMarkdown(data.summary);
    }
  } catch (error) {
    console.error('Error rendering hotel data:', error);
    return renderMarkdown('数据渲染出错');
  }
};

// 处理消息内容
const processMessageContent = (message: any, setMessages: React.Dispatch<React.SetStateAction<any[]>>, messages: any[]) => {
  // 如果是通知消息
  if (message.isNotification) {
    const items: CollapseProps['items'] = [
      {
        key: '1',
        label: message.notificationType || '系统通知',
        children: (
          <>
            <div>
              {typeof message.content === 'string' ? renderMarkdown(message.content) : JSON.stringify(message.content)}
            </div>
            {message.timestamp && (
              <div style={{ fontSize: '12px', color: '#999', marginTop: '8px', textAlign: 'right' }}>
                {new Date(message.timestamp).toLocaleString('zh-CN')}
              </div>
            )}
          </>
        ),
      },
    ];

    return (
      <Collapse 
        items={items} 
        // defaultActiveKey={['1']} 
        ghost
        expandIconPosition="end"
        style={{ 
          background: '#f0f8ff', 
          borderRadius: '8px',
          borderLeft: '4px solid #1890ff',
          marginBottom: 0
        }}
      />
    );
  }
  
  // 如果是酒店数据
  if (message.isHotelData && typeof message.content === 'object' && message.content !== null) {
    return RenderHotelData(message.content, setMessages, messages);
  }

  // 如果是订单消息
  if (message.type === 'order' && typeof message.content === 'object') {
    const order = message.content.content;
    return (
      <div
        style={{
          display: 'flex',
          alignItems: 'stretch',
          gap: 32,
          padding: '24px 24px',
          margin: '16px 0',
          maxWidth: 640,
          minWidth: 320,
          width: '100%',
          background: '#f6f6f6',
          borderRadius: 16,
          flexWrap: 'wrap',
          boxSizing: 'border-box',
          position: 'relative'
        }}
      >
        {/* 左侧标题+二维码 */}
        <div style={{
          flex: '0 0 180px',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          minWidth: 180
        }}>
          <div style={{ fontWeight: 700, fontSize: 20, color: '#388e3c', marginBottom: 16, textAlign: 'center' }}>
            {message.content.summary}
          </div>
          <img
            src={order.qrCodeUrl}
            alt="支付二维码"
            style={{
              width: 140,
              height: 140,
              borderRadius: 8,
              border: '1px solid #e0e0e0',
              background: '#fff',
              marginBottom: 8,
              display: 'block',
            }}
          />
          <div style={{ fontSize: 13, color: '#333', margin: '4px 0 0 0', letterSpacing: 1, textAlign: 'center' }}>
            订单号：<span style={{ fontWeight: 500 }}>{order.orderNo}</span>
          </div>
        </div>
        {/* 右侧信息 */}
        <div style={{
          flex: '1 1 220px',
          fontSize: 15,
          color: '#222',
          lineHeight: 1.8,
          minWidth: 180,
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'flex-start',
          textAlign: 'left'
        }}>
          <div><b>酒店：</b>{order.hotelName}</div>
          <div><b>房型：</b>{order.roomType}</div>
          <div><b>入住：</b>{order.checkInDate}</div>
          <div><b>离店：</b>{order.checkOutDate}</div>
          <div><b>房客：</b>{order?.guestNames?.join('、')}</div>
          <div><b>金额：</b><span style={{ color: '#43b244', fontWeight: 600 }}>¥{order.orderAmount}</span></div>
          <div><b>状态：</b><span style={{ color: order.orderStatus === '已支付' ? '#43b244' : '#faad14', fontWeight: 600 }}>{order.orderStatus}</span></div>
          <div><b>支付方式：</b>{order.paymentType}</div>
          <div><b>创建时间：</b>{order.createTime}</div>
        </div>
        <div
          id={`polling-status-${order.orderNo}`}
          style={{
            position: 'absolute',
            bottom: 0,
            left: '50%',
            transform: 'translateX(-50%)',
            color: order.orderStatus === '已支付' ? '#43b244' : (order.orderStatus === '待支付' ? '#faad14' : '#faad14'),
            fontSize: 14,
            marginTop: 2,
            textAlign: 'center',
            fontWeight: 600,
            width: '100%'
          }}
        >
          {order.orderStatus === '已支付'
            ? '支付成功!'
            : order.orderStatus === '待支付'
              ? ''
              : order.orderStatus}
        </div>
      </div>
    );
  }

  // 如果是普通文本，使用 markdown 渲染
  if (typeof message.content === 'string') {
    return renderMarkdown(message.content);
  }

  // 其他情况，转为字符串后渲染
  return renderMarkdown(JSON.stringify(message.content));
};

const md = new MarkdownIt({ html: true, breaks: true });

const renderMarkdown = (content: string) => {
  return (
    <Typography>
      <div dangerouslySetInnerHTML={{ __html: md.render(content) }} />
    </Typography>
  );
};

const ChatList: React.FC<ChatListProps> = ({ messages, setMessages }) => {
  const { styles } = useStyles();
  const pollingTimerRef = useRef<NodeJS.Timeout | null>(null);
  const pendingOrdersRef = useRef<Map<string, { pollCount: number, startTime: number }>>(new Map());
  const MAX_POLL_COUNT = 30; // 最多轮询30次，相当于5分钟

  // 轮询支付状态
  const pollOrderStatus = useCallback(async () => {
    const pendingOrders = Array.from(pendingOrdersRef.current.entries());
    if (pendingOrders.length === 0) {
      if (pollingTimerRef.current) {
        clearTimeout(pollingTimerRef.current);
        pollingTimerRef.current = null;
      }
      return;
    }

    try {
      for (const [orderNo, orderData] of pendingOrders) {
        const statusEl = document.getElementById(`polling-status-${orderNo}`);
        if (!statusEl) continue;

        const detail = await getHotelOrderDetail({ customerOrderNo: orderNo });

        if (detail.success && detail.data && detail.data.payStatus === 1) {
          statusEl.textContent = '支付成功！';
          pendingOrdersRef.current.delete(orderNo);

          setMessages(prev => {
            const newMessages = [...prev];
            const orderMessageIndex = newMessages.findIndex(
              msg => msg.type === 'order' && msg.content?.content?.orderNo === orderNo
            );
            if (orderMessageIndex !== -1) {
              newMessages[orderMessageIndex].content.content.orderStatus = '已支付';
              newMessages[orderMessageIndex].content.content.payStatus = detail.data.payStatus;
              newMessages[orderMessageIndex].content.content.paymentType = '支付宝';
              newMessages[orderMessageIndex].content.summary = '订单支付成功';
            }
            return newMessages;
          });
        } else {
          if (orderData.pollCount < MAX_POLL_COUNT) {
            const elapsedSeconds = Math.floor((Date.now() - orderData.startTime) / 1000);
            statusEl.textContent = `正在查询支付状态...（${elapsedSeconds}秒）`;
            pendingOrdersRef.current.set(orderNo, { 
              ...orderData, 
              pollCount: orderData.pollCount + 1 
            });
          } else {
            statusEl.textContent = '未查到订单支付信息，请稍后在订单中心查看。';
            pendingOrdersRef.current.delete(orderNo);
          }
        }
      }
    } catch (error) {
      console.error('Error polling order status:', error);
    }

    // 继续轮询
    pollingTimerRef.current = setTimeout(pollOrderStatus, 10000); // 10秒轮询一次
  }, [setMessages]);

  // 监听消息变化，处理需要轮询的订单
  useEffect(() => {
    messages.forEach(message => {
      if (
        message.type === 'order' &&
        message.content?.content?.orderStatus === '待支付'
      ) {
        const orderNo = message.content.content.orderNo;
        if (!pendingOrdersRef.current.has(orderNo)) {
          pendingOrdersRef.current.set(orderNo, { pollCount: 0, startTime: Date.now() });
        }
      } else if (
        message.type === 'order' &&
        message.content?.content?.orderStatus !== '待支付'
      ) {
        const orderNo = message.content.content.orderNo;
        pendingOrdersRef.current.delete(orderNo);
      }
    });

    if (pendingOrdersRef.current.size > 0 && !pollingTimerRef.current) {
      pollingTimerRef.current = setTimeout(pollOrderStatus, 20000); // 20秒后开始轮询
    }

    // 组件卸载时清理定时器
    return () => {
      if (pollingTimerRef.current) {
        clearTimeout(pollingTimerRef.current);
      }
    };
  }, [messages, pollOrderStatus]);

  return (
    <div className={styles.chatList}>
      {/* 🌟 消息列表 */}
      <Bubble.List
        items={messages?.map((i) => ({
          role: i.role,
          content: i,
          messageRender: (content) => processMessageContent(content, setMessages, messages),
          classNames: {
            content: i.loading ? styles.loadingMessage : '',
          },
          loading: i.loading,
        }))}
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
            style: { maxWidth: 800 }
          },
          user: {
            placement: 'end',
            avatar: { icon: <UserOutlined />, style: { background: '#87d068' } },
          },
        }}
      />
    </div>
  );
};

export default ChatList;
