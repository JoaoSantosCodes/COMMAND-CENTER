import React from 'react';
import { Box, Typography, Chip } from '@mui/material';
import BusinessIcon from '@mui/icons-material/Business';

interface LojaTituloCardProps {
  data: any;
}

function getPeopleOrVDNovo(row: any) {
  return row['VD NOVO'] || row['People/PEOP'] || row['People'] || '-';
}

const LojaTituloCard: React.FC<LojaTituloCardProps> = ({ data }) => (
  <>
    <Box display="flex" alignItems="center" gap={2} mb={2} width="100%" justifyContent="center">
      <BusinessIcon color="primary" fontSize="large" />
      <Typography
        variant="h5"
        fontWeight={900}
        color="primary.main"
        textAlign="center"
        sx={{
          wordBreak: 'normal',
          whiteSpace: 'normal',
          overflowWrap: 'break-word',
          maxWidth: { xs: '90vw', md: '700px' },
          lineHeight: 1.1,
          letterSpacing: 0.5,
        }}
      >
        {data['LOJAS'] || '-'}
      </Typography>
      <Chip label={data['Status_Loja'] || data['STATUS'] || '-'} color={data['Status_Loja'] === 'ATIVA' ? 'success' : 'default'} sx={{ fontWeight: 700, fontSize: 16, ml: 2, px: 2, height: 32 }} />
    </Box>
    <Typography variant="subtitle1" color="text.secondary" mb={2} textAlign="center">
      Código: <b>{data['CODIGO'] || '-'}</b> &nbsp;|&nbsp; People/PEOP/VD NOVO: <b>{getPeopleOrVDNovo(data)}</b>
    </Typography>
  </>
);

export default LojaTituloCard; 