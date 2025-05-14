import React, { useState, useCallback } from 'react';
import { useStyles } from '../styles/useStyles';
import { useChat } from '../hooks/useChat';
import ChatSider from './ChatSider';
import ChatList from './ChatList';
import ChatSender from './ChatSender';
import { DEFAULT_CONVERSATIONS_ITEMS } from '../constants/chatData';
import type { GetProp } from 'antd';
import { Attachments, Welcome, Prompts } from '@ant-design/x';
import { SENDER_PROMPTS } from '../constants/chatData';

interface Conversation {
  key: string;
  label: string;
  group: string;
}

const ChatPage: React.FC = () => {
  const { styles } = useStyles();

  // 会话状态
  const [conversations, setConversations] = useState<Conversation[]>(DEFAULT_CONVERSATIONS_ITEMS);
  const [curConversation, setCurConversation] = useState(DEFAULT_CONVERSATIONS_ITEMS[0].key);

  // 处理第一条消息
  const handleFirstMessage = useCallback((message: string) => {
    const now = new Date();
    const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
    const yesterday = new Date(today);
    yesterday.setDate(yesterday.getDate() - 1);

    let group: string;
    if (now >= today && now < new Date(today.getTime() + 24 * 60 * 60 * 1000)) {
      group = '今天';
    } else if (now >= yesterday && now < today) {
      group = '昨天';
    } else {
      group = now.toLocaleDateString('zh-CN', { year: 'numeric', month: '2-digit', day: '2-digit' }).replace(/\//g, '-');
    }

    const newConversation: Conversation = {
      key: Date.now().toString(),
      label: message.slice(0, 20) + (message.length > 20 ? '...' : ''),
      group: group,
    };
    setConversations(prev => [newConversation, ...prev]);
    setCurConversation(newConversation.key);
  }, []);

  // 使用自定义 hook 处理聊天逻辑
  const {
    messages,
    setMessages,
    onSubmit,
    loading,
    cancelRequest,
  } = useChat(handleFirstMessage);

  // 附件状态
  const [attachmentsOpen, setAttachmentsOpen] = useState(false);
  const [attachedFiles, setAttachedFiles] = useState<GetProp<typeof Attachments, 'items'>>([]);

  // 输入框状态
  const [inputValue, setInputValue] = useState('');

  // 侧边栏收起状态
  const [collapsed, setCollapsed] = useState(false);
  const toggleCollapsed = () => setCollapsed(!collapsed);

  // 处理取消请求
  const handleCancel = () => {
    cancelRequest();
  };

  return (
    <div className={styles.layout}>
      {/* 侧边栏 */}
      <ChatSider
        conversations={conversations}
        setConversations={setConversations}
        curConversation={curConversation}
        setCurConversation={setCurConversation}
        setMessages={setMessages}
        collapsed={collapsed}
        toggleCollapsed={toggleCollapsed}
      />

      {/* 聊天主区域 */}
      <div
        className={styles.chat}
        style={{
          justifyContent: !messages?.length ? 'center' : '',
          alignItems: !messages?.length ? 'center' : '',
          maxWidth: !messages?.length ? 800 : 1000,
        }}>
        {messages?.length ? (
          <ChatList
            messages={messages}
            setMessages={setMessages}
          />
        ) : (
          <Welcome
            variant="borderless"
            icon="https://avatars.githubusercontent.com/u/199323856?s=48&v=4"
            title="您好，我是您的酒店助手"
            description="我是一个基于ANP协议的酒店助手，可以为您提供酒店信息、预订、支付等服务。"
          />
        )}
        {/* 🌟 提示词 */}
        {messages?.length ? <Prompts
          items={SENDER_PROMPTS}
          onItemClick={(info) => {
            if (!loading) {
              onSubmit(info.data.description as string);
            }
          }}
          styles={{ item: { padding: '6px 12px' } }}
          className={styles.senderPrompt}
        /> : null}

        {/* 聊天输入区域 */}
        <ChatSender
          inputValue={inputValue}
          setInputValue={setInputValue}
          onSubmit={onSubmit}
          attachmentsOpen={attachmentsOpen}
          setAttachmentsOpen={setAttachmentsOpen}
          attachedFiles={attachedFiles}
          setAttachedFiles={setAttachedFiles}
          loading={loading}
          onCancel={handleCancel} // 传递 handleCancel 函数给 ChatSender
        />
      </div>
    </div>
  );
};

export default ChatPage;
