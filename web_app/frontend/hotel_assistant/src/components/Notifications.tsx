import React from 'react';
import { Box, Badge, IconButton } from '@mui/material';
import NotificationsIcon from '@mui/icons-material/Notifications';

/**
 * Notification button component that only shows notification count
 */
interface NotificationsProps {
  count: number;
}

const Notifications: React.FC<NotificationsProps> = ({ count }) => {

  return (
    <Box>
      {/* Notification Icon with Badge */}
      <IconButton 
        color="primary" 
        sx={{ position: 'fixed', top: 10, right: 10, zIndex: 1000 }}
      >
        <Badge badgeContent={count} color="error">
          <NotificationsIcon />
        </Badge>
      </IconButton>
    </Box>
  );
};

export default Notifications;
