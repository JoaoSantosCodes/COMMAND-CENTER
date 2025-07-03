import React, { useState, useCallback, useMemo } from 'react';
import { apiService } from '../services/api';
import { SearchResult } from '../types';
import { Box, Typography, TextField, Button, CircularProgress, Alert, Paper, Tabs, Tab, Container, Select, MenuItem, FormControl, InputLabel, List, ListItem, ListItemText, ListItemIcon, Chip, Divider } from '@mui/material';
import PeopleCard from '../components/PeopleCard';
import PeopleContactCard from '../components/PeopleContactCard';
import CarimboGenerator from '../components/CarimboGenerator';
import LojaDetalheCard from '../components/LojaDetalheCard';
import BusinessIcon from '@mui/icons-material/Business';
import ContentCopyIcon from '@mui/icons-material/ContentCopy';
import SearchIcon from '@mui/icons-material/Search';
import SortIcon from '@mui/icons-material/Sort';
import PieChartOutlineIcon from '@mui/icons-material/PieChartOutline';
import { PieChart, Pie, Cell, Tooltip as RechartsTooltip, ResponsiveContainer } from 'recharts';
import RoomIcon from '@mui/icons-material/Room';
import EmailIcon from '@mui/icons-material/Email';
import PhoneIcon from '@mui/icons-material/Phone';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import Collapse from '@mui/material/Collapse';
import Tooltip from '@mui/material/Tooltip';

// Hook para debounce
const useDebounce = (value: string, delay: number) => {
  const [debouncedValue, setDebouncedValue] = useState(value);

  React.useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => {
      clearTimeout(handler);
    };
  }, [value, delay]);

  return debouncedValue;
};

const tabLabels = [
  'People/PEOP',
  'Designação',
  'ID Vivo',
  'Endereço',
  'Busca Loja > Operadora > Circuito',
  'GGL e GR',
];

const statusOptions = [
  { value: '', label: 'Todos' },
  { value: 'ATIVA', label: 'Ativa' },
  { value: 'INATIVA', label: 'Inativa' },
  { value: 'PENDENTE', label: 'Pendente' },
];

