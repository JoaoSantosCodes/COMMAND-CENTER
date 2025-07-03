import React, { useEffect, useState } from 'react';
import { Box, Typography, Paper, Button, CircularProgress, Grid, Snackbar, Alert, IconButton, Tooltip, Switch, Dialog, DialogTitle, DialogContent, DialogActions, TextField, Divider, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Chip, useTheme } from '@mui/material';
import RefreshIcon from '@mui/icons-material/Refresh';
import DeleteSweepIcon from '@mui/icons-material/DeleteSweep';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import ErrorIcon from '@mui/icons-material/Error';
import InfoOutlinedIcon from '@mui/icons-material/InfoOutlined';
import FileDownloadIcon from '@mui/icons-material/FileDownload';
import apiService from '../services/api';

// Mock para histórico de operações (substituir por API futuramente)
const mockHistory = [
  { action: 'Limpar Cache', user: 'admin', date: new Date().toLocaleString() },
  { action: 'Ativar Cache', user: 'admin', date: new Date().toLocaleString() },
];

const metricInfo = {
  enabled: 'Indica se o cache está ativo. Quando desativado, o sistema ignora o cache.',
  current_size: 'Quantidade de itens atualmente armazenados no cache.',
  max_size: 'Limite máximo de itens que o cache pode armazenar.',
  hits: 'Número de vezes que o sistema encontrou o dado no cache (acesso rápido).',
  misses: 'Número de vezes que o sistema não encontrou o dado no cache.',
  sets: 'Número de vezes que um valor foi salvo no cache.',
  evictions: 'Itens removidos do cache para abrir espaço para novos.',
  hit_rate: 'Percentual de buscas atendidas pelo cache.',
  created_at: 'Data/hora em que o cache foi inicializado.',
};

