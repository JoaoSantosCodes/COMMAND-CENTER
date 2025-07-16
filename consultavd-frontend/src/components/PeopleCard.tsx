import React from 'react';
import { Box, Typography, Grid, Paper, Divider, Slide, useTheme } from '@mui/material';
import BadgeIcon from '@mui/icons-material/Badge';
import StoreIcon from '@mui/icons-material/Store';
import LocationOnIcon from '@mui/icons-material/LocationOn';

interface PeopleCardProps {
  data: any;
}

function getPeopleOrVDNovo(row: any) {
  return row['VD NOVO'] || row['People/PEOP'] || row['People'] || '-';
}

const GroupBlock: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const theme = useTheme();
  return (
    <Box
      sx={{
        bgcolor: theme.palette.mode === 'dark' ? 'rgba(255,255,255,0.01)' : 'rgba(0,0,0,0.01)',
        borderRadius: 2,
        p: { xs: 2, md: 2 },
        mb: 2,
        boxShadow: 0,
        border: `1px solid ${theme.palette.divider}`,
        minHeight: 60,
      }}
    >
      {children}
    </Box>
  );
};

const PeopleCard: React.FC<PeopleCardProps> = ({ data }) => {
  const theme = useTheme();
  if (!data) return null;
  return (
    <Slide in direction="up" timeout={600} mountOnEnter unmountOnExit>
      <Paper sx={{ p: { xs: 2, md: 3 }, mb: 2, borderRadius: 3, boxShadow: 6, bgcolor: 'background.paper', color: 'text.primary', transition: 'box-shadow 0.3s, transform 0.3s', '&:hover': { boxShadow: 12, transform: 'translateY(-4px) scale(1.01)' } }}>
        <Box display="flex" alignItems="center" gap={1} mb={1}>
          <BadgeIcon color="primary" />
          <Typography variant="h6" fontWeight={900} gutterBottom color="primary">
            Dados Principais
          </Typography>
        </Box>
        <Divider sx={{ mb: 2 }} />
        <Grid container spacing={2}>
          <Grid item xs={12} md={6}>
            <GroupBlock>
              <Typography variant="subtitle2" color="text.secondary">People/PEOP / VD NOVO</Typography>
              <Typography variant="h5" fontWeight={700}>{getPeopleOrVDNovo(data)}</Typography>
            </GroupBlock>
            <GroupBlock>
              <Typography variant="subtitle2" color="text.secondary">Status Loja</Typography>
              <Typography variant="body1" fontWeight={600}>{data['Status_Loja'] || data['STATUS'] || '-'}</Typography>
            </GroupBlock>
            <GroupBlock>
              <Box display="flex" alignItems="center" gap={1}>
                <StoreIcon color="action" fontSize="small" />
                <Typography variant="subtitle2" color="text.secondary">Loja</Typography>
              </Box>
              <Typography variant="body1">{data['LOJAS'] || '-'}</Typography>
            </GroupBlock>
            <GroupBlock>
              <Typography variant="subtitle2" color="text.secondary">Código</Typography>
              <Typography variant="body1">{data['CODIGO'] || '-'}</Typography>
            </GroupBlock>
          </Grid>
          <Grid item xs={12} md={6}>
            <GroupBlock>
              <Box display="flex" alignItems="center" gap={1}>
                <LocationOnIcon color="action" fontSize="small" />
                <Typography variant="subtitle2" color="text.secondary">Endereço</Typography>
              </Box>
              <Typography variant="body1">{data['ENDEREÇO'] || '-'}</Typography>
              <Typography variant="body2" color="text.secondary">
                Bairro: <b>{data['BAIRRO'] || '-'}</b> | Cidade: <b>{data['CIDADE'] || '-'}</b> | UF: <b>{data['UF'] || '-'}</b> | CEP: <b>{data['CEP'] || '-'}</b>
              </Typography>
            </GroupBlock>
            <GroupBlock>
              <Typography variant="subtitle2" color="text.secondary">2ª a 6ª</Typography>
              <Typography variant="body1">{data['2ª_a_6ª'] || data['2ª a 6ª'] || '-'}</Typography>
            </GroupBlock>
            <GroupBlock>
              <Typography variant="subtitle2" color="text.secondary">VD NOVO</Typography>
              <Typography variant="body1">{data['VD NOVO'] || '-'}</Typography>
            </GroupBlock>
          </Grid>
        </Grid>
      </Paper>
    </Slide>
  );
};

export default PeopleCard; 