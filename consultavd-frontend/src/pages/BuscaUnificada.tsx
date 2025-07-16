import React, { useState, useCallback, useMemo } from 'react';
import { apiService } from '../services/api';
import { SearchResult } from '../types';
import { 
  Box, 
  Typography, 
  TextField, 
  Button, 
  CircularProgress, 
  Alert, 
  Paper, 
  Tabs, 
  Tab, 
  Container, 
  Select, 
  MenuItem, 
  FormControl, 
  InputLabel, 
  List, 
  ListItem, 
  ListItemText, 
  ListItemIcon, 
  Chip, 
  Divider,
  IconButton,
  Tooltip,
  Badge,
  Fab,
  Card,
  CardContent,
  Grid,
  InputAdornment,
  Autocomplete,
  Switch,
  FormControlLabel,
  Collapse,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Skeleton,
  Fade,
  Zoom,
  Slide
} from '@mui/material';
import PeopleCard from '../components/PeopleCard';
import PeopleContactCard from '../components/PeopleContactCard';
import CarimboGenerator from '../components/CarimboGenerator';
import LojaDetalheCard from '../components/LojaDetalheCard';
import BusinessIcon from '@mui/icons-material/Business';
import ContentCopyIcon from '@mui/icons-material/ContentCopy';
import SearchIcon from '@mui/icons-material/Search';
import SortIcon from '@mui/icons-material/Sort';
import RoomIcon from '@mui/icons-material/Room';
import EmailIcon from '@mui/icons-material/Email';
import PhoneIcon from '@mui/icons-material/Phone';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import FilterListIcon from '@mui/icons-material/FilterList';
import RefreshIcon from '@mui/icons-material/Refresh';
import ClearIcon from '@mui/icons-material/Clear';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import LocationOnIcon from '@mui/icons-material/LocationOn';
import PersonIcon from '@mui/icons-material/Person';
import StoreIcon from '@mui/icons-material/Store';
import WifiIcon from '@mui/icons-material/Wifi';
import ContactSupportIcon from '@mui/icons-material/ContactSupport';

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
  { label: 'People/PEOP', icon: <PersonIcon />, color: '#2196f3' },
  { label: 'Designação', icon: <BusinessIcon />, color: '#4caf50' },
  { label: 'ID Vivo', icon: <WifiIcon />, color: '#ff9800' },
  { label: 'Endereço', icon: <LocationOnIcon />, color: '#9c27b0' },
  { label: 'Busca Loja > Operadora > Circuito', icon: <StoreIcon />, color: '#f44336' },
  { label: 'GGL e GR', icon: <ContactSupportIcon />, color: '#607d8b' },
];

const statusOptions = [
  { value: '', label: 'Todos', color: '#757575' },
  { value: 'ATIVA', label: 'Ativa', color: '#4caf50' },
  { value: 'INATIVA', label: 'Inativa', color: '#f44336' },
  { value: 'PENDENTE', label: 'Pendente', color: '#ff9800' },
];

