import React, { useState } from 'react';
import { Box, Typography, Paper, Button, TextField, CircularProgress, Snackbar, Alert, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, IconButton, Tooltip, Chip, Autocomplete, Stack, Fade, useTheme } from '@mui/material';
import PlayArrowIcon from '@mui/icons-material/PlayArrow';
import ClearIcon from '@mui/icons-material/Clear';
import FileDownloadIcon from '@mui/icons-material/FileDownload';
import HistoryIcon from '@mui/icons-material/History';
import DeleteSweepIcon from '@mui/icons-material/DeleteSweep';
import apiService from '../services/api';

const sqlCommands = [
  { label: "Listar todas as lojas", query: "SELECT * FROM lojas_lojas;" },
  { label: "Listar todos os inventários", query: "SELECT * FROM inventario_planilha1;" },
  { label: "Listar todos os registros de lojas_ggl_gr", query: "SELECT * FROM lojas_ggl_gr;" },
  { label: "Contar lojas por status", query: "SELECT status, COUNT(*) as total FROM lojas_lojas GROUP BY status;" },
  { label: "Buscar lojas ativas", query: "SELECT * FROM lojas_lojas WHERE status = 'ATIVA';" },
  { label: "Buscar inventário de uma loja (id=1)", query: "SELECT * FROM inventario_planilha1 WHERE loja_id = 1;" },
];

const mockHistory = sqlCommands.map(c => c.query);

