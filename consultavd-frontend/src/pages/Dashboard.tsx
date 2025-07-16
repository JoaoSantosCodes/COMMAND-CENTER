import React, { useState, useEffect } from 'react';
import {
  Box,
  Grid,
  Typography,
  Paper,
  CircularProgress,
  Alert,
  Container,
  Skeleton,
  Chip,
  IconButton,
  Tooltip,
  Badge,
  Fab,
  Drawer,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Divider,
  Switch,
  FormControlLabel,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
} from '@mui/material';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip as RechartsTooltip,
  Legend,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  LineChart,
  Line,
  AreaChart,
  Area,
} from 'recharts';
import {
  Refresh as RefreshIcon,
  Notifications as NotificationsIcon,
  TrendingUp as TrendingUpIcon,
  Warning as WarningIcon,
  CheckCircle as CheckCircleIcon,
  Error as ErrorIcon,
  FilterList as FilterIcon,
  Timeline as TimelineIcon,
  LocationOn as LocationIcon,
  Speed as SpeedIcon,
} from '@mui/icons-material';
import DashboardCard from '../components/DashboardCard';
import NotificationDrawer from '../components/NotificationDrawer';
import { apiService } from '../services/api';
import { DashboardStats } from '../types';
import Mapav2Img from '../assets/Mapav2.png';
import packageJson from '../../package.json';

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8', '#82ca9d', '#ffc658'];

// Definir tipo Notification localmente

type Notification = {
  id: number;
  type: 'warning' | 'error' | 'info' | 'success';
  message: string;
  time: string;
  read?: boolean;
};

