import React from 'react';
import { Box, Typography } from '@mui/material';
import AccessTimeIcon from '@mui/icons-material/AccessTime';

interface LojaFuncionamentoCardProps {
  data: any;
}

const LojaFuncionamentoCard: React.FC<LojaFuncionamentoCardProps> = ({ data }) => (
  <Box display="flex" flexDirection="column" gap={1}>
    <Box display="flex" alignItems="center" gap={1} mb={1}>
      <AccessTimeIcon color="action" />
      <Typography variant="subtitle2" color="text.secondary" fontWeight={700}>Funcionamento</Typography>
    </Box>
    <Typography variant="body2">2ª a 6ª: <b>{data['2ª_a_6ª'] || data['2ª a 6ª'] || '-'}</b></Typography>
    <Typography variant="body2">Sábado: <b>{data['SAB'] || '-'}</b></Typography>
    <Typography variant="body2">Domingo: <b>{data['DOM'] || '-'}</b></Typography>
    <Typography variant="body2">Func.: <b>{data['FUNC.'] || '-'}</b></Typography>
  </Box>
);

export default LojaFuncionamentoCard; 