import React, { useState } from 'react';
import { Box, Typography, Grid, Paper, Divider, IconButton, Tooltip, Slide, useTheme } from '@mui/material';
import EmailIcon from '@mui/icons-material/Email';
import PhoneIcon from '@mui/icons-material/Phone';
import SmartphoneIcon from '@mui/icons-material/Smartphone';
import ContentCopyIcon from '@mui/icons-material/ContentCopy';
import AccessTimeIcon from '@mui/icons-material/AccessTime';
import PersonIcon from '@mui/icons-material/Person';

interface PeopleContactCardProps {
  data: any;
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

export const PeopleContactCard: React.FC<PeopleContactCardProps> = ({ data }) => {
  const [copied, setCopied] = useState<string | null>(null);
  const theme = useTheme();
  if (!data) return null;

  const handleCopy = async (text: string, label: string) => {
    await navigator.clipboard.writeText(text);
    setCopied(label);
    setTimeout(() => setCopied(null), 1500);
  };

  return (
    <Slide in direction="up" timeout={600} mountOnEnter unmountOnExit>
      <Paper
        sx={{
          p: { xs: 2, md: 3 },
          mb: 2,
          borderRadius: 3,
          boxShadow: 6,
          bgcolor: 'background.paper',
          color: 'text.primary',
          transition: 'box-shadow 0.3s, transform 0.3s',
          '&:hover': {
            boxShadow: 12,
            transform: 'translateY(-4px) scale(1.01)',
          },
        }}
      >
        <Box display="flex" alignItems="center" gap={1} mb={1}>
          <PhoneIcon color="primary" />
          <Typography variant="h6" fontWeight={900} gutterBottom color="primary">
            Contatos e Informações Adicionais
          </Typography>
        </Box>
        <Divider sx={{ mb: 2 }} />
        <Grid container spacing={2}>
          <Grid item xs={12} md={6}>
            <GroupBlock>
              <Box display="flex" alignItems="center" gap={1}>
                <PhoneIcon color="action" fontSize="small" />
                <Typography variant="subtitle2" color="text.secondary">Telefone 1</Typography>
              </Box>
              <Typography variant="body1">{data['TELEFONE1'] || '-'}</Typography>
            </GroupBlock>
            <GroupBlock>
              <Box display="flex" alignItems="center" gap={1}>
                <PhoneIcon color="action" fontSize="small" />
                <Typography variant="subtitle2" color="text.secondary">Telefone 2</Typography>
              </Box>
              <Typography variant="body1">{data['TELEFONE2'] || '-'}</Typography>
            </GroupBlock>
            <GroupBlock>
              <Box display="flex" alignItems="center" gap={1}>
                <SmartphoneIcon color="action" fontSize="small" />
                <Typography variant="subtitle2" color="text.secondary">Celular</Typography>
                {data['CELULAR'] && (
                  <Tooltip title={copied === 'celular' ? 'Copiado!' : 'Copiar'}>
                    <IconButton size="small" onClick={() => handleCopy(data['CELULAR'], 'celular')}>
                      <ContentCopyIcon fontSize="inherit" />
                    </IconButton>
                  </Tooltip>
                )}
              </Box>
              <Typography variant="body1">{data['CELULAR'] || '-'}</Typography>
            </GroupBlock>
            <GroupBlock>
              <Box display="flex" alignItems="center" gap={1}>
                <EmailIcon color="action" fontSize="small" />
                <Typography variant="subtitle2" color="text.secondary">E-mail</Typography>
                {data['E_MAIL'] && (
                  <Tooltip title={copied === 'email' ? 'Copiado!' : 'Copiar'}>
                    <IconButton size="small" onClick={() => handleCopy(data['E_MAIL'], 'email')}>
                      <ContentCopyIcon fontSize="inherit" />
                    </IconButton>
                  </Tooltip>
                )}
              </Box>
              <Typography
                variant="body1"
                sx={{
                  wordBreak: 'break-all',
                  overflowWrap: 'break-word',
                  maxWidth: '100%',
                  display: 'block',
                }}
              >
                {data['E_MAIL'] || '-'}
              </Typography>
            </GroupBlock>
          </Grid>
          <Grid item xs={12} md={6}>
            <GroupBlock>
              <Box display="flex" alignItems="center" gap={1}>
                <AccessTimeIcon color="action" fontSize="small" />
                <Typography variant="subtitle2" color="text.secondary">Sábado</Typography>
              </Box>
              <Typography variant="body1">{data['SAB'] || '-'}</Typography>
            </GroupBlock>
            <GroupBlock>
              <Box display="flex" alignItems="center" gap={1}>
                <AccessTimeIcon color="action" fontSize="small" />
                <Typography variant="subtitle2" color="text.secondary">Domingo</Typography>
              </Box>
              <Typography variant="body1">{data['DOM'] || '-'}</Typography>
            </GroupBlock>
            <GroupBlock>
              <Box display="flex" alignItems="center" gap={1}>
                <AccessTimeIcon color="action" fontSize="small" />
                <Typography variant="subtitle2" color="text.secondary">Funcionamento</Typography>
              </Box>
              <Typography variant="body1">{data['FUNC.'] || '-'}</Typography>
            </GroupBlock>
            <GroupBlock>
              <Box display="flex" alignItems="center" gap={1}>
                <PersonIcon color="action" fontSize="small" />
                <Typography variant="subtitle2" color="text.secondary">Nome GGL</Typography>
              </Box>
              <Typography variant="body1">{data['NOME_GGL'] || '-'}</Typography>
            </GroupBlock>
            <GroupBlock>
              <Box display="flex" alignItems="center" gap={1}>
                <PersonIcon color="action" fontSize="small" />
                <Typography variant="subtitle2" color="text.secondary">Nome GR</Typography>
              </Box>
              <Typography variant="body1">{data['NOME_GR'] || '-'}</Typography>
            </GroupBlock>
          </Grid>
        </Grid>
      </Paper>
    </Slide>
  );
};

export default PeopleContactCard; 