const ConsultaSQL: React.FC = () => {
  const [sql, setSql] = useState(sqlCommands[0].query);
  const [result, setResult] = useState<any[] | null>(null);
  const [columns, setColumns] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [snackbar, setSnackbar] = useState<{ open: boolean; message: string; severity: 'success' | 'error' }>({ open: false, message: '', severity: 'success' });
  const [history, setHistory] = useState<string[]>(mockHistory);
  const [showHistory, setShowHistory] = useState(false);
  const [showAllCols, setShowAllCols] = useState(false);
  const theme = useTheme();

  const validateSQL = (query: string) => /^\s*select\b/i.test(query);

  const handleExecute = async () => {
    setError(null);
    setResult(null);
    setColumns([]);
    if (!validateSQL(sql)) {
      setError('Por segurança, apenas comandos SELECT são permitidos.');
      return;
    }
    setLoading(true);
    try {
      const response = await apiService.executeSQL(sql);
      setResult(response.data);
      setColumns(response.columns);
      setHistory([sql, ...history.filter(q => q !== sql)].slice(0, 10));
      setSnackbar({ open: true, message: 'Consulta executada com sucesso!', severity: 'success' });
      setLoading(false);
    } catch (e: any) {
      setError(e?.response?.data?.detail || 'Erro ao executar a consulta.');
      setSnackbar({ open: true, message: 'Erro ao executar a consulta.', severity: 'error' });
      setLoading(false);
    }
  };

  const handleClear = () => {
    setSql('');
    setResult(null);
    setColumns([]);
    setError(null);
  };

  const handleExport = () => {
    if (!result || columns.length === 0) return;
    const csv = [columns.join(',')].concat(result.map(row => columns.map(col => row[col]).join(','))).join('\n');
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'resultado_sql.csv';
    a.click();
    URL.revokeObjectURL(url);
  };

  const handleHistoryClear = () => setHistory([]);

  return (
    <Box p={3} sx={{ maxWidth: 1000, margin: '0 auto' }}>
      <Typography variant="h4" gutterBottom>Consulta SQL Customizada</Typography>
      <Paper sx={{ p: 3, mb: 2, background: theme.palette.background.paper }}>
        <Box display="flex" alignItems="center" justifyContent="space-between" mb={2}>
          <Typography variant="h6">Editor SQL</Typography>
          <Tooltip title="Ver histórico de comandos"><IconButton onClick={() => setShowHistory(v => !v)}><HistoryIcon /></IconButton></Tooltip>
        </Box>
        <Box mb={2} display="flex" alignItems="center" gap={2}>
          <Autocomplete
            options={sqlCommands}
            getOptionLabel={option => option.label}
            sx={{ minWidth: 320 }}
            renderInput={params => <TextField {...params} label="Comandos Prontos" size="small" />}
            onChange={(_e, value) => value && setSql(value.query)}
            isOptionEqualToValue={(option, value) => option.query === value.query}
          />
        </Box>
        <TextField
          label="Digite sua consulta SQL (apenas SELECT)"
          multiline
          minRows={4}
          maxRows={12}
          fullWidth
          value={sql}
          onChange={e => setSql(e.target.value)}
          variant="outlined"
          sx={{ mb: 2, fontFamily: 'monospace', background: theme.palette.background.default, borderRadius: 2, color: theme.palette.text.primary }}
          InputProps={{ style: { fontFamily: 'monospace', color: theme.palette.text.primary } }}
        />
        <Stack direction="row" spacing={2} mb={2}>
          <Tooltip title="Executar consulta">
            <span>
              <Button variant="contained" color="primary" startIcon={<PlayArrowIcon />} onClick={handleExecute} disabled={loading || !sql.trim()} sx={{ minWidth: 120 }}>
                {loading ? <CircularProgress size={22} color="inherit" /> : 'Executar'}
              </Button>
            </span>
          </Tooltip>
          <Tooltip title="Limpar editor e resultado">
            <span>
              <Button variant="outlined" color="secondary" startIcon={<ClearIcon />} onClick={handleClear} disabled={loading} sx={{ minWidth: 120 }}>
                Limpar
              </Button>
            </span>
          </Tooltip>
          <Tooltip title="Exportar resultado para CSV">
            <span>
              <Button variant="outlined" color="success" startIcon={<FileDownloadIcon />} onClick={handleExport} disabled={!result || !columns.length} sx={{ minWidth: 180 }}>
                Exportar Resultado
              </Button>
            </span>
          </Tooltip>
        </Stack>
        {error && <Fade in={!!error}><Alert severity="error" sx={{ mb: 2 }}>{error}</Alert></Fade>}
        {result && columns.length > 0 && !loading && (
          <Fade in={true}>
            <Box>
              <Box display="flex" alignItems="center" gap={1} mb={1} sx={{ overflowX: 'auto', pb: 1, maxWidth: '100%' }}>
                <Typography variant="body2" color="text.secondary" sx={{ flexShrink: 0 }}>Colunas:</Typography>
                <Box display="flex" gap={1} sx={{ flexWrap: 'wrap', maxWidth: 'calc(100vw - 350px)' }}>
                  {(showAllCols ? columns : columns.slice(0, 8)).map(col => (
                    <Tooltip key={col} title={col} arrow>
                      <Chip label={col} size="small" sx={{ fontWeight: 600, maxWidth: 260, mb: 1, textOverflow: 'ellipsis', overflow: 'hidden' }} />
                    </Tooltip>
                  ))}
                  {columns.length > 8 && !showAllCols && (
                    <Chip
                      label={`+${columns.length - 8} mais`}
                      size="small"
                      color="info"
                      sx={{ mb: 1, cursor: 'pointer', fontWeight: 600 }}
                      onClick={() => setShowAllCols(true)}
                    />
                  )}
                  {columns.length > 8 && showAllCols && (
                    <Chip
                      label="Ocultar"
                      size="small"
                      color="default"
                      sx={{ mb: 1, cursor: 'pointer', fontWeight: 600 }}
                      onClick={() => setShowAllCols(false)}
                    />
                  )}
                </Box>
                <Box flex={1} />
                <Chip label={`${result.length} resultado${result.length !== 1 ? 's' : ''}`} color="info" size="small" sx={{ flexShrink: 0 }} />
              </Box>
              <TableContainer sx={{ maxHeight: 400, borderRadius: 2, boxShadow: 1, overflowX: 'auto', background: theme.palette.background.paper }}>
                <Table size="small" stickyHeader sx={{ minWidth: 800 }}>
                  <TableHead>
                    <TableRow sx={{ background: theme.palette.background.paper }}>
                      {columns.map(col => <TableCell key={col} sx={{ fontWeight: 700, background: theme.palette.background.paper, color: theme.palette.primary.main, maxWidth: 180, whiteSpace: 'nowrap', textOverflow: 'ellipsis', overflow: 'hidden' }}>{col}</TableCell>)}
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {result.map((row, idx) => (
                      <TableRow key={idx} sx={{ background: idx % 2 === 0 ? theme.palette.background.paper : theme.palette.background.default, transition: 'background 0.2s' }}>
                        {columns.map(col => <TableCell key={col} sx={{ maxWidth: 180, whiteSpace: 'nowrap', textOverflow: 'ellipsis', overflow: 'hidden', color: theme.palette.text.primary }}>{row[col]}</TableCell>)}
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </Box>
          </Fade>
        )}
      </Paper>
      <Fade in={showHistory} unmountOnExit>
        <Paper sx={{ p: 2, mb: 2, background: theme.palette.background.paper }}>
          <Box display="flex" alignItems="center" justifyContent="space-between" mb={1}>
            <Typography variant="h6" gutterBottom>Histórico de Consultas</Typography>
            <Tooltip title="Limpar histórico"><IconButton onClick={handleHistoryClear}><DeleteSweepIcon /></IconButton></Tooltip>
          </Box>
          {history.length === 0 ? <Typography color="text.secondary">Nenhuma consulta recente.</Typography> : (
            <Box display="flex" flexWrap="wrap" gap={1}>
              {history.map((q, idx) => (
                <Chip key={idx} label={q} onClick={() => setSql(q)} sx={{ cursor: 'pointer', mb: 1, bgcolor: theme.palette.background.default, color: theme.palette.text.primary, fontWeight: 600 }} />
              ))}
            </Box>
          )}
        </Paper>
      </Fade>
      <Snackbar
        open={snackbar.open}
        autoHideDuration={2500}
        onClose={() => setSnackbar({ ...snackbar, open: false })}
        anchorOrigin={{ vertical: 'top', horizontal: 'center' }}
        TransitionComponent={Fade}
      >
        <Alert severity={snackbar.severity} variant="filled" sx={{ width: '100%' }}>
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Box>
  );
};

export default ConsultaSQL; 