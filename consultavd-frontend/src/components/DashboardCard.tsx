import React from 'react';
import { Box, Typography, Paper, useTheme, Slide } from '@mui/material';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import TrendingDownIcon from '@mui/icons-material/TrendingDown';

interface DashboardCardProps {
  title: string;
  value: string;
  icon: string;
  color: 'primary' | 'secondary' | 'success' | 'error' | 'warning' | 'info';
  trend?: {
    value: number;
    isPositive: boolean;
  };
  subtitle?: string;
}

const DashboardCard: React.FC<DashboardCardProps> = ({ title, value, icon, color, trend, subtitle }) => {
  const theme = useTheme();
  
  return (
    <Slide in direction="up" timeout={600} mountOnEnter unmountOnExit>
      <Paper 
        sx={{ 
          p: { xs: 2, md: 3 }, 
          borderRadius: 4, 
          boxShadow: 6, 
          bgcolor: 'background.paper', 
          color: 'text.primary', 
          minWidth: 180,
          maxWidth: 260,
          mx: 'auto',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          transition: 'all 0.3s ease', 
          '&:hover': { 
            boxShadow: 12, 
            transform: 'translateY(-4px) scale(1.02)',
            '& .card-icon': {
              transform: 'scale(1.1)',
            }
          },
          position: 'relative',
          overflow: 'hidden',
          '&::before': {
            content: '""',
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            height: 3,
            background: `linear-gradient(90deg, ${theme.palette[color].main}, ${theme.palette[color].light})`,
          }
        }}
      >
        <Box width="100%" display="flex" justifyContent="flex-end" alignItems="center" mb={0.5}>
          {trend && (
            <Box display="flex" alignItems="center" gap={0.5}>
              {trend.isPositive ? (
                <TrendingUpIcon color="success" fontSize="small" />
              ) : (
                <TrendingDownIcon color="error" fontSize="small" />
              )}
              <Typography 
                variant="body2" 
                color={trend.isPositive ? 'success.main' : 'error.main'}
                fontWeight={600}
              >
                {trend.isPositive ? '+' : ''}{trend.value}%
              </Typography>
            </Box>
          )}
        </Box>
        
        <Box display="flex" flexDirection="column" alignItems="center" justifyContent="center" width="100%" mb={1}>
          <Typography 
            variant="h2" 
            component="span" 
            color={color} 
            className="card-icon"
            sx={{ 
              fontSize: 48, 
              mb: 0.5, 
              lineHeight: 1,
              transition: 'transform 0.3s ease',
              filter: 'drop-shadow(0 2px 4px rgba(0,0,0,0.1))'
            }}
          >
            {icon}
          </Typography>
          <Typography 
            variant="h3" 
            fontWeight={900} 
            color={color} 
            sx={{ 
              fontSize: 32, 
              mb: 0.5, 
              lineHeight: 1,
              textShadow: '0 1px 2px rgba(0,0,0,0.1)'
            }}
          >
            {value}
          </Typography>
        </Box>
        
        <Typography 
          variant="subtitle1" 
          fontWeight={600} 
          color="text.secondary" 
          align="center" 
          sx={{ 
            fontSize: 16, 
            mt: 0.5,
            mb: subtitle ? 0.5 : 0
          }}
        >
          {title}
        </Typography>
        
        {subtitle && (
          <Typography 
            variant="caption" 
            color="text.secondary" 
            align="center" 
            sx={{ 
              fontSize: 12,
              opacity: 0.8,
              fontStyle: 'italic'
            }}
          >
            {subtitle}
          </Typography>
        )}
      </Paper>
    </Slide>
  );
};

export default DashboardCard; 