const BuscaUnificada: React.FC = () => {
  const [tab, setTab] = useState(0);
  const [result, setResult] = useState<SearchResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Campos separados para cada tab
  const [peopleCode, setPeopleCode] = useState('');
  const [designation, setDesignation] = useState('');
  const [idVivo, setIdVivo] = useState('');
  const [address, setAddress] = useState('');
  
  // Campos para Busca Loja > Operadora > Circuito
  const [lojaSearch, setLojaSearch] = useState('');
  const [selectedLoja, setSelectedLoja] = useState('');
  const [selectedOperadora, setSelectedOperadora] = useState('');
  const [selectedCircuito, setSelectedCircuito] = useState('');
  const [lojasFiltradas, setLojasFiltradas] = useState<any[]>([]);
  const [operadoras, setOperadoras] = useState<string[]>([]);
  const [circuitos, setCircuitos] = useState<string[]>([]);

  // Campos para GGL e GR
  const [gglGrSearch, setGglGrSearch] = useState('');

  // Debounce para busca de lojas
  const debouncedLojaSearch = useDebounce(lojaSearch, 300);

  // Memoizar resultados para evitar re-renders desnecessários
  const memoizedResult = useMemo(() => result, [result]);

  const [statusFilter, setStatusFilter] = useState('');

  // Filtrar lojas pelo status selecionado
  const filteredLojas = useMemo(() => {
    if (!result?.lojas) return [];
    if (!statusFilter) return result.lojas;
    return result.lojas.filter(
      loja => loja.status === statusFilter
    );
  }, [result, statusFilter]);

  const [quickSearch, setQuickSearch] = useState('');
  const [sortField, setSortField] = useState<'nome' | 'codigo' | 'cidade'>('nome');
  const [sortAsc, setSortAsc] = useState(true);

  // Função para filtrar e ordenar lojas
  const filteredAndSortedLojas = useMemo(() => {
    let arr = filteredLojas;
    if (quickSearch) {
      const q = quickSearch.toLowerCase();
      arr = arr.filter(loja => {
        const nome = loja.nome || (loja as any)['NOME'] || (loja as any)['LOJAS'] || '';
        const codigo = String(loja.id || (loja as any)['codigo'] || (loja as any)['CODIGO'] || '');
        const cidade = loja.cidade || (loja as any)['CIDADE'] || '';
        return nome.toLowerCase().includes(q) || codigo.includes(q) || cidade.toLowerCase().includes(q);
      });
    }
    arr = [...arr].sort((a, b) => {
      const get = (loja: any) => {
        if (sortField === 'nome') return (loja.nome || loja['NOME'] || loja['LOJAS'] || '').toLowerCase();
        if (sortField === 'codigo') return String(loja.id || loja['codigo'] || loja['CODIGO'] || '');
        if (sortField === 'cidade') return (loja.cidade || loja['CIDADE'] || '').toLowerCase();
        return '';
      };
      const va = get(a), vb = get(b);
      if (va < vb) return sortAsc ? -1 : 1;
      if (va > vb) return sortAsc ? 1 : -1;
      return 0;
    });
    return arr;
  }, [filteredLojas, quickSearch, sortField, sortAsc]);

  // Estatísticas
  const totalLojas = filteredAndSortedLojas.length;
  const statusCount = filteredAndSortedLojas.reduce((acc, loja) => {
    const status = loja.status || (loja as any)['STATUS'] || (loja as any)['Status_Loja'] || '-';
    acc[status] = (acc[status] || 0) + 1;
    return acc;
  }, {} as Record<string, number>);
  const cidadesCount = filteredAndSortedLojas.reduce((acc, loja) => {
    const cidade = (loja.cidade || (loja as any)['CIDADE'] || '-').toUpperCase();
    acc[cidade] = (acc[cidade] || 0) + 1;
    return acc;
  }, {} as Record<string, number>);
  const cidadesMaisFrequentes = Object.entries(cidadesCount).sort((a, b) => b[1] - a[1]).slice(0, 3);
  const statusColors = { 'ATIVA': '#43a047', 'INATIVA': '#e53935', 'PENDENTE': '#fbc02d', '-': '#757575' };
  const statusData = Object.entries(statusCount).map(([status, value]) => ({ name: status, value, color: statusColors[status as keyof typeof statusColors] || '#757575' }));

  const handleSearch = useCallback(async () => {
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      let data: SearchResult | null = null;
      if (tab === 0) {
        data = await apiService.searchByPeople(peopleCode);
      } else if (tab === 1) {
        data = await apiService.searchByDesignation(designation);
      } else if (tab === 2) {
        data = await apiService.searchByIdVivo(idVivo);
      } else if (tab === 3) {
        data = await apiService.searchByAddress(address);
      } else if (tab === 4) {
        // Busca Loja > Operadora > Circuito
        if (selectedLoja && selectedOperadora && selectedCircuito) {
          data = await apiService.searchByLojaOperadoraCircuito(selectedLoja, selectedOperadora, selectedCircuito);
        } else {
          setError('Selecione Loja, Operadora e Circuito');
        }
      } else if (tab === 5) {
        // Busca por GGL e GR
        data = await apiService.searchByGglGr(gglGrSearch);
      } else {
        setError('Busca ainda não implementada para esta aba');
      }
      if (data) setResult(data);
    } catch (e) {
      setError('Erro ao buscar dados');
    } finally {
      setLoading(false);
    }
  }, [tab, peopleCode, designation, address, selectedLoja, selectedOperadora, selectedCircuito, gglGrSearch, idVivo]);

  const handleKeyPress = useCallback((event: React.KeyboardEvent) => {
    if (event.key === 'Enter') {
      handleSearch();
    }
  }, [handleSearch]);

  // Buscar lojas quando digitar no campo de busca (com debounce)
  const handleLojaSearch = useCallback(async (searchTerm: string) => {
    setLojaSearch(searchTerm);
  }, []);

  // Efeito para buscar lojas com debounce
  React.useEffect(() => {
    if (debouncedLojaSearch.length >= 2) {
      const searchLojas = async () => {
        try {
          const response = await apiService.searchLojas(debouncedLojaSearch);
          setLojasFiltradas(response.data || []);
        } catch (e) {
          setLojasFiltradas([]);
        }
      };
      searchLojas();
    } else {
      setLojasFiltradas([]);
    }
  }, [debouncedLojaSearch]);

  // Buscar operadoras quando selecionar uma loja
  const handleLojaSelect = useCallback(async (lojaId: string) => {
    setSelectedLoja(lojaId);
    setSelectedOperadora('');
    setSelectedCircuito('');
    setOperadoras([]);
    setCircuitos([]);
    
    if (lojaId) {
      try {
        const response = await apiService.getOperadorasByLoja(lojaId);
        setOperadoras(response.data || []);
      } catch (e) {
        setOperadoras([]);
      }
    }
  }, []);

  // Buscar circuitos quando selecionar uma operadora
  const handleOperadoraSelect = useCallback(async (operadora: string) => {
    setSelectedOperadora(operadora);
    setSelectedCircuito('');
    setCircuitos([]);
    
    if (operadora && selectedLoja) {
      try {
        const response = await apiService.getCircuitosByLojaOperadora(selectedLoja, operadora);
        setCircuitos(response.data || []);
      } catch (e) {
        setCircuitos([]);
      }
    }
  }, [selectedLoja]);

  // Resetar campos quando mudar de aba
  const handleTabChange = useCallback((_event: any, newValue: number) => {
    setTab(newValue);
    setResult(null);
    setError(null);
    // Resetar campos quando mudar de aba
    if (newValue !== 4) {
      setLojaSearch('');
      setSelectedLoja('');
      setSelectedOperadora('');
      setSelectedCircuito('');
      setLojasFiltradas([]);
      setOperadoras([]);
      setCircuitos([]);
    }
  }, []);

  const [expandedIdx, setExpandedIdx] = useState<number | null>(null);
  const [copied, setCopied] = useState<string>('');

  return (
    <Box>
      <Typography variant="h5" fontWeight={700} mb={2}>Busca Unificada</Typography>
      <Paper sx={{ mb: 2 }}>
        <Tabs
          value={tab}
          onChange={handleTabChange}
          indicatorColor="primary"
          textColor="primary"
          variant="scrollable"
          scrollButtons="auto"
        >
          {tabLabels.map((label, idx) => (
            <Tab label={label} key={label} />
          ))}
        </Tabs>
      </Paper>
      
      {tab === 0 && (
        <Box p={2}>
          <Typography>Busca por código People/PEOP</Typography>
          <Box display="flex" gap={2} mb={3} mt={2}>
            <TextField
              label="Código People/PEOP"
              value={peopleCode}
              onChange={e => setPeopleCode(e.target.value)}
              onKeyPress={handleKeyPress}
              fullWidth
            />
            <Button variant="contained" color="primary" onClick={handleSearch} disabled={loading || !peopleCode}>
              Buscar
            </Button>
          </Box>
        </Box>
      )}
      
      {tab === 1 && (
        <Box p={2}>
          <Typography>Busca por Designação</Typography>
          <Box display="flex" gap={2} mb={3} mt={2}>
            <TextField
              label="Designação"
              value={designation}
              onChange={e => setDesignation(e.target.value)}
              onKeyPress={handleKeyPress}
              fullWidth
            />
            <Button variant="contained" color="primary" onClick={handleSearch} disabled={loading || !designation}>
              Buscar
            </Button>
          </Box>
        </Box>
      )}
      
      {tab === 2 && (
        <Box p={2}>
          <Typography>Busca por ID Vivo</Typography>
          <Box display="flex" gap={2} mb={3} mt={2}>
            <TextField
              label="ID Vivo"
              value={idVivo}
              onChange={e => setIdVivo(e.target.value)}
              onKeyPress={handleKeyPress}
              fullWidth
              placeholder="Digite o ID Vivo"
            />
            <Button variant="contained" color="primary" onClick={handleSearch} disabled={loading || !idVivo}>
              Buscar
            </Button>
          </Box>
        </Box>
      )}
      
      {tab === 3 && (
        <Box p={2}>
          <Typography>Busca por Endereço</Typography>
          <Box display="flex" gap={2} mb={3} mt={2}>
            <TextField
              label="Endereço"
              value={address}
              onChange={e => setAddress(e.target.value)}
              onKeyPress={handleKeyPress}
              fullWidth
            />
            <Button variant="contained" color="primary" onClick={handleSearch} disabled={loading || !address}>
              Buscar
            </Button>
          </Box>
        </Box>
      )}
      
      {tab === 4 && (
        <Box p={2}>
          <Typography variant="h6" mb={2}>Busca Loja &gt; Operadora &gt; Circuito</Typography>
          
          {/* Busca de Loja */}
          <Box mb={3}>
            <Typography variant="subtitle1" mb={1}>1. Busque a Loja</Typography>
            <TextField
              label="Digite o nome ou código da loja"
              value={lojaSearch}
              onChange={e => handleLojaSearch(e.target.value)}
              fullWidth
              sx={{ mb: 2 }}
            />
            
            {lojasFiltradas.length > 0 && (
              <FormControl fullWidth sx={{ mb: 2 }}>
                <InputLabel>Selecione a Loja</InputLabel>
                <Select
                  value={selectedLoja}
                  onChange={e => handleLojaSelect(e.target.value)}
                  label="Selecione a Loja"
                >
                  {lojasFiltradas.map((loja) => (
                    <MenuItem key={loja.id} value={loja.id}>
                      {loja.codigo} - {loja.nome}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            )}
          </Box>

          {/* Seleção de Operadora */}
          {selectedLoja && (
            <Box mb={3}>
              <Typography variant="subtitle1" mb={1}>2. Selecione a Operadora</Typography>
              <FormControl fullWidth sx={{ mb: 2 }}>
                <InputLabel>Operadora</InputLabel>
                <Select
                  value={selectedOperadora}
                  onChange={e => handleOperadoraSelect(e.target.value)}
                  label="Operadora"
                >
                  {operadoras.map((operadora) => (
                    <MenuItem key={operadora} value={operadora}>
                      {operadora}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Box>
          )}

          {/* Seleção de Circuito */}
          {selectedOperadora && (
            <Box mb={3}>
              <Typography variant="subtitle1" mb={1}>3. Selecione o Circuito</Typography>
              <FormControl fullWidth sx={{ mb: 2 }}>
                <InputLabel>Circuito</InputLabel>
                <Select
                  value={selectedCircuito}
                  onChange={e => setSelectedCircuito(e.target.value)}
                  label="Circuito"
                >
                  {circuitos.map((circuito) => (
                    <MenuItem key={circuito} value={circuito}>
                      {circuito}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Box>
          )}

          {/* Botão de Busca */}
          {selectedCircuito && (
            <Box display="flex" gap={2}>
              <Button 
                variant="contained" 
                color="primary" 
                onClick={handleSearch} 
                disabled={loading}
                fullWidth
              >
                Buscar Circuito
              </Button>
            </Box>
          )}
        </Box>
      )}
      
      {tab === 5 && (
        <Box p={2}>
          <Typography>Busca por GGL e GR</Typography>
          <Box display="flex" gap={2} mb={3} mt={2}>
            <TextField
              label="Nome do GGL ou GR"
              value={gglGrSearch}
              onChange={e => setGglGrSearch(e.target.value)}
              onKeyPress={handleKeyPress}
              fullWidth
              placeholder="Digite o nome do GGL ou GR"
            />
            <Button variant="contained" color="primary" onClick={handleSearch} disabled={loading || !gglGrSearch}>
              Buscar
            </Button>
          </Box>
        </Box>
      )}
      
      {/* Loader e feedback visual aprimorado */}
      {loading && (
        <Box display="flex" flexDirection="column" alignItems="center" justifyContent="center" minHeight={200} my={4}>
          <CircularProgress size={48} thickness={5} />
          <Typography mt={2} fontWeight={600} color="text.secondary">Buscando...</Typography>
        </Box>
      )}
      {error && <Alert severity="error" sx={{ my: 2 }}>{error}</Alert>}

      {/* Filtro de status da loja */}
      {result?.lojas && result.lojas.length > 0 && (
        <Box display="flex" alignItems="center" gap={2} mb={2}>
          <FormControl size="small" sx={{ minWidth: 180 }}>
            <InputLabel>Status da Loja</InputLabel>
            <Select
              value={statusFilter}
              label="Status da Loja"
              onChange={e => setStatusFilter(e.target.value)}
            >
              {statusOptions.map(opt => (
                <MenuItem key={opt.value} value={opt.value}>{opt.label}</MenuItem>
              ))}
            </Select>
          </FormControl>
          <Typography variant="body2" color="text.secondary">
            {filteredLojas.length} loja(s) encontrada(s) com o status selecionado
          </Typography>
        </Box>
      )}

      {/* Exibir todos os resultados encontrados */}
      {result && (
        <Container maxWidth="md" sx={{ mb: 4, mt: 2 }}>
          {/* Lojas - exibição condicional */}
          {tab === 5 && filteredAndSortedLojas && (
            <Box mb={3}>
              {/* Resumo estatístico e busca rápida */}
              <Box display="flex" flexDirection={{ xs: 'column', md: 'row' }} alignItems={{ xs: 'stretch', md: 'center' }} gap={2} mb={2} flexWrap="wrap">
                <Box flex={1} display="flex" alignItems="center" gap={1} flexWrap="wrap">
                  <SearchIcon />
                  <TextField
                    size="small"
                    placeholder="Buscar por nome, código ou cidade..."
                    value={quickSearch}
                    onChange={e => setQuickSearch(e.target.value)}
                    sx={{ minWidth: 220 }}
                  />
                  <SortIcon sx={{ ml: 2 }} />
                  <Button
                    size="small"
                    variant={sortField === 'nome' ? 'contained' : 'outlined'}
                    onClick={() => setSortField('nome')}
                  >Nome</Button>
                  <Button
                    size="small"
                    variant={sortField === 'codigo' ? 'contained' : 'outlined'}
                    onClick={() => setSortField('codigo')}
                  >Código</Button>
                  <Button
                    size="small"
                    variant={sortField === 'cidade' ? 'contained' : 'outlined'}
                    onClick={() => setSortField('cidade')}
                  >Cidade</Button>
                  <Button
                    size="small"
                    onClick={() => setSortAsc(a => !a)}
                  >{sortAsc ? 'A-Z' : 'Z-A'}</Button>
                </Box>
                <Box display="flex" alignItems="center" gap={2} flexWrap="wrap" minWidth={0}>
                  <PieChartOutlineIcon />
                  <Typography variant="body2">Total: <b>{totalLojas}</b></Typography>
                  <Typography variant="body2" color="success.main">Ativas: <b>{statusCount['ATIVA'] || 0}</b></Typography>
                  <Typography variant="body2" color="error.main">Inativas: <b>{statusCount['INATIVA'] || 0}</b></Typography>
                  <Typography variant="body2" color="warning.main">Pendente: <b>{statusCount['PENDENTE'] || 0}</b></Typography>
                  {cidadesMaisFrequentes.length > 0 && (
                    <Typography variant="body2" sx={{ maxWidth: { xs: '100%', md: 220 }, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                      Cidades + comuns: {cidadesMaisFrequentes.map(([c, n]) => `${c} (${n})`).join(', ')}
                    </Typography>
                  )}
                  <Box width={60} height={60} minWidth={60}>
                    <ResponsiveContainer width="100%" height="100%">
                      <PieChart>
                        <Pie data={statusData} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={25}>
                          {statusData.map((entry, idx) => (
                            <Cell key={`cell-${idx}`} fill={entry.color} />
                          ))}
                        </Pie>
                        <RechartsTooltip />
                      </PieChart>
                    </ResponsiveContainer>
                  </Box>
                </Box>
              </Box>
              {/* Lista de lojas (restante do código permanece igual, mas usa filteredAndSortedLojas) */}
              <List sx={{ bgcolor: 'background.paper', borderRadius: 2, boxShadow: 2, p: 0 }}>
                {filteredAndSortedLojas.map((loja, idx) => {
                  const nome = loja.nome || (loja as any)['NOME'] || (loja as any)['LOJAS'] || '-';
                  const codigo = loja.id || (loja as any)['codigo'] || (loja as any)['CODIGO'] || '-';
                  const status = loja.status || (loja as any)['STATUS'] || (loja as any)['Status_Loja'] || '-';
                  const cidade = loja.cidade || (loja as any)['CIDADE'] || '-';
                  const uf = loja.uf || (loja as any)['UF'] || '-';
                  const endereco = loja.endereco || (loja as any)['ENDERECO'] || (loja as any)['ENDEREÇO'] || '-';
                  const email = (loja as any)['EMAIL'] || (loja as any)['E-MAIL'] || '';
                  const telefone = (loja as any)['TELEFONE'] || (loja as any)['TELEFONE 1'] || '';
                  // Funções de ação rápida
                  const handleCopy = (text: string, type: string) => {
                    navigator.clipboard.writeText(text);
                    setCopied(type + idx);
                    setTimeout(() => setCopied(''), 1200);
                  };
                  const handleExpand = () => setExpandedIdx(expandedIdx === idx ? null : idx);
                  const handleMap = () => {
                    const url = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(endereco + ', ' + cidade + ', ' + uf)}`;
                    window.open(url, '_blank');
                  };
                  const handleEmail = () => {
                    if (email) window.open(`mailto:${email}`);
                  };
                  return (
                    <React.Fragment key={loja.id || idx}>
                      <ListItem
                        alignItems="flex-start"
                        sx={{
                          bgcolor: idx % 2 === 0 ? 'background.default' : 'background.paper',
                          '&:hover': { bgcolor: 'action.hover', boxShadow: 2 },
                          py: 2, px: { xs: 1, md: 2 },
                          display: 'flex',
                          flexDirection: { xs: 'column', sm: 'row' },
                          alignItems: { xs: 'flex-start', sm: 'center' },
                          gap: 2,
                          outline: expandedIdx === idx ? '2px solid #1976d2' : 'none',
                          transition: 'outline 0.2s',
                        }}
                        tabIndex={0}
                        onKeyDown={e => { if (e.key === 'Enter' || e.key === ' ') handleExpand(); }}
                        secondaryAction={
                          <Box display="flex" alignItems="center" gap={1}>
                            <Tooltip title={copied === 'carimbo'+idx ? 'Copiado!' : 'Copiar carimbo'} open={copied === 'carimbo'+idx || undefined}>
                              <ContentCopyIcon
                                fontSize="small"
                                sx={{ cursor: 'pointer', ml: 1 }}
                                onClick={() => handleCopy(`**CARIMBO - CONSULTA VD**\nLoja: ${nome}\nCódigo: ${codigo}\nCidade: ${cidade}\nUF: ${uf}\nStatus: ${status}`,'carimbo')}
                                titleAccess="Copiar carimbo"
                              />
                            </Tooltip>
                            <Tooltip title="Ver no mapa">
                              <RoomIcon fontSize="small" sx={{ cursor: 'pointer' }} onClick={handleMap} />
                            </Tooltip>
                            {email && (
                              <Tooltip title="Enviar e-mail">
                                <EmailIcon fontSize="small" sx={{ cursor: 'pointer' }} onClick={handleEmail} />
                              </Tooltip>
                            )}
                            {telefone && (
                              <Tooltip title={copied === 'tel'+idx ? 'Copiado!' : 'Copiar telefone'} open={copied === 'tel'+idx || undefined}>
                                <PhoneIcon fontSize="small" sx={{ cursor: 'pointer' }} onClick={() => handleCopy(telefone, 'tel')} />
                              </Tooltip>
                            )}
                            <Tooltip title={expandedIdx === idx ? 'Recolher detalhes' : 'Expandir detalhes'}>
                              <ExpandMoreIcon
                                fontSize="small"
                                sx={{ cursor: 'pointer', transform: expandedIdx === idx ? 'rotate(180deg)' : 'rotate(0deg)', transition: 'transform 0.2s' }}
                                onClick={handleExpand}
                              />
                            </Tooltip>
                            <Chip label={status} color={status === 'ATIVA' ? 'success' : status === 'INATIVA' ? 'error' : status === 'PENDENTE' ? 'warning' : 'default'} size="small" sx={{ fontWeight: 700 }} />
                          </Box>
                        }
                      >
                        <ListItemIcon sx={{ minWidth: 36 }}>
                          <BusinessIcon color="primary" />
                        </ListItemIcon>
                        <Box flex={1} minWidth={0}>
                          <Typography variant="subtitle1" fontWeight={800} fontSize={18} noWrap>{nome}</Typography>
                          <Box display="flex" flexWrap="wrap" gap={2} mt={0.5}>
                            <Typography variant="body2" color="text.secondary">
                              Código: <b>{codigo}</b>
                            </Typography>
                            <Typography variant="body2" color="text.secondary">
                              Cidade: <b>{cidade}</b> / UF: <b>{uf}</b>
                            </Typography>
                          </Box>
                        </Box>
                      </ListItem>
                      <Collapse in={expandedIdx === idx} timeout="auto" unmountOnExit>
                        <Box px={4} py={2} bgcolor="background.default" borderRadius={2} mb={1}>
                          <Typography variant="body2" fontWeight={700} mb={1}>Endereço:</Typography>
                          <Typography variant="body2" mb={1}>{endereco}</Typography>
                          {telefone && (
                            <Typography variant="body2" mb={1}><PhoneIcon fontSize="inherit" sx={{ mr: 1 }} />{telefone}</Typography>
                          )}
                          {email && (
                            <Typography variant="body2" mb={1}><EmailIcon fontSize="inherit" sx={{ mr: 1 }} />{email}</Typography>
                          )}
                        </Box>
                      </Collapse>
                      {idx < filteredAndSortedLojas.length - 1 && <Divider component="li" />}
                    </React.Fragment>
                  );
                })}
              </List>
            </Box>
          )}
          {/* Lojas - cards detalhados para as demais abas */}
          {tab !== 5 && filteredLojas && filteredLojas.length > 0 && (
            <Box mb={3}>
              <Typography variant="h6">Lojas Encontradas</Typography>
              {filteredLojas.map((loja, idx) => (
                <Box key={loja.id || idx} mb={2}>
                  <LojaDetalheCard data={loja} />
                  <PeopleCard data={loja} />
                  <PeopleContactCard data={loja} />
                  <CarimboGenerator data={loja} />
                </Box>
              ))}
            </Box>
          )}
          {/* Nenhum resultado de loja */}
          {result.lojas && filteredLojas.length === 0 && (
            <Alert severity="info">Nenhuma loja encontrada com o status selecionado.</Alert>
          )}
          {/* Circuitos */}
          {result.circuitos && result.circuitos.length > 0 && (
            <Box mb={3}>
              <Typography variant="h6">Circuitos Encontrados</Typography>
              <ul>
                {result.circuitos.map((circuito, idx) => (
                  <li key={circuito.id || idx}>
                    <b>{circuito.designacao}</b> - Operadora: {circuito.operadora} - Tipo: {circuito.tipo} - Status: {circuito.status}
                  </li>
                ))}
              </ul>
            </Box>
          )}
          {/* Inventário */}
          {result.inventario && result.inventario.length > 0 && (
            <Box mb={3}>
              <Typography variant="h6">Inventário Encontrado</Typography>
              <ul>
                {result.inventario.map((item, idx) => (
                  <li key={item.id || idx}>
                    <b>{item.equipamento}</b> - Modelo: {item.modelo} - Serial: {item.serial} - Status: {item.status}
                  </li>
                ))}
              </ul>
            </Box>
          )}
          {/* Nenhum resultado */}
          {(!result.lojas?.length && !result.circuitos?.length && !result.inventario?.length) && (
            <Alert severity="info">Nenhum resultado encontrado.</Alert>
          )}
        </Container>
      )}
    </Box>
  );
};

export default BuscaUnificada; 