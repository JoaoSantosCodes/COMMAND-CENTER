import React, { useState } from 'react';
import { Box, Typography, Button, Paper, TextField, Snackbar, Alert } from '@mui/material';

interface CarimboGeneratorProps {
  data: any;
}

function getPeopleOrVDNovo(row: any) {
  return row['VD NOVO'] || row['People/PEOP'] || row['People'] || '-';
}

function gerarCarimbo(data: any) {
  const now = new Date();
  const dataHora = now.toLocaleString('pt-BR');
  return `**CARIMBO - CONSULTA VD**\n` +
    `Data/Hora: ${dataHora}\n` +
    `People/PEOP: ${getPeopleOrVDNovo(data)}\n` +
    `Loja: ${data['LOJAS'] || '-'}\n` +
    `Endereço: ${data['ENDEREÇO'] || '-'}\n` +
    `Bairro: ${data['BAIRRO'] || '-'}\n` +
    `Cidade: ${data['CIDADE'] || '-'}\n` +
    `UF: ${data['UF'] || '-'}\n` +
    `CEP: ${data['CEP'] || '-'}\n` +
    `Status: ${data['Status_Loja'] || data['STATUS'] || '-'}\n` +
    `2ª a 6ª: ${data['2ª_a_6ª'] || data['2ª a 6ª'] || '-'}\n` +
    `SAB: ${data['SAB'] || '-'}\n` +
    `DOM: ${data['DOM'] || '-'}\n` +
    `FUNC: ${data['FUNC.'] || '-'}\n` +
    `Telefone: ${data['TELEFONE1'] || '-'}\n` +
    `E-mail: ${data['E_MAIL'] || '-'}\n`;
}

const CarimboGenerator: React.FC<CarimboGeneratorProps> = ({ data }) => {
  const [open, setOpen] = useState(false);
  if (!data) return null;
  const carimbo = gerarCarimbo(data);

  const handleCopy = async () => {
    await navigator.clipboard.writeText(carimbo);
    setOpen(true);
  };

  return (
    <Paper sx={{ p: 3, mb: 2, borderRadius: 3, boxShadow: 2, bgcolor: 'background.paper', color: 'text.primary' }}>
      <Box display="flex" alignItems="center" justifyContent="space-between" mb={1}>
        <Typography variant="h6" fontWeight={900} color="primary">Carimbo de Consulta</Typography>
        <Button variant="contained" color="primary" onClick={handleCopy}>Copiar Carimbo</Button>
      </Box>
      <TextField
        multiline
        fullWidth
        minRows={6}
        value={carimbo}
        InputProps={{ readOnly: true }}
        sx={{ fontFamily: 'monospace', bgcolor: 'background.paper', color: 'text.primary' }}
      />
      <Snackbar open={open} autoHideDuration={2000} onClose={() => setOpen(false)}>
        <Alert severity="success" sx={{ width: '100%' }}>
          Carimbo copiado para a área de transferência!
        </Alert>
      </Snackbar>
    </Paper>
  );
};

export default CarimboGenerator; 