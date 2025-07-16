import React from 'react';
import { Box, Typography } from '@mui/material';
import LocationOnIcon from '@mui/icons-material/LocationOn';

interface LojaEnderecoCardProps {
  data: any;
}

const LojaEnderecoCard: React.FC<LojaEnderecoCardProps> = ({ data }) => (
  <Box display="flex" flexDirection="column" gap={1}>
    <Box display="flex" alignItems="center" gap={1} mb={1}>
      <LocationOnIcon color="action" />
      <Typography variant="subtitle2" color="text.secondary" fontWeight={700}>Endereço</Typography>
    </Box>
    <Typography variant="body1" fontWeight={600}>{data['ENDEREÇO'] || '-'}</Typography>
    <Typography variant="body2" color="text.secondary">
      Bairro: <b>{data['BAIRRO'] || '-'}</b> | Cidade: <b>{data['CIDADE'] || '-'}</b> | UF: <b>{data['UF'] || '-'}</b>
    </Typography>
    <Typography variant="body2" color="text.secondary">CEP: <b>{data['CEP'] || '-'}</b></Typography>
  </Box>
);

export default LojaEnderecoCard; 