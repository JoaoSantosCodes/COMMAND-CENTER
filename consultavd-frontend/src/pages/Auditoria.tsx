import React, { useState, useEffect } from 'react';
import { Box, Typography, Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Stack, TextField, Button, MenuItem, CircularProgress, Alert, Chip, Dialog, DialogTitle, DialogContent, DialogActions, IconButton, Tooltip, useTheme } from '@mui/material';
import FileDownloadIcon from '@mui/icons-material/FileDownload';
import VisibilityIcon from '@mui/icons-material/Visibility';
import CloseIcon from '@mui/icons-material/Close';
import dayjs from 'dayjs';
import apiService from '../services/api';

const unique = (arr: string[]) => Array.from(new Set(arr));

const Auditoria: React.FC = () => {
  const theme = useTheme();
  const [logs, setLogs] = useState<any[]>([]);
  const [filters, setFilters] = useState({ user: '', action: '', table: '', search: '', dateFrom: '', dateTo: '' });
  const [page, setPage] = useState(0);
  const pageSize = 10;
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [selected, setSelected] = useState<any | null>(null);
  const [total, setTotal] = useState(0);

  // Buscar logs reais do backend
  useEffect(() => {
    setLoading(true);
    setError(null);
    apiService.getAuditLogs(page + 1, pageSize)
      .then(resp => {
        // Mapear campos do backend para o formato esperado
        const mapped = (resp.data || []).map((log: any, idx: number) => ({
          id: idx + 1 + page * pageSize,
          datetime: log.timestamp,
          user: log.user,
          action: log.action,
          table: log.table,
          row_id: log.record_id,
          summary: log.action + ' em ' + log.table,
          details: {
            before: log.old_value || {},
            after: log.new_value || {},
            changed: log.old_value && log.new_value ? Object.keys(log.new_value).filter(k => (log.old_value?.[k] !== log.new_value?.[k])) : Object.keys(log.new_value || {})
          }
        }));
        setLogs(mapped);
        setTotal(resp.pagination?.total || 0);
      })
      .catch(e => setError('Erro ao buscar logs de auditoria.'))
      .finally(() => setLoading(false));
  }, [page]);

  // Filtros (aplicados no frontend)
  const filtered = logs.filter(log =>
    (!filters.user || log.user === filters.user) &&
    (!filters.action || log.action === filters.action) &&
    (!filters.table || log.table === filters.table) &&
    (!filters.search || log.summary.toLowerCase().includes(filters.search.toLowerCase())) &&
    (!filters.dateFrom || log.datetime >= filters.dateFrom) &&
    (!filters.dateTo || log.datetime <= filters.dateTo)
  );

  // Exportação CSV
  const handleExport = () => {
    const cols = ['Data/Hora', 'Usuário', 'Ação', 'Tabela', 'ID', 'Resumo'];
    const csv = [cols.join(',')].concat(
      filtered.map(l => [l.datetime, l.user, l.action, l.table, l.row_id, l.summary].join(','))
    ).join('\n');
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'auditoria.csv';
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <Box p={3} sx={{ maxWidth: 1200, margin: '0 auto' }}>
      <Typography variant="h4" gutterBottom>Auditoria</Typography>
      <Paper sx={{ p: 3, mb: 2, background: theme.palette.background.paper }}>
        <Stack direction={{ xs: 'column', sm: 'row' }} spacing={2} mb={2} alignItems="center">
          <TextField label="Usuário" select size="small" value={filters.user} onChange={e => setFilters(f => ({ ...f, user: e.target.value }))} sx={{ minWidth: 120 }}>
            <MenuItem value="">Todos</MenuItem>
            {unique(logs.map(l => l.user)).map(u => <MenuItem key={u} value={u}>{u}</MenuItem>)}
          </TextField>
          <TextField label="Ação" select size="small" value={filters.action} onChange={e => setFilters(f => ({ ...f, action: e.target.value }))} sx={{ minWidth: 120 }}>
            <MenuItem value="">Todas</MenuItem>
            {unique(logs.map(l => l.action)).map(a => <MenuItem key={a} value={a}>{a}</MenuItem>)}
          </TextField>
          <TextField label="Tabela" select size="small" value={filters.table} onChange={e => setFilters(f => ({ ...f, table: e.target.value }))} sx={{ minWidth: 160 }}>
            <MenuItem value="">Todas</MenuItem>
            {unique(logs.map(l => l.table)).map(t => <MenuItem key={t} value={t}>{t}</MenuItem>)}
          </TextField>
          <TextField label="Buscar resumo" size="small" value={filters.search} onChange={e => setFilters(f => ({ ...f, search: e.target.value }))} sx={{ minWidth: 180 }} />
          <TextField label="De" type="date" size="small" value={filters.dateFrom} onChange={e => setFilters(f => ({ ...f, dateFrom: e.target.value }))} InputLabelProps={{ shrink: true }} />
          <TextField label="Até" type="date" size="small" value={filters.dateTo} onChange={e => setFilters(f => ({ ...f, dateTo: e.target.value }))} InputLabelProps={{ shrink: true }} />
          <Button variant="outlined" color="success" startIcon={<FileDownloadIcon />} onClick={handleExport}>
            Exportar CSV
          </Button>
        </Stack>
        {loading && <Box display="flex" justifyContent="center" alignItems="center" minHeight={120}><CircularProgress size={40} /></Box>}
        {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
        <TableContainer sx={{ maxHeight: 420, borderRadius: 2, boxShadow: 1, overflowX: 'auto', background: theme.palette.background.paper }}>
          <Table size="small" stickyHeader sx={{ minWidth: 900 }}>
            <TableHead>
              <TableRow>
                <TableCell>Data/Hora</TableCell>
                <TableCell>Usuário</TableCell>
                <TableCell>Ação</TableCell>
                <TableCell>Tabela</TableCell>
                <TableCell>ID</TableCell>
                <TableCell>Resumo</TableCell>
                <TableCell>Detalhes</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {filtered.slice(page * pageSize, (page + 1) * pageSize).map(log => (
                <TableRow key={log.id}>
                  <TableCell>{log.datetime}</TableCell>
                  <TableCell>{log.user}</TableCell>
                  <TableCell><Chip label={log.action} size="small" color={log.action === 'DELETE' ? 'error' : log.action === 'UPDATE' ? 'warning' : 'success'} /></TableCell>
                  <TableCell>{log.table}</TableCell>
                  <TableCell>{log.row_id}</TableCell>
                  <TableCell>{log.summary}</TableCell>
                  <TableCell>
                    <Tooltip title="Ver detalhes">
                      <IconButton size="small" onClick={() => setSelected(log)}><VisibilityIcon /></IconButton>
                    </Tooltip>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
        <Box mt={2} display="flex" justifyContent="space-between" alignItems="center">
          <Typography variant="body2" color="text.secondary">Página {page + 1} de {Math.max(1, Math.ceil(total / pageSize))}</Typography>
          <Stack direction="row" spacing={1}>
            <Button size="small" variant="outlined" onClick={() => setPage(p => Math.max(0, p - 1))} disabled={page === 0}>Anterior</Button>
            <Button size="small" variant="outlined" onClick={() => setPage(p => p + 1)} disabled={(page + 1) * pageSize >= filtered.length}>Próxima</Button>
          </Stack>
        </Box>
      </Paper>
      <Dialog open={!!selected} onClose={() => setSelected(null)} maxWidth="sm" fullWidth>
        <DialogTitle>
          Detalhes da Auditoria
          <IconButton onClick={() => setSelected(null)} sx={{ position: 'absolute', right: 8, top: 8 }}>
            <CloseIcon />
          </IconButton>
        </DialogTitle>
        <DialogContent dividers>
          {selected && (
            <>
              <Typography variant="subtitle2" gutterBottom>Data/Hora: {selected.datetime}</Typography>
              <Typography variant="subtitle2" gutterBottom>Usuário: {selected.user}</Typography>
              <Typography variant="subtitle2" gutterBottom>Ação: <Chip label={selected.action} size="small" color={selected.action === 'DELETE' ? 'error' : selected.action === 'UPDATE' ? 'warning' : 'success'} /></Typography>
              <Typography variant="subtitle2" gutterBottom>Tabela: {selected.table}</Typography>
              <Typography variant="subtitle2" gutterBottom>ID: {selected.row_id}</Typography>
              <Box mt={2}>
                <Typography variant="subtitle1" fontWeight={600}>Campos alterados:</Typography>
                <Stack direction="row" spacing={1} flexWrap="wrap" mb={2}>
                  {selected.details.changed.map((f: string) => <Chip key={f} label={f} size="small" color="primary" />)}
                </Stack>
                <Box display="flex" gap={4}>
                  <Box>
                    <Typography variant="body2" fontWeight={600}>Antes</Typography>
                    <Paper variant="outlined" sx={{ p: 1, minWidth: 120, background: theme.palette.mode === 'dark' ? '#222' : '#f7f7f7' }}>
                      <Typography variant="body2">
                        {Object.entries(selected.details.before || {}).length > 0
                          ? Object.entries(selected.details.before).map(([k, v]) => `${k}: ${v}`).join(' | ')
                          : 'Nenhuma alteração'}
                      </Typography>
                    </Paper>
                  </Box>
                  <Box>
                    <Typography variant="body2" fontWeight={600}>Depois</Typography>
                    <Paper variant="outlined" sx={{ p: 1, minWidth: 120, background: theme.palette.mode === 'dark' ? '#222' : '#f7f7f7' }}>
                      <Typography variant="body2">
                        {Object.entries(selected.details.after || {}).length > 0
                          ? Object.entries(selected.details.after).map(([k, v]) => `${k}: ${v}`).join(' | ')
                          : 'Nenhuma alteração'}
                      </Typography>
                    </Paper>
                  </Box>
                </Box>
              </Box>
            </>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setSelected(null)}>Fechar</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Auditoria; 