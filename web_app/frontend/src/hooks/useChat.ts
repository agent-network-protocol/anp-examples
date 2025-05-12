import { BubbleDataType } from '@ant-design/x/es/bubble/BubbleList';
import { useXAgent, useXChat } from '@ant-design/x';
import { useRef, useState } from 'react';
import { message } from 'antd';
import { AI_CONFIG } from '../constants/chatData';
import { SAMPLE_HOTELS } from '../constants/hotelData';

export const useChat = () => {
  const abortController = useRef<AbortController>(null);
  const [messageHistory, setMessageHistory] = useState<Record<string, any>>({});

  // 使用 useXAgent 创建 AI 代理
  const [agent] = useXAgent<BubbleDataType>({
    baseURL: AI_CONFIG.baseURL,
    model: AI_CONFIG.model,
    dangerouslyApiKey: AI_CONFIG.apiKey,
  });
  
  const loading = agent.isRequesting();

  // 使用 useXChat 处理聊天逻辑
  const { onRequest, messages, setMessages } = useXChat({
    agent,
    requestFallback: (_, { error }) => {
      if (error.name === 'AbortError') {
        return {
          content: 'Request is aborted',
          role: 'assistant',
        };
      }
      return {
        content: 'Request failed, please try again!',
        role: 'assistant',
      };
    },
    transformMessage: (info) => {
      const { originMessage, chunk } = info || {};
      let currentText = '';
      try {
        if (chunk?.data && !chunk?.data.includes('DONE')) {
          const message = JSON.parse(chunk?.data);
          console.log('0--00--', message)
          currentText = message?.choices?.[0].delta?.content;
        }
      } catch (error) {
        console.error(error);
      }
      console.log('00-----', originMessage)
      return {
        content: (originMessage?.content || '') + currentText,
        role: 'assistant',
      };
    },
    resolveAbortController: (controller) => {
      abortController.current = controller;
    },
  });

  // 处理酒店查询
  const handleHotelQuery = (query: string) => {
    // 检查是否是酒店查询
    if (query.includes('查找酒店')) {
      // 创建包含酒店数据的 JSON
      const hotelsData = {
        type: 'hotels',
        hotels: SAMPLE_HOTELS
      };
      
      // 将 JSON 转换为字符串，并包装在 Markdown 代码块中
      const jsonString = JSON.stringify(hotelsData, null, 2);
      const markdownResponse = `以下是我为您找到的酒店信息：\n\n\`\`\`json\n${jsonString}\n\`\`\`\n\n您可以点击"立即预订"按钮进行预订。`;
      
      // 添加用户消息
      onRequest({
        stream: false,
        message: { role: 'user', content: query },
      });
      
      // 添加包含酒店数据的助手消息
      setTimeout(() => {
        // 模拟 AI 响应
        const fakeResponse = {
          content: markdownResponse,
          role: 'assistant',
        };
        
        // 手动添加响应到消息列表
        setMessages(prev => [
          ...prev, 
          {
            id: `hotel_${Date.now()}`,
            status: 'done' as any,
            message: fakeResponse
          }
        ]);
      }, 500);
      
      return true;
    }
    
    return false;
  };

  // 提交消息
  const onSubmit = (val: string) => {
    if (!val) return;

    if (loading) {
      message.error('Request is in progress, please wait for the request to complete.');
      return;
    }

    // 先尝试处理酒店查询
    if (handleHotelQuery(val)) {
      return;
    }

    // 如果不是酒店查询，则发送到 AI 服务
    onRequest({
      stream: true,
      message: { role: 'user', content: val },
    });
  };

  // 更新消息历史
  const updateMessageHistory = (conversationKey: string) => {
    if (messages?.length) {
      setMessageHistory((prev) => ({
        ...prev,
        [conversationKey]: messages,
      }));
    }
  };

  return {
    abortController,
    messageHistory,
    setMessageHistory,
    loading,
    messages,
    setMessages,
    onSubmit,
    updateMessageHistory,
  };
};
