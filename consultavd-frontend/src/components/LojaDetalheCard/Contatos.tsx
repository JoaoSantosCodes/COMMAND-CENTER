import React from 'react';
import { Box, Typography } from '@mui/material';
import PhoneIcon from '@mui/icons-material/Phone';
import EmailIcon from '@mui/icons-material/Email';

interface LojaContatosCardProps {
  data: any;
}

const LojaContatosCard: React.FC<LojaContatosCardProps> = ({ data }) => (
  <Box display="flex" flexDirection="column" gap={1}>
    <Box display="flex" alignItems="center" gap={1} mb={1}>
      <PhoneIcon color="action" />
      <Typography variant="subtitle2" color="text.secondary" fontWeight={700}>Contatos</Typography>
    </Box>
    <Typography variant="body1">Tel 1: <b>{data['TELEFONE1'] || '-'}</b></Typography>
    <Typography variant="body1">Tel 2: <b>{data['TELEFONE2'] || '-'}</b></Typography>
    <Typography variant="body1">Celular: <b>{data['CELULAR'] || '-'}</b></Typography>
    <Box display="flex" alignItems="center" gap={1} mt={1}>
      <EmailIcon color="action" />
      <Typography variant="body2" sx={{ wordBreak: 'break-all', overflowWrap: 'break-word', maxWidth: '100%', display: 'block' }}>{data['E_MAIL'] || '-'}</Typography>
    </Box>
  </Box>
);

export default LojaContatosCard; 