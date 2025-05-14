import { useState, useRef } from 'react';
import { message } from 'antd';

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
  orderAmount: number;
  ratePlanID: string;
  hotel: {
    hotelID: string;
    hotelName: string;
    address: string;
    rating: number;
    price: string;
  };
}

// 定义消息接口
interface ChatMessage {
  role: 'user' | 'assistant';
  content: string | ChatResponse;
  isHotelData?: boolean;
  loading?: boolean;
}

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/';

export const useChat = (onFirstMessage?: (message: string) => void) => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [loading, setLoading] = useState(false);
  const abortControllerRef = useRef<AbortController | null>(null);
  const isFirstMessageRef = useRef(true);

  // 处理消息查询
  const handleSender = async (query: string) => {
    setLoading(true);
    // 添加一个带有 loading 状态的空消息
    setMessages(prev => [
      ...prev,
      { role: 'assistant', content: '', loading: true }
    ]);

    abortControllerRef.current = new AbortController();

    try {
      const response = await fetch(`${API_BASE_URL}/api/travel/hotel/query`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query }),
        signal: abortControllerRef.current.signal,
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      let data = await response.json() as ChatResponse;
      // 更新消息，移除 loading 状态
      setMessages(prev => {
        const newMessages = [...prev];
        const loadingMessageIndex = newMessages.findIndex(msg => msg.loading);
        if (loadingMessageIndex !== -1) {
          newMessages[loadingMessageIndex] = {
            role: 'assistant',
            content: data,
            isHotelData: Array.isArray(data.content),
            loading: false
          };
        }
        return newMessages;
      });

    } catch (error: unknown) {
      if (error instanceof Error) {
        if (error.name === 'AbortError') {
          console.log('Request was cancelled');
        } else {
          console.error('Error:', error);
          message.error('请求失败，请稍后重试。');

          // 更新消息，显示错误状态
          setMessages(prev => {
            const newMessages = [...prev];
            const loadingMessageIndex = newMessages.findIndex(msg => msg.loading);
            if (loadingMessageIndex !== -1) {
              newMessages[loadingMessageIndex] = {
                role: 'assistant',
                content: '抱歉，请求失败，请稍后重试。',
                loading: false
              };
            }
            return newMessages;
          });
        }
      }
    } finally {
      setLoading(false);
      abortControllerRef.current = null;
    }
  };

  // 提交消息
  const onSubmit = (val: string) => {
    if (!val) return;

    if (loading) {
      message.info('请求正在进行中，请等待请求完成。');
      return;
    }

    setMessages(prev => [
      ...prev,
      { role: 'user', content: val },
    ]);

    if (isFirstMessageRef.current && onFirstMessage) {
      onFirstMessage(val);
      isFirstMessageRef.current = false;
    }

    handleSender(val);
  };

  // 取消请求
  const cancelRequest = () => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
      setLoading(false);
      message.info('请求已取消');

      // 移除最后一条正在加载的消息
      setMessages(prev => {
        const newMessages = [...prev];
        const loadingMessageIndex = newMessages.findIndex(msg => msg.loading);
        if (loadingMessageIndex !== -1) {
          newMessages.splice(loadingMessageIndex, 1);
        }
        return newMessages;
      });
    }
  };

  return {
    messages,
    setMessages,
    onSubmit,
    loading,
    cancelRequest,
  };
};
