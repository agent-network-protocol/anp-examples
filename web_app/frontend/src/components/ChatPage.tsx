import React, { useEffect, useState } from 'react';
import { useStyles } from '../styles/useStyles';
import { useChat } from '../hooks/useChat';
import ChatSider from './ChatSider';
import ChatList from './ChatList';
import ChatSender from './ChatSender';
import { DEFAULT_CONVERSATIONS_ITEMS } from '../constants/chatData';
import type { GetProp } from 'antd';
import { Attachments } from '@ant-design/x';

const ChatPage: React.FC = () => {
  const { styles } = useStyles();
  
  // 使用自定义 hook 处理聊天逻辑
  const {
    abortController,
    messageHistory,
    setMessageHistory,
    loading,
    messages,
    setMessages,
    onSubmit,
    updateMessageHistory,
  } = useChat();

  // 会话状态
  const [conversations, setConversations] = useState(DEFAULT_CONVERSATIONS_ITEMS);
  const [curConversation, setCurConversation] = useState(DEFAULT_CONVERSATIONS_ITEMS[0].key);

  // 附件状态
  const [attachmentsOpen, setAttachmentsOpen] = useState(false);
  const [attachedFiles, setAttachedFiles] = useState<GetProp<typeof Attachments, 'items'>>([]);

  // 输入框状态
  const [inputValue, setInputValue] = useState('');

  // 侧边栏收起状态
  const [collapsed, setCollapsed] = useState(false);
  const toggleCollapsed = () => setCollapsed(!collapsed);

  // 更新消息历史
  useEffect(() => {
    updateMessageHistory(curConversation);
  }, [messages, curConversation]);

  return (
    <div className={styles.layout}>
      {/* 侧边栏 */}
      <ChatSider
        conversations={conversations}
        setConversations={setConversations}
        curConversation={curConversation}
        setCurConversation={setCurConversation}
        setMessages={setMessages}
        messageHistory={messageHistory}
        abortController={abortController}
        collapsed={collapsed}
        toggleCollapsed={toggleCollapsed}
      />

      {/* 聊天主区域 */}
      <div className={styles.chat}>
        {/* 聊天列表 */}
        <ChatList
          messages={messages}
          onSubmit={onSubmit}
          loading={loading}
        />
        
        {/* 聊天输入区域 */}
        <ChatSender
          inputValue={inputValue}
          setInputValue={setInputValue}
          onSubmit={onSubmit}
          loading={loading}
          attachmentsOpen={attachmentsOpen}
          setAttachmentsOpen={setAttachmentsOpen}
          attachedFiles={attachedFiles}
          setAttachedFiles={setAttachedFiles}
        />
      </div>
    </div>
  );
};

export default ChatPage;
