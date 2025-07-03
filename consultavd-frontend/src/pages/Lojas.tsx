import React, { useEffect, useState } from 'react';
import DataTable from '../components/DataTable';
import { apiService } from '../services/api';
import { Loja, TableColumn } from '../types';
import { Box, Typography, CircularProgress, Alert, Button } from '@mui/material';

const columns: TableColumn[] = [
  { field: 'id', headerName: 'ID', width: 80 },
  { field: 'nome', headerName: 'Nome', width: 200 },
  { field: 'endereco', headerName: 'Endereço', width: 220 },
  { field: 'cidade', headerName: 'Cidade', width: 120 },
  { field: 'uf', headerName: 'UF', width: 60 },
  { field: 'status', headerName: 'Status', width: 100 },
];

const Lojas: React.FC = () => {
  const [lojas, setLojas] = useState<Loja[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    apiService.getLojas()
      .then(res => setLojas(res.data || []))
      .catch(() => setError('Erro ao carregar lojas'))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <Box display="flex" justifyContent="center" alignItems="center" minHeight={300}><CircularProgress /></Box>;
  if (error) return <Alert severity="error">{error}</Alert>;

  return (
    <Box>
      <Box display="flex" alignItems="center" justifyContent="space-between" mb={2}>
        <Typography variant="h5" fontWeight={700}>Lojas</Typography>
        <Button variant="contained" color="primary">Nova Loja</Button>
      </Box>
      <DataTable rows={lojas} columns={columns} />
    </Box>
  );
};

export default Lojas; 