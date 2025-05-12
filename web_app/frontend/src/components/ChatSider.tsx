import React from 'react';
import { Avatar, Button } from 'antd';
import { Conversations } from '@ant-design/x';
import { 
  CommentOutlined,
  DeleteOutlined, 
  EditOutlined, 
  MenuFoldOutlined, 
  MenuUnfoldOutlined, 
  PlusOutlined, 
  QuestionCircleOutlined 
} from '@ant-design/icons';
import dayjs from 'dayjs';
import { useStyles } from '../styles/useStyles';
import { DEFAULT_CONVERSATIONS_ITEMS } from '../constants/chatData';

interface ChatSiderProps {
  conversations: typeof DEFAULT_CONVERSATIONS_ITEMS;
  setConversations: React.Dispatch<React.SetStateAction<typeof DEFAULT_CONVERSATIONS_ITEMS>>;
  curConversation: string;
  setCurConversation: React.Dispatch<React.SetStateAction<string>>;
  setMessages: React.Dispatch<React.SetStateAction<any[]>>;
  messageHistory: Record<string, any>;
  abortController: React.RefObject<AbortController | null>;
  collapsed: boolean;
  toggleCollapsed: () => void;
}

const ChatSider: React.FC<ChatSiderProps> = ({
  conversations,
  setConversations,
  curConversation,
  setCurConversation,
  setMessages,
  messageHistory,
  abortController,
  collapsed,
  toggleCollapsed,
}) => {
  const { styles } = useStyles();

  return (
    <div className={`${styles.sider} ${collapsed ? styles.collapsed : ''}`}>
      {/* 收起/展开按钮 */}
      <div className={styles.toggleBtn} onClick={toggleCollapsed}>
        {collapsed ? <MenuUnfoldOutlined /> : <MenuFoldOutlined />}
      </div>
      
      {/* 🌟 Logo */}
      <div className={`${styles.logo} logo`}>
        <img
          src="https://avatars.githubusercontent.com/u/199323856?s=48&v=4"
          draggable={false}
          alt="logo"
          width={24}
          height={24}
        />
        {!collapsed && <span>ANP</span>}
      </div>

      {/* 🌟 添加会话 */}
      <Button
        onClick={() => {
          const now = dayjs().valueOf().toString();
          setConversations([
            {
              key: now,
              label: `新对话 ${conversations.length + 1}`,
              group: '今天',
            },
            ...conversations,
          ]);
          setCurConversation(now);
          setMessages([]);
        }}
        type="link"
        className={styles.addBtn}
        icon={<PlusOutlined />}
      >
        {!collapsed && "新对话"}
      </Button>

      {/* 🌟 会话管理 - 在非折叠状态下显示 */}
      {!collapsed && (
        <Conversations
          items={conversations}
          className={styles.conversations}
          activeKey={curConversation}
          onActiveChange={async (val) => {
            abortController.current?.abort();
            // The abort execution will trigger an asynchronous requestFallback, which may lead to timing issues.
            // In future versions, the sessionId capability will be added to resolve this problem.
            setTimeout(() => {
              setCurConversation(val);
              setMessages(messageHistory?.[val] || []);
            }, 100);
          }}
          groupable
          styles={{ item: { padding: '0 8px' } }}
          menu={(conversation) => ({
            items: [
              {
                label: 'Rename',
                key: 'rename',
                icon: <EditOutlined />,
              },
              {
                label: 'Delete',
                key: 'delete',
                icon: <DeleteOutlined />,
                danger: true,
                onClick: () => {
                  const newList = conversations.filter((item) => item.key !== conversation.key);
                  const newKey = newList?.[0]?.key;
                  setConversations(newList);
                  // The delete operation modifies curConversation and triggers onActiveChange, so it needs to be executed with a delay to ensure it overrides correctly at the end.
                  // This feature will be fixed in a future version.
                  setTimeout(() => {
                    if (conversation.key === curConversation) {
                      setCurConversation(newKey);
                      setMessages(messageHistory?.[newKey] || []);
                    }
                  }, 200);
                },
              },
            ],
          })}
        />
      )}

      {/* 用户头像 */}
      {collapsed ? (
        <div className="siderFooter-collapsed">
          <Avatar size={24} />
        </div>
      ) : (
        <div className={styles.siderFooter}>
          <Avatar size={24} />
          <Button type="text" icon={<QuestionCircleOutlined />} />
        </div>
      )}
    </div>
  );
};

export default ChatSider;
