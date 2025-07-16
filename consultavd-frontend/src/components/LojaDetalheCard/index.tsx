import React from 'react';
import { Box, Paper, Divider, Grid, useTheme, Slide } from '@mui/material';
import LojaTituloCard from './Titulo';
import LojaEnderecoCard from './Endereco';
import LojaContatosCard from './Contatos';
import LojaFuncionamentoCard from './Funcionamento';
import LojaGestoresCard from './Gestores';
import LojaStatusExtraCard from './StatusExtra';

interface LojaDetalheCardProps {
  data: any;
}

const AnimatedBlock: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const theme = useTheme();
  return (
    <Box
      sx={{
        bgcolor: theme.palette.mode === 'dark' ? 'rgba(255,255,255,0.02)' : 'rgba(0,0,0,0.03)',
        borderRadius: 3,
        p: 2,
        mb: 2,
        boxShadow: 1,
        transition: 'box-shadow 0.3s, background 0.3s',
        '&:hover': {
          boxShadow: 4,
          bgcolor: theme.palette.mode === 'dark' ? 'rgba(255,255,255,0.06)' : 'rgba(0,0,0,0.07)',
        },
      }}
    >
      {children}
    </Box>
  );
};

const LojaDetalheCard: React.FC<LojaDetalheCardProps> = ({ data }) => {
  const theme = useTheme();
  if (!data) return null;
  return (
    <Slide in direction="up" timeout={600} mountOnEnter unmountOnExit>
      <Box display="flex" justifyContent="center" alignItems="flex-start" width="100%" mb={4}>
        <Paper sx={{
          p: { xs: 3, md: 5 },
          borderRadius: 6,
          boxShadow: 6,
          maxWidth: 900,
          width: '100%',
          minHeight: 340,
          background: theme.palette.background.paper,
          color: theme.palette.text.primary,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          border: `1.5px solid ${theme.palette.divider}`,
          transition: 'box-shadow 0.3s, transform 0.3s',
          '&:hover': {
            boxShadow: 12,
            transform: 'translateY(-4px) scale(1.01)',
          },
        }}>
          <LojaTituloCard data={data} />
          <Divider sx={{ mb: 3, width: '100%' }} />
          <Grid container spacing={4}>
            <Grid item xs={12} sm={6}>
              <AnimatedBlock><LojaEnderecoCard data={data} /></AnimatedBlock>
            </Grid>
            <Grid item xs={12} sm={6}>
              <AnimatedBlock><LojaContatosCard data={data} /></AnimatedBlock>
            </Grid>
          </Grid>
          <Divider sx={{ my: 3, width: '100%' }} />
          <Grid container spacing={4}>
            <Grid item xs={12} sm={4}>
              <AnimatedBlock><LojaFuncionamentoCard data={data} /></AnimatedBlock>
            </Grid>
            <Grid item xs={12} sm={4}>
              <AnimatedBlock><LojaGestoresCard data={data} /></AnimatedBlock>
            </Grid>
            <Grid item xs={12} sm={4}>
              <AnimatedBlock><LojaStatusExtraCard data={data} /></AnimatedBlock>
            </Grid>
          </Grid>
        </Paper>
      </Box>
    </Slide>
  );
};

export default LojaDetalheCard; 