const Dashboard: React.FC = () => {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [lastUpdate, setLastUpdate] = useState<Date>(new Date());
  const [notifications, setNotifications] = useState<number>(3);
  const [showFilters, setShowFilters] = useState(false);
  const [showNotifications, setShowNotifications] = useState(false);
  const [timeFilter, setTimeFilter] = useState('7d');
  const [autoRefresh, setAutoRefresh] = useState(true);
  const [alerts, setAlerts] = useState([
    { id: 1, type: 'warning', message: '5 lojas com circuitos instáveis', time: '2 min atrás' },
    { id: 2, type: 'error', message: '2 lojas offline', time: '5 min atrás' },
    { id: 3, type: 'info', message: 'Sincronização concluída', time: '10 min atrás' },
  ]);
  const [notificationList, setNotificationList] = useState<Notification[]>([
    { id: 1, type: 'warning', message: '5 lojas com circuitos instáveis', time: '2 min atrás', read: false },
    { id: 2, type: 'error', message: '2 lojas offline', time: '5 min atrás', read: false },
    { id: 3, type: 'info', message: 'Sincronização concluída', time: '10 min atrás', read: true },
    { id: 4, type: 'success', message: 'Backup automático realizado', time: '15 min atrás', read: true },
  ]);

  useEffect(() => {
    loadDashboardStats();
    
    // Auto-refresh a cada 30 segundos se habilitado
    if (autoRefresh) {
      const interval = setInterval(loadDashboardStats, 30000);
      return () => clearInterval(interval);
    }
  }, [autoRefresh]);

  const loadDashboardStats = async () => {
    try {
      setLoading(true);
      const data = await apiService.getDashboardStats();
      setStats(data);
      setLastUpdate(new Date());
      setError(null);
    } catch (err) {
      setError('Erro ao carregar estatísticas do dashboard');
      console.error('Dashboard error:', err);
    } finally {
      setLoading(false);
    }
  };

  const prepareChartData = () => {
    if (!stats) return { status: [], operadora: [], uf: [], timeline: [] };

    const statusData = Object.entries(stats.lojas_por_status).map(([status, count]) => ({
      name: status,
      value: count,
    }));

    const operadoraData = Object.entries(stats.circuitos_por_operadora).map(([operadora, count]) => ({
      name: operadora,
      value: count,
    }));

    const ufData = Object.entries(stats.lojas_por_uf)
      .sort(([, a], [, b]) => b - a)
      .slice(0, 10)
      .map(([uf, count]) => ({
        name: uf,
        value: count,
      }));

    // Dados simulados para timeline (em produção viriam do backend)
    const timelineData = [
      { date: 'Jan', lojas: 1800, circuitos: 4800 },
      { date: 'Fev', lojas: 1850, circuitos: 5000 },
      { date: 'Mar', lojas: 1900, circuitos: 5200 },
      { date: 'Abr', lojas: 1927, circuitos: 5370 },
    ];

    return { status: statusData, operadora: operadoraData, uf: ufData, timeline: timelineData };
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'ATIVA': return '#4caf50';
      case 'INATIVA': return '#f44336';
      case 'MANUTENCAO': return '#ff9800';
      default: return '#9e9e9e';
    }
  };

  const getAlertIcon = (type: string) => {
    switch (type) {
      case 'warning': return <WarningIcon color="warning" />;
      case 'error': return <ErrorIcon color="error" />;
      case 'info': return <CheckCircleIcon color="info" />;
      default: return <CheckCircleIcon color="success" />;
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress size={60} />
      </Box>
    );
  }

  if (error) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4 }}>
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      </Container>
    );
  }

  const chartData = prepareChartData();

  // Preparar dados para gráficos aprimorados
  const statusData = Object.entries(stats?.lojas_por_status || {}).map(([status, count]) => ({
    name: status,
    value: count,
    color: getStatusColor(status),
  }));

  // Top 10 UFs
  const ufDataRaw = Object.entries(stats?.lojas_por_uf || {})
    .sort(([, a], [, b]) => b - a);
  const ufData = ufDataRaw.slice(0, 10).map(([uf, count]) => ({ name: uf, value: count }));

  // Circuitos por Operadora (Top 7 + Outros)
  const operadoraDataRaw = Object.entries(stats?.circuitos_por_operadora || {})
    .sort(([, a], [, b]) => b - a);
  const topOperadoras = operadoraDataRaw.slice(0, 7);
  const outrosCount = operadoraDataRaw.slice(7).reduce((acc, [, count]) => acc + count, 0);
  const operadoraData = [
    ...topOperadoras.map(([op, count]) => ({ name: op, value: count })),
    ...(outrosCount > 0 ? [{ name: 'Outros', value: outrosCount }] : [])
  ];

  // Substituir valores fixos por dados reais do backend
  const totalLojas = stats?.total_lojas || 1;
  const ufs = stats?.lojas_por_uf ? Object.entries(stats.lojas_por_uf)
    .sort(([, a], [, b]) => b - a)
    .slice(0, 5) : [];
  const COLORS_UF = ['#2196f3', '#43a047', '#fbc02d', '#e53935', '#8e24aa'];

  // Obter informações dinâmicas do sistema
  const appVersion = packageJson.version ? `${packageJson.version} (React/TypeScript)` : 'Desconhecida';
  const buildDate = process.env.REACT_APP_BUILD_DATE || 'Desconhecida';
  const environment = process.env.NODE_ENV === 'production' ? 'Produção' : 'Desenvolvimento';

  // Calcular métricas avançadas
  const totalCircuitos = stats?.total_circuitos || 0;
  const lojasAtivas = stats?.lojas_por_status?.ATIVA || 0;
  const lojasInativas = stats?.lojas_por_status?.INATIVA || 0;
  const taxaDisponibilidade = totalLojas > 0 ? ((lojasAtivas / totalLojas) * 100).toFixed(1) : '0';
  const mediaCircuitosPorLoja = totalLojas > 0 ? (totalCircuitos / totalLojas).toFixed(1) : '0';

  return (
    <Container maxWidth="xl" sx={{ mt: 2, mb: 4, px: { xs: 1, sm: 2, md: 3 } }}>
      {/* Header com controles - Layout melhorado */}
      <Box sx={{ 
        display: 'flex', 
        justifyContent: 'space-between', 
        alignItems: 'flex-start', 
        mb: 4,
        flexDirection: { xs: 'column', md: 'row' },
        gap: 2
      }}>
        <Box sx={{ flex: 1 }}>
          <Typography 
            variant="h3" 
            component="h1" 
            fontWeight="bold" 
            align="left"
            sx={{ 
              fontSize: { xs: '1.8rem', sm: '2.2rem', md: '2.5rem' },
              background: 'linear-gradient(45deg, #2196F3, #21CBF3)',
              backgroundClip: 'text',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              mb: 0.5
            }}
          >
            📊 COMMAND CENTER
          </Typography>
          <Typography 
            variant="body2" 
            color="textSecondary" 
            align="left"
            sx={{ 
              fontSize: { xs: '0.8rem', sm: '0.9rem' },
              opacity: 0.8
            }}
          >
            Última atualização: {lastUpdate.toLocaleTimeString()}
          </Typography>
        </Box>
        
        <Box sx={{ 
          display: 'flex', 
          gap: 1, 
          alignItems: 'center',
          flexWrap: 'wrap',
          justifyContent: { xs: 'center', md: 'flex-end' }
        }}>
          <FormControlLabel
            control={
              <Switch
                checked={autoRefresh}
                onChange={(e) => setAutoRefresh(e.target.checked)}
                size="small"
              />
            }
            label="Auto-refresh"
            sx={{ fontSize: '0.8rem' }}
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
              <FilterIcon />
            </IconButton>
          </Tooltip>
          
          <Tooltip title="Atualizar">
            <IconButton 
              onClick={loadDashboardStats} 
              disabled={loading}
              sx={{
                animation: loading ? 'spin 1s linear infinite' : 'none',
                '@keyframes spin': {
                  '0%': { transform: 'rotate(0deg)' },
                  '100%': { transform: 'rotate(360deg)' }
                }
              }}
            >
              <RefreshIcon />
            </IconButton>
          </Tooltip>
          
          <Badge badgeContent={notifications} color="error">
            <Tooltip title="Notificações">
              <IconButton 
                onClick={() => setShowNotifications(true)}
                sx={{
                  '&:hover': {
                    transform: 'scale(1.1)',
                    transition: 'transform 0.2s ease'
                  }
                }}
              >
                <NotificationsIcon />
              </IconButton>
            </Tooltip>
          </Badge>
        </Box>
      </Box>

      {/* Alertas em tempo real - Layout melhorado */}
      {alerts.length > 0 && (
        <Box sx={{ 
          mb: 4,
          p: 2,
          bgcolor: 'background.paper',
          borderRadius: 3,
          boxShadow: 2,
          border: '1px solid',
          borderColor: 'divider'
        }}>
          <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            ⚠️ Alertas do Sistema
          </Typography>
          <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
            {alerts.map((alert) => (
              <Chip
                key={alert.id}
                icon={getAlertIcon(alert.type)}
                label={`${alert.message} (${alert.time})`}
                variant="outlined"
                color={alert.type === 'error' ? 'error' : alert.type === 'warning' ? 'warning' : 'info'}
                sx={{ 
                  mb: 1,
                  '&:hover': {
                    transform: 'translateY(-2px)',
                    boxShadow: 2,
                    transition: 'all 0.2s ease'
                  }
                }}
              />
            ))}
          </Box>
        </Box>
      )}

      {/* Filtros - Layout melhorado */}
      {showFilters && (
        <Paper sx={{ 
          p: 3, 
          mb: 4, 
          borderRadius: 3,
          boxShadow: 3,
          bgcolor: 'background.paper',
          border: '1px solid',
          borderColor: 'divider'
        }}>
          <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            🔧 Filtros
          </Typography>
          <Grid container spacing={2} alignItems="center">
            <Grid item xs={12} sm={6} md={3}>
              <FormControl fullWidth size="small">
                <InputLabel>Período</InputLabel>
                <Select
                  value={timeFilter}
                  onChange={(e) => setTimeFilter(e.target.value)}
                  label="Período"
                >
                  <MenuItem value="1d">Últimas 24h</MenuItem>
                  <MenuItem value="7d">Últimos 7 dias</MenuItem>
                  <MenuItem value="30d">Últimos 30 dias</MenuItem>
                  <MenuItem value="90d">Últimos 90 dias</MenuItem>
                </Select>
              </FormControl>
            </Grid>
          </Grid>
        </Paper>
      )}
      
      <Typography 
        variant="body1" 
        color="textSecondary" 
        sx={{ 
          mb: 4, 
          textAlign: 'center',
          fontSize: '1.1rem',
          opacity: 0.8
        }}
      >
        Visão geral do sistema de consulta de lojas, circuitos e inventário
      </Typography>

      {/* Painel Infográfico - Layout melhorado */}
      <Box sx={{ 
        my: 4, 
        p: { xs: 2, md: 4 }, 
        bgcolor: 'background.paper', 
        borderRadius: 4, 
        boxShadow: 4,
        border: '1px solid',
        borderColor: 'divider',
        background: 'linear-gradient(135deg, rgba(33, 150, 243, 0.05) 0%, rgba(33, 203, 243, 0.05) 100%)'
      }}>
        <Typography 
          variant="h5" 
          gutterBottom 
          fontWeight={900} 
          fontSize={{ xs: 24, md: 28 }} 
          color="primary.main" 
          align="center"
          sx={{ mb: 2 }}
        >
          🗺️ Distribuição Geográfica das Lojas
        </Typography>
        <Typography 
          variant="body1" 
          color="text.secondary" 
          mb={4} 
          align="center"
          sx={{ fontSize: '1rem', opacity: 0.8 }}
        >
          Visualização aproximada das regiões/estados com maior concentração de lojas.
        </Typography>
        <Box 
          display="flex" 
          flexWrap="wrap" 
          justifyContent="center" 
          alignItems="center" 
          gap={{ xs: 2, md: 3 }} 
          mb={3}
        >
          {ufs.map(([uf, count], idx) => (
            <Box key={uf} sx={{
              bgcolor: 'background.default',
              borderRadius: 4,
              boxShadow: 3,
              p: { xs: 1.5, md: 2 },
              minWidth: { xs: 100, md: 120 },
              minHeight: { xs: 120, md: 150 },
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              justifyContent: 'center',
              position: 'relative',
              transition: 'all 0.3s ease',
              animation: `fadeIn 0.7s ${idx * 0.1 + 0.2}s both`,
              '&:hover': {
                transform: 'translateY(-8px) scale(1.05)',
                boxShadow: 8,
                '& .progress-circle': {
                  transform: 'scale(1.1)',
                }
              },
              '@keyframes fadeIn': {
                from: { opacity: 0, transform: 'translateY(20px)' },
                to: { opacity: 1, transform: 'none' }
              }
            }}>
              <Box position="relative" mb={1} className="progress-circle">
                <CircularProgress 
                  variant="determinate" 
                  value={Math.round((Number(count) / totalLojas) * 100)} 
                  size={{ xs: 60, md: 70 }} 
                  thickness={6} 
                  sx={{ 
                    color: COLORS_UF[idx % COLORS_UF.length], 
                    bgcolor: COLORS_UF[idx % COLORS_UF.length] + '22', 
                    borderRadius: '50%', 
                    boxShadow: 3,
                    transition: 'transform 0.3s ease'
                  }} 
                />
                <Typography 
                  variant="h5" 
                  fontWeight={900} 
                  position="absolute" 
                  top={{ xs: 15, md: 18 }} 
                  left={0} 
                  right={0} 
                  textAlign="center" 
                  color={COLORS_UF[idx % COLORS_UF.length]}
                  sx={{ fontSize: { xs: '1.2rem', md: '1.5rem' } }}
                >
                  {Math.round((Number(count) / totalLojas) * 100)}%
                </Typography>
              </Box>
              <Typography 
                variant="subtitle2" 
                fontWeight={700} 
                color={COLORS_UF[idx % COLORS_UF.length]} 
                textAlign="center" 
                sx={{ 
                  textShadow: '0 1px 2px #0006',
                  fontSize: { xs: '0.9rem', md: '1rem' }
                }}
              >
                {uf}
              </Typography>
            </Box>
          ))}
        </Box>
      </Box>

      {/* Cards principais com métricas avançadas - Layout melhorado */}
      <Grid container spacing={{ xs: 2, md: 3 }} sx={{ mb: 5 }}>
        <Grid item xs={12} sm={6} md={3}>
          {loading ? (
            <Skeleton variant="rectangular" height={160} sx={{ borderRadius: 3 }} />
          ) : (
            <DashboardCard
              title="Total de Lojas"
              value={stats?.total_lojas.toLocaleString() || '0'}
              icon="🏪"
              color="primary"
              trend={{ value: 5, isPositive: true }}
              subtitle={`${taxaDisponibilidade}% disponíveis`}
            />
          )}
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          {loading ? (
            <Skeleton variant="rectangular" height={160} sx={{ borderRadius: 3 }} />
          ) : (
            <DashboardCard
              title="Total de Circuitos"
              value={stats?.total_circuitos.toLocaleString() || '0'}
              icon="🔗"
              color="success"
              trend={{ value: 12, isPositive: true }}
              subtitle={`${mediaCircuitosPorLoja} por loja`}
            />
          )}
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          {loading ? (
            <Skeleton variant="rectangular" height={160} sx={{ borderRadius: 3 }} />
          ) : (
            <DashboardCard
              title="Lojas Ativas"
              value={stats?.lojas_por_status.ATIVA?.toLocaleString() || '0'}
              icon="🟢"
              color="success"
              subtitle="Operacionais"
            />
          )}
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          {loading ? (
            <Skeleton variant="rectangular" height={160} sx={{ borderRadius: 3 }} />
          ) : (
            <DashboardCard
              title="Lojas Inativas"
              value={stats?.lojas_por_status.INATIVA?.toLocaleString() || '0'}
              icon="🔴"
              color="error"
              subtitle="Fora de operação"
            />
          )}
        </Grid>
      </Grid>

      {/* Gráficos interativos - Layout melhorado */}
      <Grid container spacing={{ xs: 2, md: 3 }} sx={{ mb: 5 }}>
        {/* Gráfico de linha - Evolução temporal */}
        <Grid item xs={12} lg={8}>
          <Paper sx={{ 
            p: { xs: 2, md: 3 }, 
            height: { xs: 350, md: 400 },
            borderRadius: 3,
            boxShadow: 3,
            border: '1px solid',
            borderColor: 'divider'
          }}>
            <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              📈 Evolução Temporal
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={chartData.timeline}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                <XAxis dataKey="date" stroke="rgba(255,255,255,0.7)" />
                <YAxis stroke="rgba(255,255,255,0.7)" />
                <RechartsTooltip 
                  contentStyle={{
                    backgroundColor: 'rgba(0,0,0,0.8)',
                    border: 'none',
                    borderRadius: 8,
                    color: 'white'
                  }}
                />
                <Legend />
                <Line 
                  type="monotone" 
                  dataKey="lojas" 
                  stroke="#2196f3" 
                  strokeWidth={3}
                  dot={{ fill: '#2196f3', strokeWidth: 2, r: 6 }}
                  activeDot={{ r: 8 }}
                />
                <Line 
                  type="monotone" 
                  dataKey="circuitos" 
                  stroke="#4caf50" 
                  strokeWidth={3}
                  dot={{ fill: '#4caf50', strokeWidth: 2, r: 6 }}
                  activeDot={{ r: 8 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        {/* Gráfico de pizza - Status das lojas */}
        <Grid item xs={12} lg={4}>
          <Paper sx={{ 
            p: { xs: 2, md: 3 }, 
            height: { xs: 350, md: 400 },
            borderRadius: 3,
            boxShadow: 3,
            border: '1px solid',
            borderColor: 'divider'
          }}>
            <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              🍕 Status das Lojas
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={statusData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {statusData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <RechartsTooltip 
                  contentStyle={{
                    backgroundColor: 'rgba(0,0,0,0.8)',
                    border: 'none',
                    borderRadius: 8,
                    color: 'white'
                  }}
                />
              </PieChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        {/* Gráfico de barras - Top UFs */}
        <Grid item xs={12} lg={6}>
          <Paper sx={{ 
            p: { xs: 2, md: 3 }, 
            height: { xs: 350, md: 400 },
            borderRadius: 3,
            boxShadow: 3,
            border: '1px solid',
            borderColor: 'divider'
          }}>
            <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              📊 Top 10 Estados
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={ufData}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                <XAxis dataKey="name" stroke="rgba(255,255,255,0.7)" />
                <YAxis stroke="rgba(255,255,255,0.7)" />
                <RechartsTooltip 
                  contentStyle={{
                    backgroundColor: 'rgba(0,0,0,0.8)',
                    border: 'none',
                    borderRadius: 8,
                    color: 'white'
                  }}
                />
                <Bar dataKey="value" fill="#8884d8" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        {/* Gráfico de área - Operadoras */}
        <Grid item xs={12} lg={6}>
          <Paper sx={{ 
            p: { xs: 2, md: 3 }, 
            height: { xs: 350, md: 400 },
            borderRadius: 3,
            boxShadow: 3,
            border: '1px solid',
            borderColor: 'divider'
          }}>
            <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              🌐 Circuitos por Operadora
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <AreaChart data={operadoraData}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                <XAxis dataKey="name" stroke="rgba(255,255,255,0.7)" />
                <YAxis stroke="rgba(255,255,255,0.7)" />
                <RechartsTooltip 
                  contentStyle={{
                    backgroundColor: 'rgba(0,0,0,0.8)',
                    border: 'none',
                    borderRadius: 8,
                    color: 'white'
                  }}
                />
                <Area 
                  type="monotone" 
                  dataKey="value" 
                  stroke="#8884d8" 
                  fill="#8884d8" 
                  fillOpacity={0.6}
                />
              </AreaChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>
      </Grid>

      {/* Informações do Sistema - Layout melhorado */}
      <Paper sx={{ 
        p: { xs: 2, md: 3 }, 
        mt: 3, 
        bgcolor: 'background.paper', 
        color: 'text.primary',
        borderRadius: 3,
        boxShadow: 3,
        border: '1px solid',
        borderColor: 'divider',
        background: 'linear-gradient(135deg, rgba(76, 175, 80, 0.05) 0%, rgba(33, 150, 243, 0.05) 100%)'
      }}>
        <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          ℹ️ Informações do Sistema
        </Typography>
        <Grid container spacing={2}>
          <Grid item xs={12} sm={6} md={3}>
            <Typography variant="body2" color="textSecondary">
              Versão: {appVersion}
            </Typography>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Typography variant="body2" color="textSecondary">
              Última atualização: {lastUpdate.toLocaleString()}
            </Typography>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Typography variant="body2" color="textSecondary">
              Ambiente: {environment}
            </Typography>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Typography variant="body2" color="textSecondary">
              Status: <Chip label="Online" color="success" size="small" />
            </Typography>
          </Grid>
        </Grid>
      </Paper>

      {/* FAB para ações rápidas - Layout melhorado */}
      <Fab
        color="primary"
        aria-label="add"
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
        onClick={loadDashboardStats}
      >
        <RefreshIcon />
      </Fab>

      {/* Drawer de Notificações */}
      <NotificationDrawer
        open={showNotifications}
        onClose={() => setShowNotifications(false)}
        notifications={notificationList}
        onMarkAsRead={(id) => {
          setNotificationList(prev => 
            prev.map(n => n.id === id ? { ...n, read: true } : n)
          );
          setNotifications(prev => Math.max(0, prev - 1));
        }}
      />
    </Container>
  );
};

export default Dashboard; 