const GerenciamentoCache: React.FC = () => {
  const theme = useTheme();
  const [stats, setStats] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [clearing, setClearing] = useState(false);
  const [snackbar, setSnackbar] = useState<{ open: boolean; message: string; severity: 'success' | 'error' }>({ open: false, message: '', severity: 'success' });
  const [confirmOpen, setConfirmOpen] = useState(false);
  const [config, setConfig] = useState({ max_size: '', default_ttl: '' });
  const [configEdit, setConfigEdit] = useState(false);
  const [history, setHistory] = useState(mockHistory);
  // Mock para itens do cache (substituir por API futuramente)
  const [cacheItems, setCacheItems] = useState<any[]>([]);

  const fetchStats = async () => {
    setLoading(true);
    try {
      const data = await apiService.getCacheStats();
      setStats(data);
      setConfig({
        max_size: data.max_size?.toString() || '',
        default_ttl: data.default_ttl?.toString() || '',
      });
    } catch (e) {
      setStats(null);
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchStats();
    // Mock: carregar itens do cache (futuramente via API)
    setCacheItems([
      { key: 'exemplo1', value: 'valor1', expires_at: '2025-07-02 01:00:00' },
      { key: 'exemplo2', value: 'valor2', expires_at: '2025-07-02 01:05:00' },
    ]);
  }, []);

  const handleClearCache = async () => {
    setClearing(true);
    try {
      await apiService.clearCache();
      setSnackbar({ open: true, message: 'Cache limpo com sucesso!', severity: 'success' });
      setHistory([{ action: 'Limpar Cache', user: 'admin', date: new Date().toLocaleString() }, ...history]);
      fetchStats();
    } catch (e) {
      setSnackbar({ open: true, message: 'Erro ao limpar o cache.', severity: 'error' });
    }
    setClearing(false);
    setConfirmOpen(false);
  };

  const handleExport = () => {
    if (!stats) return;
    const csv = [
      'Métrica,Valor',
      `Habilitado,${stats.enabled}`,
      `Tamanho Atual,${stats.current_size}`,
      `Tamanho Máximo,${stats.max_size}`,
      `Hits,${stats.hits}`,
      `Misses,${stats.misses}`,
      `Sets,${stats.sets}`,
      `Evictions,${stats.evictions}`,
      `Taxa de Acerto,${(stats.hit_rate * 100).toFixed(1)}%`,
      `Criado em,${new Date(stats.created_at).toLocaleString()}`,
    ].join('\n');
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'cache_stats.csv';
    a.click();
    URL.revokeObjectURL(url);
  };

  const handleToggleCache = () => {
    // Mock: alternar status (futuramente via API)
    setStats((prev: any) => ({ ...prev, enabled: !prev.enabled }));
    setHistory([{ action: stats?.enabled ? 'Desativar Cache' : 'Ativar Cache', user: 'admin', date: new Date().toLocaleString() }, ...history]);
  };

  const handleConfigEdit = () => setConfigEdit(true);
  const handleConfigSave = () => {
    // Mock: salvar configs (futuramente via API)
    setStats((prev: any) => ({ ...prev, max_size: Number(config.max_size), default_ttl: Number(config.default_ttl) }));
    setConfigEdit(false);
    setSnackbar({ open: true, message: 'Configurações salvas (mock).', severity: 'success' });
  };

  return (
    <Box p={3} sx={{ maxWidth: 900, margin: '0 auto' }}>
      <Typography variant="h4" gutterBottom>Gerenciamento de Cache</Typography>
      <Paper sx={{ p: 3, mb: 2, background: theme.palette.background.paper }}>
        <Box display="flex" alignItems="center" justifyContent="space-between" mb={2}>
          <Typography variant="h6">Status do Cache</Typography>
          <Box>
            <Tooltip title="Exportar estatísticas (CSV)"><IconButton onClick={handleExport}><FileDownloadIcon /></IconButton></Tooltip>
            <Tooltip title="Atualizar status"><IconButton onClick={fetchStats} disabled={loading}><RefreshIcon /></IconButton></Tooltip>
          </Box>
        </Box>
        {loading ? <Box display="flex" justifyContent="center" alignItems="center" minHeight={120}><CircularProgress size={40} /></Box> : stats ? (
          <Grid container spacing={2}>
            <Grid item xs={12} sm={6} md={4}>
              <Paper sx={{ p: 2, bgcolor: stats.enabled ? '#1e4620' : '#5a1a1a', color: '#fff' }}>
                <Box display="flex" alignItems="center" gap={1}>
                  {stats.enabled ? <CheckCircleIcon color="success" /> : <ErrorIcon color="error" />}
                  <Typography fontWeight={600}>Habilitado</Typography>
                  <Tooltip title={metricInfo.enabled}><InfoOutlinedIcon fontSize="small" /></Tooltip>
                </Box>
                <Box mt={1}>
                  <Switch checked={stats.enabled} onChange={handleToggleCache} color="success" />
                  <Typography variant="body2">{stats.enabled ? 'Ativo' : 'Desativado'}</Typography>
                </Box>
              </Paper>
            </Grid>
            <Grid item xs={12} sm={6} md={4}>
              <Paper sx={{ p: 2, bgcolor: theme.palette.background.default, color: theme.palette.text.primary }}>
                <Box display="flex" alignItems="center" gap={1}>
                  <Typography fontWeight={600}>Tamanho Atual</Typography>
                  <Tooltip title={metricInfo.current_size}><InfoOutlinedIcon fontSize="small" /></Tooltip>
                </Box>
                <Typography variant="h5">{stats.current_size} / {stats.max_size}</Typography>
              </Paper>
            </Grid>
            <Grid item xs={12} sm={6} md={4}>
              <Paper sx={{ p: 2, bgcolor: theme.palette.background.default, color: theme.palette.text.primary }}>
                <Box display="flex" alignItems="center" gap={1}>
                  <Typography fontWeight={600}>Taxa de Acerto</Typography>
                  <Tooltip title={metricInfo.hit_rate}><InfoOutlinedIcon fontSize="small" /></Tooltip>
                </Box>
                <Typography variant="h5">{(stats.hit_rate * 100).toFixed(1)}%</Typography>
              </Paper>
            </Grid>
            <Grid item xs={12} sm={6} md={4}>
              <Paper sx={{ p: 2, bgcolor: theme.palette.background.default, color: theme.palette.text.primary }}>
                <Box display="flex" alignItems="center" gap={1}>
                  <Typography fontWeight={600}>Hits</Typography>
                  <Tooltip title={metricInfo.hits}><InfoOutlinedIcon fontSize="small" /></Tooltip>
                </Box>
                <Chip label={stats.hits} color="success" />
              </Paper>
            </Grid>
            <Grid item xs={12} sm={6} md={4}>
              <Paper sx={{ p: 2, bgcolor: theme.palette.background.default, color: theme.palette.text.primary }}>
                <Box display="flex" alignItems="center" gap={1}>
                  <Typography fontWeight={600}>Misses</Typography>
                  <Tooltip title={metricInfo.misses}><InfoOutlinedIcon fontSize="small" /></Tooltip>
                </Box>
                <Chip label={stats.misses} color="warning" />
              </Paper>
            </Grid>
            <Grid item xs={12} sm={6} md={4}>
              <Paper sx={{ p: 2, bgcolor: theme.palette.background.default, color: theme.palette.text.primary }}>
                <Box display="flex" alignItems="center" gap={1}>
                  <Typography fontWeight={600}>Sets</Typography>
                  <Tooltip title={metricInfo.sets}><InfoOutlinedIcon fontSize="small" /></Tooltip>
                </Box>
                <Chip label={stats.sets} color="info" />
              </Paper>
            </Grid>
            <Grid item xs={12} sm={6} md={4}>
              <Paper sx={{ p: 2, bgcolor: theme.palette.background.default, color: theme.palette.text.primary }}>
                <Box display="flex" alignItems="center" gap={1}>
                  <Typography fontWeight={600}>Evictions</Typography>
                  <Tooltip title={metricInfo.evictions}><InfoOutlinedIcon fontSize="small" /></Tooltip>
                </Box>
                <Chip label={stats.evictions} color="secondary" />
              </Paper>
            </Grid>
            <Grid item xs={12} sm={6} md={4}>
              <Paper sx={{ p: 2, bgcolor: theme.palette.background.default, color: theme.palette.text.primary }}>
                <Box display="flex" alignItems="center" gap={1}>
                  <Typography fontWeight={600}>Criado em</Typography>
                  <Tooltip title={metricInfo.created_at}><InfoOutlinedIcon fontSize="small" /></Tooltip>
                </Box>
                <Typography variant="body2">{new Date(stats.created_at).toLocaleString()}</Typography>
              </Paper>
            </Grid>
            <Grid item xs={12} sm={6} md={4}>
              <Paper sx={{ p: 2, bgcolor: theme.palette.background.default, color: theme.palette.text.primary }}>
                <Box display="flex" alignItems="center" gap={1}>
                  <Typography fontWeight={600}>Configurações</Typography>
                  <Tooltip title="Configurações rápidas do cache"><InfoOutlinedIcon fontSize="small" /></Tooltip>
                </Box>
                {configEdit ? (
                  <>
                    <TextField
                      label="Tamanho Máximo"
                      size="small"
                      value={config.max_size}
                      onChange={e => setConfig({ ...config, max_size: e.target.value })}
                      sx={{ my: 1 }}
                    />
                    <TextField
                      label="TTL Padrão (s)"
                      size="small"
                      value={config.default_ttl}
                      onChange={e => setConfig({ ...config, default_ttl: e.target.value })}
                      sx={{ my: 1 }}
                    />
                    <Button size="small" variant="contained" color="success" onClick={handleConfigSave}>Salvar</Button>
                  </>
                ) : (
                  <>
                    <Typography variant="body2">Tamanho Máximo: {stats.max_size}</Typography>
                    <Typography variant="body2">TTL Padrão: {stats.default_ttl || 300}s</Typography>
                    <Button size="small" variant="outlined" sx={{ mt: 1 }} onClick={handleConfigEdit}>Editar</Button>
                  </>
                )}
              </Paper>
            </Grid>
          </Grid>
        ) : (
          <Typography color="error">Não foi possível obter o status do cache.</Typography>
        )}
        <Box mt={3} display="flex" justifyContent="flex-end">
          <Button
            variant="contained"
            color="error"
            startIcon={<DeleteSweepIcon />}
            onClick={() => setConfirmOpen(true)}
            disabled={clearing}
          >
            Limpar Cache
          </Button>
        </Box>
      </Paper>
      {/* Modal de confirmação */}
      <Dialog open={confirmOpen} onClose={() => setConfirmOpen(false)}>
        <DialogTitle>Confirmar limpeza do cache</DialogTitle>
        <DialogContent>Tem certeza que deseja limpar todo o cache? Esta ação não pode ser desfeita.</DialogContent>
        <DialogActions>
          <Button onClick={() => setConfirmOpen(false)}>Cancelar</Button>
          <Button onClick={handleClearCache} color="error" variant="contained" autoFocus disabled={clearing}>Limpar</Button>
        </DialogActions>
      </Dialog>
      {/* Itens do cache (mock) */}
      <Paper sx={{ p: 2, mb: 2, background: theme.palette.background.paper }}>
        <Typography variant="h6" gutterBottom>Itens do Cache <Tooltip title="Lista resumida dos itens atualmente no cache (mock)"><InfoOutlinedIcon fontSize="small" /></Tooltip></Typography>
        <TableContainer>
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell>Chave</TableCell>
                <TableCell>Valor</TableCell>
                <TableCell>Expira em</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {cacheItems.length === 0 ? (
                <TableRow><TableCell colSpan={3}>Nenhum item no cache.</TableCell></TableRow>
              ) : cacheItems.map((item, idx) => (
                <TableRow key={idx}>
                  <TableCell>{item.key}</TableCell>
                  <TableCell>{item.value}</TableCell>
                  <TableCell>{item.expires_at}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Paper>
      {/* Histórico de operações (mock) */}
      <Paper sx={{ p: 2, mb: 2, background: theme.palette.background.paper }}>
        <Typography variant="h6" gutterBottom>Histórico de Operações <Tooltip title="Ações recentes realizadas no cache"><InfoOutlinedIcon fontSize="small" /></Tooltip></Typography>
        <TableContainer>
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell>Ação</TableCell>
                <TableCell>Usuário</TableCell>
                <TableCell>Data/Hora</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {history.length === 0 ? (
                <TableRow><TableCell colSpan={3}>Nenhuma operação registrada.</TableCell></TableRow>
              ) : history.map((item, idx) => (
                <TableRow key={idx}>
                  <TableCell>{item.action}</TableCell>
                  <TableCell>{item.user}</TableCell>
                  <TableCell>{item.date}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Paper>
      <Snackbar
        open={snackbar.open}
        autoHideDuration={3000}
        onClose={() => setSnackbar({ ...snackbar, open: false })}
        anchorOrigin={{ vertical: 'top', horizontal: 'center' }}
      >
        <Alert severity={snackbar.severity} variant="filled" sx={{ width: '100%' }}>
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Box>
  );
};

export default GerenciamentoCache; 