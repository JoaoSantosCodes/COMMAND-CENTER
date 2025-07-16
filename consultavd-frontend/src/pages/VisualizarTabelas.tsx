import React, { useEffect, useState } from 'react';
import { Box, Typography, Paper, CircularProgress, Alert, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Autocomplete, TextField, Button, Chip, Stack, Tooltip, useTheme } from '@mui/material';
import FileDownloadIcon from '@mui/icons-material/FileDownload';
import apiService from '../services/api';

const VisualizarTabelas: React.FC = () => {
  const theme = useTheme();
  const [tables, setTables] = useState<string[]>([]);
  const [selected, setSelected] = useState<string | null>(null);
  const [data, setData] = useState<any[]>([]);
  const [columns, setColumns] = useState<string[]>([]);
  const [types, setTypes] = useState<{ [col: string]: string } | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState(0);
  const pageSize = 50;
  const [showAllCols, setShowAllCols] = useState(false);
  const maxCols = 8;

  // Buscar tabelas ao montar
  useEffect(() => {
    const fetchTables = async () => {
      setLoading(true);
      setError(null);
      try {
        const resp = await apiService.executeSQL("SELECT name FROM sqlite_master WHERE type='table';");
        setTables(resp.data.map((row: any) => row.name));
      } catch (e: any) {
        setError('Erro ao buscar tabelas.');
      }
      setLoading(false);
    };
    fetchTables();
  }, []);

  // Buscar dados e estrutura ao selecionar tabela
  useEffect(() => {
    if (!selected) return;
    const fetchData = async () => {
      setLoading(true);
      setError(null);
      try {
        const resp = await apiService.executeSQL(`SELECT * FROM ${selected} LIMIT ${pageSize} OFFSET ${page * pageSize}`);
        setData(resp.data);
        setColumns(resp.columns);
        setTypes(null);
      } catch (e: any) {
        setError(e?.response?.data?.detail || 'Erro ao buscar dados da tabela.');
        setData([]);
        setColumns([]);
        setTypes(null);
      }
      setLoading(false);
    };
    fetchData();
  }, [selected, page]);

  const handleExport = () => {
    if (!data || columns.length === 0) return;
    const csv = [columns.join(',')].concat(data.map(row => columns.map(col => row[col]).join(','))).join('\n');
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${selected}_dados.csv`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <Box p={3} sx={{ maxWidth: 1100, margin: '0 auto' }}>
      <Typography variant="h4" gutterBottom>Visualizar Tabelas</Typography>
      <Paper sx={{ p: 3, mb: 2, background: theme.palette.background.paper }}>
        <Stack direction={{ xs: 'column', sm: 'row' }} spacing={2} alignItems="center" mb={2}>
          <Autocomplete
            options={tables}
            value={selected}
            onChange={(_e, v) => { setSelected(v); setPage(0); }}
            renderInput={params => <TextField {...params} label="Selecione uma tabela" size="small" />}
            sx={{ minWidth: 300 }}
            disabled={loading || tables.length === 0}
          />
          {selected && (
            <Button variant="outlined" color="success" startIcon={<FileDownloadIcon />} onClick={handleExport} disabled={!data.length}>
              Exportar Dados
            </Button>
          )}
        </Stack>
        {loading && <Box display="flex" justifyContent="center" alignItems="center" minHeight={120}><CircularProgress size={40} /></Box>}
        {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
        {selected && columns.length > 0 && !loading && (
          <>
            <Box mb={2}>
              <Typography variant="subtitle1" fontWeight={600}>Estrutura da Tabela</Typography>
              <Box display="flex" flexWrap="wrap" gap={1}>
                {(showAllCols ? columns : columns.slice(0, maxCols)).map(col => (
                  <Chip key={col} label={col} size="small" sx={{ fontWeight: 600, maxWidth: 260, textOverflow: 'ellipsis', overflow: 'hidden' }} />
                ))}
                {columns.length > maxCols && !showAllCols && (
                  <Chip
                    label={`+${columns.length - maxCols} mais`}
                    size="small"
                    color="primary"
                    clickable
                    onClick={() => setShowAllCols(true)}
                    sx={{ fontWeight: 600 }}
                  />
                )}
                {columns.length > maxCols && showAllCols && (
                  <Chip
                    label="Mostrar menos"
                    size="small"
                    color="secondary"
                    clickable
                    onClick={() => setShowAllCols(false)}
                    sx={{ fontWeight: 600 }}
                  />
                )}
              </Box>
            </Box>
            <TableContainer sx={{ maxHeight: 400, borderRadius: 2, boxShadow: 1, overflowX: 'auto', background: theme.palette.background.paper }}>
              <Table size="small" stickyHeader sx={{ minWidth: 800 }}>
                <TableHead>
                  <TableRow sx={{ background: theme.palette.background.paper }}>
                    {columns.map(col => <TableCell key={col} sx={{ fontWeight: 700, background: theme.palette.background.paper, color: theme.palette.primary.main, maxWidth: 180, whiteSpace: 'nowrap', textOverflow: 'ellipsis', overflow: 'hidden' }}>{col}</TableCell>)}
                  </TableRow>
                </TableHead>
                <TableBody>
                  {data.map((row, idx) => (
                    <TableRow key={idx} sx={{ background: idx % 2 === 0 ? theme.palette.background.paper : theme.palette.background.default, transition: 'background 0.2s' }}>
                      {columns.map(col => <TableCell key={col} sx={{ maxWidth: 180, whiteSpace: 'nowrap', textOverflow: 'ellipsis', overflow: 'hidden', color: theme.palette.text.primary }}>{row[col]}</TableCell>)}
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
            <Box mt={2} display="flex" justifyContent="space-between" alignItems="center">
              <Typography variant="body2" color="text.secondary">Página {page + 1}</Typography>
              <Stack direction="row" spacing={1}>
                <Button size="small" variant="outlined" onClick={() => setPage(p => Math.max(0, p - 1))} disabled={page === 0}>Anterior</Button>
                <Button size="small" variant="outlined" onClick={() => setPage(p => p + 1)} disabled={data.length < pageSize}>Próxima</Button>
              </Stack>
            </Box>
          </>
        )}
      </Paper>
    </Box>
  );
};

export default VisualizarTabelas; 