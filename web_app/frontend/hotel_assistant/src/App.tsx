import React, { useState, useEffect } from 'react';
import ChatPage from './components/ChatPage';
import Notifications from './components/Notifications';
import './App.css';

const App: React.FC = () => {
  const [notificationCount, setNotificationCount] = useState<number>(0);

  // 回调函数，用于从ChatPage获取通知计数
  const handleNotificationCountChange = (count: number) => {
    setNotificationCount(count);
  };

  return (
    <>
      <ChatPage onNotificationCountChange={handleNotificationCountChange} />
      <Notifications count={notificationCount} />
    </>
  );
};

export default App;
