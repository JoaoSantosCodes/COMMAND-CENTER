import React from 'react';
import { Box, Typography } from '@mui/material';
import BusinessIcon from '@mui/icons-material/Business';

interface LojaStatusExtraCardProps {
  data: any;
}

const LojaStatusExtraCard: React.FC<LojaStatusExtraCardProps> = ({ data }) => (
  <Box display="flex" flexDirection="column" gap={1}>
    <Box display="flex" alignItems="center" gap={1} mb={1}>
      <BusinessIcon color="action" />
      <Typography variant="subtitle2" color="text.secondary" fontWeight={700}>Status Extra</Typography>
    </Box>
    <Typography variant="body2">VD NOVO: <b>{data['VD NOVO'] || '-'}</b></Typography>
  </Box>
);

export default LojaStatusExtraCard; 