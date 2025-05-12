import {
  AppstoreAddOutlined,
  CommentOutlined,
  FileSearchOutlined,
  HeartOutlined,
  PaperClipOutlined,
  ProductOutlined,
  ScheduleOutlined,
  SmileOutlined,
} from '@ant-design/icons';
import type { GetProp } from 'antd';
import { Prompts } from '@ant-design/x';
import React from 'react';

// 默认会话列表
export const DEFAULT_CONVERSATIONS_ITEMS = [
  {
    key: 'default-0',
    label: 'What is ANP?',
    group: '今天',
  },
  {
    key: 'default-1',
    label: 'How to quickly install and import components?',
    group: '今天',
  },
  {
    key: 'default-2',
    label: 'New AGI Hybrid Interface',
    group: '昨天',
  },
];

// 热门话题
export const HOT_TOPICS = {
  key: '1',
  label: 'Hot Topics',
  children: [
    {
      key: '1-1',
      description: 'What has ANP upgraded?',
      icon: React.createElement('span', { style: { color: '#f93a4a', fontWeight: 700 } }, '1'),
    },
    {
      key: '1-2',
      description: 'New AGI Hybrid Interface',
      icon: React.createElement('span', { style: { color: '#ff6565', fontWeight: 700 } }, '2'),
    },
    {
      key: '1-3',
      description: 'What components are in ANP?',
      icon: React.createElement('span', { style: { color: '#ff8f1f', fontWeight: 700 } }, '3'),
    },
    {
      key: '1-4',
      description: 'Come and discover the new design paradigm of the AI era.',
      icon: React.createElement('span', { style: { color: '#00000040', fontWeight: 700 } }, '4'),
    },
    {
      key: '1-5',
      description: 'How to quickly install and import components?',
      icon: React.createElement('span', { style: { color: '#00000040', fontWeight: 700 } }, '5'),
    },
  ],
};

// 设计指南
export const DESIGN_GUIDE = {
  key: '2',
  label: 'Design Guide',
  children: [
    {
      key: '2-1',
      icon: React.createElement(HeartOutlined),
      label: 'Intention',
      description: 'AI understands user needs and provides solutions.',
    },
    {
      key: '2-2',
      icon: React.createElement(SmileOutlined),
      label: 'Role',
      description: "AI's public persona and image",
    },
    {
      key: '2-3',
      icon: React.createElement(CommentOutlined),
      label: 'Chat',
      description: 'How AI Can Express Itself in a Way Users Understand',
    },
    {
      key: '2-4',
      icon: React.createElement(PaperClipOutlined),
      label: 'Interface',
      description: 'AI balances "chat" & "do" behaviors.',
    },
  ],
};

// 发送器提示
export const SENDER_PROMPTS: GetProp<typeof Prompts, 'items'> = [
  {
    key: '1',
    description: 'Upgrades',
    icon: React.createElement(ScheduleOutlined),
  },
  {
    key: '2',
    description: 'Components',
    icon: React.createElement(ProductOutlined),
  },
  {
    key: '3',
    description: 'RICH Guide',
    icon: React.createElement(FileSearchOutlined),
  },
  {
    key: '4',
    description: 'Installation Introduction',
    icon: React.createElement(AppstoreAddOutlined),
  },
];

// AI 配置
export const AI_CONFIG = {
  apiKey: `Bearer ${import.meta.env.VITE_AI_API_KEY}`,
  baseURL: `${import.meta.env.VITE_AI_BASE_URL}/chat/completions`,
  model: import.meta.env.VITE_AI_MODEL,
};
