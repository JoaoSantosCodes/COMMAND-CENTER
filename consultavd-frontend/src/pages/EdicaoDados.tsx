import React, { useState, useEffect } from 'react';
import { Button, Select, MenuItem, Snackbar, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, IconButton, TextField, CircularProgress, Box } from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import AddIcon from '@mui/icons-material/Add';
import type { SelectChangeEvent } from '@mui/material/Select';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8080';

const EdicaoDados: React.FC = () => {
  const [tables, setTables] = useState<string[]>([]);
  const [selectedTable, setSelectedTable] = useState<string>('');
  const [data, setData] = useState<any[]>([]);
  const [columns, setColumns] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [snackbar, setSnackbar] = useState<{ open: boolean; message: string; type: 'success' | 'error' }>({ open: false, message: '', type: 'success' });
  const [deletedRows, setDeletedRows] = useState<any[]>([]);
  const [primaryKey, setPrimaryKey] = useState<string>('id');
  const [page, setPage] = useState(1);
  const [rowsPerPage, setRowsPerPage] = useState(20);
  const [totalRows, setTotalRows] = useState(0);
  const [search, setSearch] = useState('');
  const [searchInput, setSearchInput] = useState('');
  const [orderBy, setOrderBy] = useState<string>('');
  const [orderDir, setOrderDir] = useState<'asc' | 'desc'>('asc');

  // Buscar tabelas ao montar
  useEffect(() => {
    const fetchTables = async () => {
      setLoading(true);
      try {
        const res = await fetch(`${API_URL}/api/tables`);
        const json = await res.json();
        if (json.success) {
          setTables(json.data);
          setSelectedTable(json.data[0] || '');
        } else {
          setSnackbar({ open: true, message: 'Erro ao buscar tabelas', type: 'error' });
        }
      } catch (e) {
        setSnackbar({ open: true, message: 'Erro de conexão ao buscar tabelas', type: 'error' });
      } finally {
        setLoading(false);
      }
    };
    fetchTables();
  }, []);

  // Buscar dados da tabela selecionada e a PK
  useEffect(() => {
    if (!selectedTable) return;
    const fetchData = async () => {
      setLoading(true);
      try {
        // Buscar PK
        const pkRes = await fetch(`${API_URL}/api/table/${selectedTable}/pk`);
        const pkJson = await pkRes.json();
        if (pkJson.success && pkJson.data.primaryKey) {
          setPrimaryKey(pkJson.data.primaryKey);
        } else {
          setPrimaryKey('id');
        }
        // Buscar dados paginados, filtrados e ordenados
        const params = new URLSearchParams({
          limit: String(rowsPerPage),
          offset: String((page-1)*rowsPerPage),
        });
        if (search) params.append('search', search);
        if (orderBy) params.append('orderBy', orderBy);
        if (orderDir) params.append('orderDir', orderDir);
        const res = await fetch(`${API_URL}/api/table/${selectedTable}?${params.toString()}`);
        const json = await res.json();
        if (json.success) {
          setColumns(json.data.columns);
          setData(json.data.rows);
          setTotalRows(json.data.total || 0);
        } else {
          setColumns([]);
          setData([]);
          setTotalRows(0);
          setSnackbar({ open: true, message: 'Erro ao buscar dados da tabela', type: 'error' });
        }
      } catch (e) {
        setColumns([]);
        setData([]);
        setTotalRows(0);
        setSnackbar({ open: true, message: 'Erro de conexão ao buscar dados', type: 'error' });
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [selectedTable, page, rowsPerPage, search, orderBy, orderDir]);

  // Atualizar página se o total de registros mudar
  useEffect(() => {
    const totalPages = Math.max(1, Math.ceil(totalRows / rowsPerPage));
    if (page > totalPages) {
      setPage(totalPages);
    }
  }, [totalRows, rowsPerPage]);

  // Campo de busca com debounce
  useEffect(() => {
    const timeout = setTimeout(() => {
      setPage(1);
      setSearch(searchInput);
    }, 500);
    return () => clearTimeout(timeout);
  }, [searchInput]);

  // Troca de tabela
  const handleTableChange = (event: SelectChangeEvent<string>) => {
    setSelectedTable(event.target.value as string);
    setPage(1);
  };

  // Editar célula
  const handleCellChange = (rowIdx: number, col: string, value: any) => {
    const newData = [...data];
    newData[rowIdx] = { ...newData[rowIdx], [col]: value };
    setData(newData);
  };

  // Adicionar linha
  const handleAddRow = () => {
    const emptyRow: any = {};
    columns.forEach((col) => (emptyRow[col] = ''));
    setData([...data, emptyRow]);
  };

  // Remover linha (marca para remoção se já existe no banco)
  const handleRemoveRow = (idx: number) => {
    const row = data[idx];
    if (row && row[primaryKey]) {
      setDeletedRows([...deletedRows, row]);
    }
    const newData = data.filter((_, i) => i !== idx);
    setData(newData);
  };

  // Salvar alterações reais
  const handleSave = async () => {
    if (!selectedTable) return;
    setLoading(true);
    try {
      // Detectar novos (sem PK), editados (com PK) e deletados
      const toInsert = data.filter((row) => !row[primaryKey]);
      const toUpdate = data.filter((row) => row[primaryKey]);
      // Inserir novos
      for (const row of toInsert) {
        await fetch(`${API_URL}/api/table/${selectedTable}`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(row),
        });
      }
      // Atualizar existentes
      for (const row of toUpdate) {
        await fetch(`${API_URL}/api/table/${selectedTable}/${row[primaryKey]}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(row),
        });
      }
      // Remover deletados
      for (const row of deletedRows) {
        await fetch(`${API_URL}/api/table/${selectedTable}/${row[primaryKey]}`, {
          method: 'DELETE' });
      }
      setSnackbar({ open: true, message: 'Alterações salvas!', type: 'success' });
      setDeletedRows([]);
      // Recarregar dados
      // Buscar o novo total e ajustar página se necessário
      const res = await fetch(`${API_URL}/api/table/${selectedTable}?limit=${rowsPerPage}&offset=${(page-1)*rowsPerPage}`);
      const json = await res.json();
      if (json.success) {
        setColumns(json.data.columns);
        setData(json.data.rows);
        setTotalRows(json.data.total || 0);
        // Se a página ficou vazia e não é a primeira, volta uma página
        if (json.data.rows.length === 0 && page > 1) {
          setPage(page - 1);
        }
      }
    } catch (e) {
      setSnackbar({ open: true, message: 'Erro ao salvar alterações', type: 'error' });
    } finally {
      setLoading(false);
    }
  };

  // Ao mudar o número de registros por página, manter o primeiro registro visível
  const handleRowsPerPageChange = (e: any) => {
    const newRowsPerPage = Number(e.target.value);
    const firstItemIndex = (page - 1) * rowsPerPage + 1;
    const newPage = Math.ceil(firstItemIndex / newRowsPerPage);
    setRowsPerPage(newRowsPerPage);
    setPage(newPage);
  };

  // Ordenação ao clicar no cabeçalho
  const handleSort = (col: string) => {
    if (orderBy === col) {
      setOrderDir(orderDir === 'asc' ? 'desc' : 'asc');
    } else {
      setOrderBy(col);
      setOrderDir('asc');
    }
    setPage(1);
  };

  return (
    <div style={{ padding: 24 }}>
      <h2>Edição de Dados</h2>
      <div style={{ marginBottom: 16, display: 'flex', alignItems: 'center', gap: 16 }}>
        <Select value={selectedTable} onChange={handleTableChange} disabled={loading || tables.length === 0}>
          {tables.map((table) => (
            <MenuItem key={table} value={table}>{table}</MenuItem>
          ))}
        </Select>
        <Button variant="contained" color="primary" style={{ marginLeft: 16 }} onClick={handleAddRow} disabled={!selectedTable || loading} startIcon={<AddIcon />}>Adicionar</Button>
        <Button variant="contained" color="success" style={{ marginLeft: 8 }} onClick={handleSave} disabled={!selectedTable || loading}>Salvar</Button>
        <TextField
          label="Buscar"
          value={searchInput}
          onChange={e => setSearchInput(e.target.value)}
          size="small"
          style={{ marginLeft: 24, minWidth: 200 }}
          disabled={loading}
        />
      </div>
      <div style={{ marginBottom: 8, display: 'flex', alignItems: 'center', gap: 16 }}>
        <span>Página: {page} / {Math.max(1, Math.ceil(totalRows/rowsPerPage))}</span>
        <Button onClick={() => setPage((p) => Math.max(1, p-1))} disabled={page === 1}>Anterior</Button>
        <Button onClick={() => setPage((p) => p < Math.ceil(totalRows/rowsPerPage) ? p+1 : p)} disabled={page >= Math.ceil(totalRows/rowsPerPage)}>Próxima</Button>
        <span>Total de registros: {totalRows}</span>
        <span style={{marginLeft: 16}}>Registros por página:</span>
        <Select value={rowsPerPage} onChange={handleRowsPerPageChange} style={{width: 80}}>
          {[10, 20, 50, 100].map(n => <MenuItem key={n} value={n}>{n}</MenuItem>)}
        </Select>
      </div>
      {loading ? (
        <Box display="flex" justifyContent="center" alignItems="center" minHeight={200}>
          <CircularProgress />
        </Box>
      ) : (
        data.length === 0 ? (
          <Box display="flex" justifyContent="center" alignItems="center" minHeight={100}>
            Nenhum registro nesta página.
          </Box>
        ) : (
          <TableContainer component={Paper}>
            <Table size="small">
              <TableHead>
                <TableRow>
                  {columns.map((col) => (
                    <TableCell key={col} onClick={() => handleSort(col)} style={{ cursor: 'pointer', userSelect: 'none' }}>
                      {col}
                      {orderBy === col && (
                        orderDir === 'asc' ? ' ▲' : ' ▼'
                      )}
                    </TableCell>
                  ))}
                  <TableCell>Ações</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {data.map((row, rowIdx) => (
                  <TableRow key={rowIdx}>
                    {columns.map((col) => (
                      <TableCell key={col}>
                        <TextField
                          value={row[col] ?? ''}
                          onChange={(e) => handleCellChange(rowIdx, col, e.target.value)}
                          size="small"
                          variant="standard"
                        />
                      </TableCell>
                    ))}
                    <TableCell>
                      <IconButton color="error" onClick={() => handleRemoveRow(rowIdx)}><DeleteIcon /></IconButton>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        )
      )}
      <Snackbar
        open={snackbar.open}
        autoHideDuration={2000}
        onClose={() => setSnackbar({ ...snackbar, open: false })}
        message={snackbar.message}
      />
    </div>
  );
};

export default EdicaoDados; 