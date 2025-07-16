import React from 'react';
import { Box, Typography } from '@mui/material';
import PersonIcon from '@mui/icons-material/Person';

interface LojaGestoresCardProps {
  data: any;
}

const LojaGestoresCard: React.FC<LojaGestoresCardProps> = ({ data }) => (
  <Box display="flex" flexDirection="column" gap={1}>
    <Box display="flex" alignItems="center" gap={1} mb={1}>
      <PersonIcon color="action" />
      <Typography variant="subtitle2" color="text.secondary" fontWeight={700}>Gestores</Typography>
    </Box>
    <Typography variant="body2">GGL: <b>{data['NOME_GGL'] || '-'}</b></Typography>
    <Typography variant="body2">GR: <b>{data['NOME_GR'] || '-'}</b></Typography>
  </Box>
);

export default LojaGestoresCard; 