const BuscaUnificada: React.FC = () => {
  const [tab, setTab] = useState(0);
  const [result, setResult] = useState<SearchResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showFilters, setShowFilters] = useState(false);
  const [autoSearch, setAutoSearch] = useState(false);

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
  const debouncedPeopleCode = useDebounce(peopleCode, 500);
  const debouncedDesignation = useDebounce(designation, 500);
  const debouncedIdVivo = useDebounce(idVivo, 500);
  const debouncedAddress = useDebounce(address, 500);

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

  // Auto-search quando habilitado
  React.useEffect(() => {
    if (autoSearch) {
      const currentValue = tab === 0 ? debouncedPeopleCode : 
                          tab === 1 ? debouncedDesignation :
                          tab === 2 ? debouncedIdVivo :
                          tab === 3 ? debouncedAddress : '';
      
      if (currentValue.length >= 3) {
        handleSearch();
      }
    }
  }, [autoSearch, debouncedPeopleCode, debouncedDesignation, debouncedIdVivo, debouncedAddress, tab, handleSearch]);

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

  const clearSearch = useCallback(() => {
    setPeopleCode('');
    setDesignation('');
    setIdVivo('');
    setAddress('');
    setGglGrSearch('');
    setResult(null);
    setError(null);
  }, []);

  return (
    <Container maxWidth="xl" sx={{ mt: 2, mb: 4 }}>
      {/* Header com controles */}
      <Box sx={{ 
        display: 'flex', 
        justifyContent: 'space-between', 
        alignItems: 'center', 
        mb: 3,
        flexDirection: { xs: 'column', md: 'row' },
        gap: 2
      }}>
        <Box>
          <Typography 
            variant="h4" 
            component="h1" 
            fontWeight="bold"
            sx={{ 
              background: 'linear-gradient(45deg, #2196F3, #21CBF3)',
              backgroundClip: 'text',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              mb: 0.5
            }}
          >
            🔍 Busca Unificada
          </Typography>
          <Typography variant="body2" color="textSecondary">
            Sistema de busca integrado para consultas rápidas
          </Typography>
        </Box>
        
        <Box sx={{ display: 'flex', gap: 1, alignItems: 'center' }}>
          <FormControlLabel
            control={
              <Switch
                checked={autoSearch}
                onChange={(e) => setAutoSearch(e.target.checked)}
                size="small"
              />
            }
            label="Auto-busca"
          />
          
          <Tooltip title="Filtros">
            <IconButton 
              onClick={() => setShowFilters(!showFilters)}
              sx={{ 
                bgcolor: showFilters ? 'primary.main' : 'transparent',
                color: showFilters ? 'white' : 'inherit',
                '&:hover': {
                  bgcolor: showFilters ? 'primary.dark' : 'action.hover'
                }
              }}
            >
              <FilterListIcon />
            </IconButton>
          </Tooltip>
          
          <Tooltip title="Limpar">
            <IconButton onClick={clearSearch}>
              <ClearIcon />
            </IconButton>
          </Tooltip>
        </Box>
      </Box>

      {/* Tabs melhorados */}
      <Paper sx={{ mb: 3, borderRadius: 3, overflow: 'hidden' }}>
        <Tabs
          value={tab}
          onChange={handleTabChange}
          indicatorColor="primary"
          textColor="primary"
          variant="scrollable"
          scrollButtons="auto"
          sx={{
            '& .MuiTab-root': {
              minHeight: 64,
              fontSize: '0.9rem',
              fontWeight: 600,
              textTransform: 'none',
              '&.Mui-selected': {
                color: tabLabels[tab]?.color || 'primary.main',
              }
            },
            '& .MuiTabs-indicator': {
              backgroundColor: tabLabels[tab]?.color || 'primary.main',
              height: 3
            }
          }}
        >
          {tabLabels.map((tabInfo, idx) => (
            <Tab 
              key={tabInfo.label} 
              label={
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                  {tabInfo.icon}
                  <Typography variant="body2">{tabInfo.label}</Typography>
                </Box>
              }
              sx={{ color: tab === idx ? tabInfo.color : 'inherit' }}
            />
          ))}
        </Tabs>
      </Paper>

      {/* Filtros avançados */}
      <Collapse in={showFilters}>
        <Paper sx={{ p: 3, mb: 3, borderRadius: 3 }}>
          <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            🔧 Filtros Avançados
          </Typography>
          <Grid container spacing={2} alignItems="center">
            <Grid item xs={12} sm={6} md={3}>
              <FormControl fullWidth size="small">
                <InputLabel>Status</InputLabel>
                <Select
                  value={statusFilter}
                  onChange={(e) => setStatusFilter(e.target.value)}
                  label="Status"
                >
                  {statusOptions.map((option) => (
                    <MenuItem key={option.value} value={option.value}>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        <Box sx={{ width: 12, height: 12, borderRadius: '50%', bgcolor: option.color }} />
                        {option.label}
                      </Box>
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <TextField
                label="Busca rápida"
                value={quickSearch}
                onChange={(e) => setQuickSearch(e.target.value)}
                size="small"
                fullWidth
                placeholder="Nome, código ou cidade..."
              />
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <FormControl fullWidth size="small">
                <InputLabel>Ordenar por</InputLabel>
                <Select
                  value={sortField}
                  onChange={(e) => setSortField(e.target.value as any)}
                  label="Ordenar por"
                >
                  <MenuItem value="nome">Nome</MenuItem>
                  <MenuItem value="codigo">Código</MenuItem>
                  <MenuItem value="cidade">Cidade</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Button
                variant="outlined"
                onClick={() => setSortAsc(!sortAsc)}
                startIcon={<SortIcon />}
                fullWidth
              >
                {sortAsc ? 'A-Z' : 'Z-A'}
              </Button>
            </Grid>
          </Grid>
        </Paper>
      </Collapse>
      
      {/* Conteúdo das abas */}
      <Fade in timeout={300}>
        <Box>
          {tab === 0 && (
            <Card sx={{ mb: 3, borderRadius: 3 }}>
              <CardContent>
                <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                  <PersonIcon color="primary" />
                  Busca por código People/PEOP
                </Typography>
                <Box display="flex" gap={2} alignItems="flex-end">
                  <TextField
                    label="Código People/PEOP"
                    value={peopleCode}
                    onChange={e => setPeopleCode(e.target.value)}
                    onKeyPress={handleKeyPress}
                    fullWidth
                    placeholder="Digite o código People/PEOP"
                    InputProps={{
                      startAdornment: (
                        <InputAdornment position="start">
                          <PersonIcon color="action" />
                        </InputAdornment>
                      ),
                    }}
                  />
                  <Button 
                    variant="contained" 
                    color="primary" 
                    onClick={handleSearch} 
                    disabled={loading || !peopleCode}
                    startIcon={loading ? <CircularProgress size={20} /> : <SearchIcon />}
                    sx={{ minWidth: 120 }}
                  >
                    {loading ? 'Buscando...' : 'Buscar'}
                  </Button>
                </Box>
              </CardContent>
            </Card>
          )}
          
          {tab === 1 && (
            <Card sx={{ mb: 3, borderRadius: 3 }}>
              <CardContent>
                <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                  <BusinessIcon color="primary" />
                  Busca por Designação
                </Typography>
                <Box display="flex" gap={2} alignItems="flex-end">
                  <TextField
                    label="Designação"
                    value={designation}
                    onChange={e => setDesignation(e.target.value)}
                    onKeyPress={handleKeyPress}
                    fullWidth
                    placeholder="Digite a designação da loja"
                    InputProps={{
                      startAdornment: (
                        <InputAdornment position="start">
                          <BusinessIcon color="action" />
                        </InputAdornment>
                      ),
                    }}
                  />
                  <Button 
                    variant="contained" 
                    color="primary" 
                    onClick={handleSearch} 
                    disabled={loading || !designation}
                    startIcon={loading ? <CircularProgress size={20} /> : <SearchIcon />}
                    sx={{ minWidth: 120 }}
                  >
                    {loading ? 'Buscando...' : 'Buscar'}
                  </Button>
                </Box>
              </CardContent>
            </Card>
          )}
          
          {tab === 2 && (
            <Card sx={{ mb: 3, borderRadius: 3 }}>
              <CardContent>
                <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                  <WifiIcon color="primary" />
                  Busca por ID Vivo
                </Typography>
                <Box display="flex" gap={2} alignItems="flex-end">
                  <TextField
                    label="ID Vivo"
                    value={idVivo}
                    onChange={e => setIdVivo(e.target.value)}
                    onKeyPress={handleKeyPress}
                    fullWidth
                    placeholder="Digite o ID Vivo"
                    InputProps={{
                      startAdornment: (
                        <InputAdornment position="start">
                          <WifiIcon color="action" />
                        </InputAdornment>
                      ),
                    }}
                  />
                  <Button 
                    variant="contained" 
                    color="primary" 
                    onClick={handleSearch} 
                    disabled={loading || !idVivo}
                    startIcon={loading ? <CircularProgress size={20} /> : <SearchIcon />}
                    sx={{ minWidth: 120 }}
                  >
                    {loading ? 'Buscando...' : 'Buscar'}
                  </Button>
                </Box>
              </CardContent>
            </Card>
          )}
          
          {tab === 3 && (
            <Card sx={{ mb: 3, borderRadius: 3 }}>
              <CardContent>
                <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                  <LocationOnIcon color="primary" />
                  Busca por Endereço
                </Typography>
                <Box display="flex" gap={2} alignItems="flex-end">
                  <TextField
                    label="Endereço"
                    value={address}
                    onChange={e => setAddress(e.target.value)}
                    onKeyPress={handleKeyPress}
                    fullWidth
                    placeholder="Digite o endereço"
                    InputProps={{
                      startAdornment: (
                        <InputAdornment position="start">
                          <LocationOnIcon color="action" />
                        </InputAdornment>
                      ),
                    }}
                  />
                  <Button 
                    variant="contained" 
                    color="primary" 
                    onClick={handleSearch} 
                    disabled={loading || !address}
                    startIcon={loading ? <CircularProgress size={20} /> : <SearchIcon />}
                    sx={{ minWidth: 120 }}
                  >
                    {loading ? 'Buscando...' : 'Buscar'}
                  </Button>
                </Box>
              </CardContent>
            </Card>
          )}
          
          {tab === 4 && (
            <Box>
              {/* Header da seção */}
              <Card sx={{ mb: 3, borderRadius: 3, background: 'linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)' }}>
                <CardContent>
                  <Typography variant="h5" gutterBottom sx={{ 
                    display: 'flex', 
                    alignItems: 'center', 
                    gap: 2,
                    fontWeight: 'bold',
                    color: '#2c3e50'
                  }}>
                    <StoreIcon sx={{ fontSize: 32, color: '#e74c3c' }} />
                    Busca Loja {'>'} Operadora {'>'} Circuito
                  </Typography>
                  <Typography variant="body1" color="textSecondary" sx={{ ml: 6 }}>
                    Selecione uma loja, operadora e circuito para buscar informações detalhadas
                  </Typography>
                </CardContent>
              </Card>

              {/* Fluxo de seleção */}
              <Grid container spacing={3}>
                {/* Passo 1: Busca de Loja */}
                <Grid item xs={12} md={4}>
                  <Card sx={{ 
                    borderRadius: 3, 
                    height: '100%',
                    border: selectedLoja ? '2px solid #27ae60' : '2px solid transparent',
                    transition: 'all 0.3s ease',
                    '&:hover': { transform: 'translateY(-2px)', boxShadow: 4 }
                  }}>
                    <CardContent>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
                        <Box sx={{ 
                          width: 32, 
                          height: 32, 
                          borderRadius: '50%', 
                          bgcolor: selectedLoja ? '#27ae60' : '#95a5a6',
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          color: 'white',
                          fontWeight: 'bold'
                        }}>
                          1
                        </Box>
                        <Typography variant="h6" fontWeight="bold" color={selectedLoja ? 'success.main' : 'text.primary'}>
                          Busque a Loja
                        </Typography>
                      </Box>
                      
                      <TextField
                        label="Nome ou código da loja"
                        value={lojaSearch}
                        onChange={e => handleLojaSearch(e.target.value)}
                        fullWidth
                        size="small"
                        placeholder="Ex: São Paulo ou SP001"
                        InputProps={{
                          startAdornment: (
                            <InputAdornment position="start">
                              <SearchIcon color="action" />
                            </InputAdornment>
                          ),
                        }}
                        sx={{ mb: 2 }}
                      />
                      
                      {lojasFiltradas.length > 0 && (
                        <FormControl fullWidth size="small">
                          <InputLabel>Selecione a Loja</InputLabel>
                          <Select
                            value={selectedLoja}
                            onChange={e => handleLojaSelect(e.target.value)}
                            label="Selecione a Loja"
                          >
                            {lojasFiltradas.map((loja) => (
                              <MenuItem key={loja.id} value={loja.id}>
                                <Box>
                                  <Typography variant="body2" fontWeight="bold">
                                    {loja.codigo} - {loja.nome}
                                  </Typography>
                                  <Typography variant="caption" color="textSecondary">
                                    {loja.cidade} - {loja.uf}
                                  </Typography>
                                </Box>
                              </MenuItem>
                            ))}
                          </Select>
                        </FormControl>
                      )}
                    </CardContent>
                  </Card>
                </Grid>

                {/* Passo 2: Seleção de Operadora */}
                <Grid item xs={12} md={4}>
                  <Card sx={{ 
                    borderRadius: 3, 
                    height: '100%',
                    border: selectedOperadora ? '2px solid #3498db' : '2px solid transparent',
                    transition: 'all 0.3s ease',
                    '&:hover': { transform: 'translateY(-2px)', boxShadow: 4 },
                    opacity: selectedLoja ? 1 : 0.6
                  }}>
                    <CardContent>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
                        <Box sx={{ 
                          width: 32, 
                          height: 32, 
                          borderRadius: '50%', 
                          bgcolor: selectedOperadora ? '#3498db' : '#95a5a6',
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          color: 'white',
                          fontWeight: 'bold'
                        }}>
                          2
                        </Box>
                        <Typography variant="h6" fontWeight="bold" color={selectedOperadora ? 'primary.main' : 'text.primary'}>
                          Operadora
                        </Typography>
                      </Box>
                      
                      <FormControl fullWidth size="small" disabled={!selectedLoja}>
                        <InputLabel>Selecione a Operadora</InputLabel>
                        <Select
                          value={selectedOperadora}
                          onChange={e => handleOperadoraSelect(e.target.value)}
                          label="Selecione a Operadora"
                        >
                          {operadoras.map((operadora) => (
                            <MenuItem key={operadora} value={operadora}>
                              {operadora}
                            </MenuItem>
                          ))}
                        </Select>
                      </FormControl>
                      
                      {!selectedLoja && (
                        <Typography variant="caption" color="textSecondary" sx={{ mt: 1, display: 'block' }}>
                          Selecione uma loja primeiro
                        </Typography>
                      )}
                    </CardContent>
                  </Card>
                </Grid>

                {/* Passo 3: Seleção de Circuito */}
                <Grid item xs={12} md={4}>
                  <Card sx={{ 
                    borderRadius: 3, 
                    height: '100%',
                    border: selectedCircuito ? '2px solid #e74c3c' : '2px solid transparent',
                    transition: 'all 0.3s ease',
                    '&:hover': { transform: 'translateY(-2px)', boxShadow: 4 },
                    opacity: selectedOperadora ? 1 : 0.6
                  }}>
                    <CardContent>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
                        <Box sx={{ 
                          width: 32, 
                          height: 32, 
                          borderRadius: '50%', 
                          bgcolor: selectedCircuito ? '#e74c3c' : '#95a5a6',
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          color: 'white',
                          fontWeight: 'bold'
                        }}>
                          3
                        </Box>
                        <Typography variant="h6" fontWeight="bold" color={selectedCircuito ? 'error.main' : 'text.primary'}>
                          Circuito
                        </Typography>
                      </Box>
                      
                      <FormControl fullWidth size="small" disabled={!selectedOperadora}>
                        <InputLabel>Selecione o Circuito</InputLabel>
                        <Select
                          value={selectedCircuito}
                          onChange={e => setSelectedCircuito(e.target.value)}
                          label="Selecione o Circuito"
                        >
                          {circuitos.map((circuito) => (
                            <MenuItem key={circuito} value={circuito}>
                              {circuito}
                            </MenuItem>
                          ))}
                        </Select>
                      </FormControl>
                      
                      {!selectedOperadora && (
                        <Typography variant="caption" color="textSecondary" sx={{ mt: 1, display: 'block' }}>
                          Selecione uma operadora primeiro
                        </Typography>
                      )}
                    </CardContent>
                  </Card>
                </Grid>
              </Grid>

              {/* Botão de busca */}
              {selectedCircuito && (
                <Box sx={{ 
                  display: 'flex', 
                  justifyContent: 'center', 
                  mt: 4,
                  animation: 'fadeInUp 0.5s ease'
                }}>
                  <Button 
                    variant="contained" 
                    color="primary" 
                    onClick={handleSearch}
                    disabled={loading}
                    startIcon={loading ? <CircularProgress size={20} /> : <SearchIcon />}
                    size="large"
                    sx={{ 
                      minWidth: 250,
                      height: 56,
                      fontSize: '1.1rem',
                      fontWeight: 'bold',
                      borderRadius: 3,
                      background: 'linear-gradient(45deg, #2196F3 30%, #21CBF3 90%)',
                      boxShadow: '0 3px 5px 2px rgba(33, 203, 243, .3)',
                      '&:hover': {
                        background: 'linear-gradient(45deg, #1976D2 30%, #1E88E5 90%)',
                        transform: 'scale(1.05)'
                      }
                    }}
                  >
                    {loading ? 'Buscando...' : '🔍 Buscar Circuito'}
                  </Button>
                </Box>
              )}

              {/* Indicador de progresso */}
              <Box sx={{ mt: 3, display: 'flex', justifyContent: 'center' }}>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                  <Box sx={{ 
                    width: 12, 
                    height: 12, 
                    borderRadius: '50%', 
                    bgcolor: selectedLoja ? '#27ae60' : '#ecf0f1' 
                  }} />
                  <Box sx={{ 
                    width: 40, 
                    height: 2, 
                    bgcolor: selectedOperadora ? '#3498db' : '#ecf0f1' 
                  }} />
                  <Box sx={{ 
                    width: 12, 
                    height: 12, 
                    borderRadius: '50%', 
                    bgcolor: selectedOperadora ? '#3498db' : '#ecf0f1' 
                  }} />
                  <Box sx={{ 
                    width: 40, 
                    height: 2, 
                    bgcolor: selectedCircuito ? '#e74c3c' : '#ecf0f1' 
                  }} />
                  <Box sx={{ 
                    width: 12, 
                    height: 12, 
                    borderRadius: '50%', 
                    bgcolor: selectedCircuito ? '#e74c3c' : '#ecf0f1' 
                  }} />
                </Box>
              </Box>
            </Box>
          )}
          
          {tab === 5 && (
            <Card sx={{ mb: 3, borderRadius: 3 }}>
              <CardContent>
                <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                  <ContactSupportIcon color="primary" />
                  Busca por GGL e GR
                </Typography>
                <Box display="flex" gap={2} alignItems="flex-end">
                  <TextField
                    label="GGL ou GR"
                    value={gglGrSearch}
                    onChange={e => setGglGrSearch(e.target.value)}
                    onKeyPress={handleKeyPress}
                    fullWidth
                    placeholder="Digite o nome do GGL ou GR"
                    InputProps={{
                      startAdornment: (
                        <InputAdornment position="start">
                          <ContactSupportIcon color="action" />
                        </InputAdornment>
                      ),
                    }}
                  />
                  <Button 
                    variant="contained" 
                    color="primary" 
                    onClick={handleSearch} 
                    disabled={loading || !gglGrSearch}
                    startIcon={loading ? <CircularProgress size={20} /> : <SearchIcon />}
                    sx={{ minWidth: 120 }}
                  >
                    {loading ? 'Buscando...' : 'Buscar'}
                  </Button>
                </Box>
              </CardContent>
            </Card>
          )}
        </Box>
      </Fade>

      {/* Resultados */}
      {error && (
        <Alert severity="error" sx={{ mb: 3, borderRadius: 2 }}>
          {error}
        </Alert>
      )}

      {result && (
        <Zoom in timeout={500}>
          <Box>


            {/* Lista de resultados */}
            <Card sx={{ borderRadius: 3 }}>
              <CardContent>
                <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                  📊 Resultados ({totalLojas} encontrados)
                </Typography>
                
                {filteredAndSortedLojas.map((loja, idx) => {
                  const handleCopy = (text: string, type: string) => {
                    navigator.clipboard.writeText(text);
                    setCopied(`${type}-${idx}`);
                    setTimeout(() => setCopied(''), 2000);
                  };

                  const handleExpand = () => setExpandedIdx(expandedIdx === idx ? null : idx);

                  const handleMap = () => {
                    const endereco = loja.endereco || (loja as any)['ENDEREÇO'] || '';
                    if (endereco) {
                      window.open(`https://www.google.com/maps/search/${encodeURIComponent(endereco)}`, '_blank');
                    }
                  };

                  const handleEmail = () => {
                    const email = (loja as any)['EMAIL'] || '';
                    if (email) {
                      window.open(`mailto:${email}`, '_blank');
                    }
                  };

                  return (
                    <Accordion 
                      key={idx} 
                      expanded={expandedIdx === idx}
                      onChange={handleExpand}
                      sx={{ 
                        mb: 1, 
                        borderRadius: 2,
                        '&:before': { display: 'none' },
                        boxShadow: 2
                      }}
                    >
                      <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, width: '100%' }}>
                          <BusinessIcon color="primary" />
                          <Box sx={{ flex: 1 }}>
                            <Typography variant="subtitle1" fontWeight={600}>
                              {loja.nome || (loja as any)['NOME'] || (loja as any)['LOJAS']}
                            </Typography>
                            <Typography variant="body2" color="textSecondary">
                              Código: {loja.id || (loja as any)['codigo'] || (loja as any)['CODIGO']} | 
                              Cidade: {loja.cidade || (loja as any)['CIDADE']}
                            </Typography>
                          </Box>
                          <Chip 
                            label={loja.status || (loja as any)['STATUS'] || (loja as any)['Status_Loja']} 
                            color={loja.status === 'ATIVA' ? 'success' : loja.status === 'INATIVA' ? 'error' : 'warning'}
                            size="small"
                          />
                        </Box>
                      </AccordionSummary>
                                             <AccordionDetails>
                         <LojaDetalheCard data={loja} />
                       </AccordionDetails>
                    </Accordion>
                  );
                })}
              </CardContent>
            </Card>
          </Box>
        </Zoom>
      )}

      {/* FAB para ações rápidas */}
      <Fab
        color="primary"
        aria-label="search"
        sx={{ 
          position: 'fixed', 
          bottom: 16, 
          right: 16,
          boxShadow: 4,
          '&:hover': {
            transform: 'scale(1.1)',
            boxShadow: 6
          },
          transition: 'all 0.2s ease'
        }}
        onClick={handleSearch}
        disabled={loading}
      >
        {loading ? <CircularProgress size={24} color="inherit" /> : <SearchIcon />}
      </Fab>
    </Container>
  );
};

export default BuscaUnificada; 