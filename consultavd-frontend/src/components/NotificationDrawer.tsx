import React from 'react';
import {
  Drawer,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Typography,
  Box,
  IconButton,
  Badge,
  Divider,
  Chip,
} from '@mui/material';
import {
  Notifications as NotificationsIcon,
  Warning as WarningIcon,
  Error as ErrorIcon,
  CheckCircle as CheckCircleIcon,
  Info as InfoIcon,
  Close as CloseIcon,
} from '@mui/icons-material';

interface Notification {
  id: number;
  type: 'warning' | 'error' | 'info' | 'success';
  message: string;
  time: string;
  read?: boolean;
}

interface NotificationDrawerProps {
  open: boolean;
  onClose: () => void;
  notifications: Notification[];
  onMarkAsRead?: (id: number) => void;
}

const NotificationDrawer: React.FC<NotificationDrawerProps> = ({
  open,
  onClose,
  notifications,
  onMarkAsRead,
}) => {
  const getNotificationIcon = (type: string) => {
    switch (type) {
      case 'warning':
        return <WarningIcon color="warning" />;
      case 'error':
        return <ErrorIcon color="error" />;
      case 'success':
        return <CheckCircleIcon color="success" />;
      case 'info':
        return <InfoIcon color="info" />;
      default:
        return <InfoIcon color="info" />;
    }
  };

  const getNotificationColor = (type: string) => {
    switch (type) {
      case 'warning':
        return 'warning';
      case 'error':
        return 'error';
      case 'success':
        return 'success';
      case 'info':
        return 'info';
      default:
        return 'default';
    }
  };

  const unreadCount = notifications.filter(n => !n.read).length;

  return (
    <Drawer
      anchor="right"
      open={open}
      onClose={onClose}
      sx={{
        '& .MuiDrawer-paper': {
          width: 320,
          bgcolor: 'background.paper',
        },
      }}
    >
      <Box sx={{ p: 2, display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <Badge badgeContent={unreadCount} color="error">
            <NotificationsIcon />
          </Badge>
          <Typography variant="h6">Notificações</Typography>
        </Box>
        <IconButton onClick={onClose} size="small">
          <CloseIcon />
        </IconButton>
      </Box>
      
      <Divider />
      
      {notifications.length === 0 ? (
        <Box sx={{ p: 3, textAlign: 'center' }}>
          <Typography variant="body2" color="text.secondary">
            Nenhuma notificação
          </Typography>
        </Box>
      ) : (
        <List sx={{ p: 0 }}>
          {notifications.map((notification) => (
            <ListItem
              key={notification.id}
              sx={{
                bgcolor: notification.read ? 'transparent' : 'action.hover',
                borderLeft: `4px solid`,
                borderColor: `${getNotificationColor(notification.type)}.main`,
                '&:hover': {
                  bgcolor: 'action.selected',
                },
              }}
              onClick={() => onMarkAsRead?.(notification.id)}
            >
              <ListItemIcon>
                {getNotificationIcon(notification.type)}
              </ListItemIcon>
              <ListItemText
                primary={
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <Typography variant="body2" sx={{ flex: 1 }}>
                      {notification.message}
                    </Typography>
                    <Chip
                      label={notification.time}
                      size="small"
                      variant="outlined"
                      color={getNotificationColor(notification.type)}
                    />
                  </Box>
                }
                secondary={
                  <Typography variant="caption" color="text.secondary">
                    {notification.type.toUpperCase()}
                  </Typography>
                }
              />
            </ListItem>
          ))}
        </List>
      )}
    </Drawer>
  );
};

export default NotificationDrawer; 