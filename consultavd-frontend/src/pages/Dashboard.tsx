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
} from '@mui/material';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from 'recharts';
import DashboardCard from '../components/DashboardCard';
import { apiService } from '../services/api';
import { DashboardStats } from '../types';
import Mapav2Img from '../assets/Mapav2.png';
import packageJson from '../../package.json';

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8'];

const Dashboard: React.FC = () => {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadDashboardStats();
  }, []);

  const loadDashboardStats = async () => {
    try {
      setLoading(true);
      const data = await apiService.getDashboardStats();
      setStats(data);
      setError(null);
    } catch (err) {
      setError('Erro ao carregar estatísticas do dashboard');
      console.error('Dashboard error:', err);
    } finally {
      setLoading(false);
    }
  };

  const prepareChartData = () => {
    if (!stats) return { status: [], operadora: [], uf: [] };

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

    return { status: statusData, operadora: operadoraData, uf: ufData };
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

  return (
    <Container maxWidth="xl" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom fontWeight="bold" align="center">
        📊 COMMAND CENTER
      </Typography>
      
      <Typography variant="body1" color="textSecondary" sx={{ mb: 4 }} align="center">
        Visão geral do sistema de consulta de lojas, circuitos e inventário
      </Typography>

      {/* Painel Infográfico - Mapa do Brasil com Indicadores e Imagem */}
      <Box sx={{ my: 4, p: { xs: 1, md: 3 }, bgcolor: 'background.paper', borderRadius: 4, boxShadow: 6 }}>
        <Typography variant="h5" gutterBottom fontWeight={900} fontSize={28} color="primary.main" align="center">
          🗺️ Distribuição Geográfica das Lojas
        </Typography>
        <Typography variant="body1" color="text.secondary" mb={3} align="center">
          Visualização aproximada das regiões/estados com maior concentração de lojas.
        </Typography>
        <Box display="flex" flexWrap="wrap" justifyContent="center" alignItems="center" gap={3} mb={3}>
          {ufs.map(([uf, count], idx) => (
            <Box key={uf} sx={{
              bgcolor: 'background.default',
              borderRadius: 3,
              boxShadow: 4,
              p: 2,
              minWidth: 110,
              minHeight: 140,
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              justifyContent: 'center',
              position: 'relative',
              transition: 'box-shadow 0.3s',
              animation: `fadeIn 0.7s ${idx * 0.1 + 0.2}s both`,
              '@keyframes fadeIn': {
                from: { opacity: 0, transform: 'translateY(20px)' },
                to: { opacity: 1, transform: 'none' }
              }
            }}>
              <Box position="relative" mb={1}>
                <CircularProgress variant="determinate" value={Math.round((Number(count) / totalLojas) * 100)} size={70} thickness={6} sx={{ color: COLORS_UF[idx % COLORS_UF.length], bgcolor: COLORS_UF[idx % COLORS_UF.length] + '22', borderRadius: '50%', boxShadow: 2 }} />
                <Typography variant="h5" fontWeight={900} position="absolute" top={18} left={0} right={0} textAlign="center" color={COLORS_UF[idx % COLORS_UF.length]}>{Math.round((Number(count) / totalLojas) * 100)}%</Typography>
              </Box>
              <Typography variant="subtitle2" fontWeight={700} color={COLORS_UF[idx % COLORS_UF.length]} textAlign="center" sx={{ textShadow: '0 1px 2px #0006' }}>{uf}</Typography>
            </Box>
          ))}
        </Box>
      </Box>

      {/* Cards principais */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          {loading ? (
            <Skeleton variant="rectangular" height={140} sx={{ borderRadius: 3 }} />
          ) : (
            <DashboardCard
              title="Total de Lojas"
              value={stats?.total_lojas.toLocaleString() || '0'}
              icon="🏪"
              color="primary"
              trend={{ value: 5, isPositive: true }}
            />
          )}
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          {loading ? (
            <Skeleton variant="rectangular" height={140} sx={{ borderRadius: 3 }} />
          ) : (
            <DashboardCard
              title="Total de Circuitos"
              value={stats?.total_circuitos.toLocaleString() || '0'}
              icon="🔗"
              color="success"
              trend={{ value: 12, isPositive: true }}
            />
          )}
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          {loading ? (
            <Skeleton variant="rectangular" height={140} sx={{ borderRadius: 3 }} />
          ) : (
            <DashboardCard
              title="Lojas Ativas"
              value={stats?.lojas_por_status.ATIVA?.toLocaleString() || '0'}
              icon="🟢"
              color="success"
            />
          )}
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          {loading ? (
            <Skeleton variant="rectangular" height={140} sx={{ borderRadius: 3 }} />
          ) : (
            <DashboardCard
              title="Lojas Inativas"
              value={stats?.lojas_por_status.INATIVA?.toLocaleString() || '0'}
              icon="🔴"
              color="error"
            />
          )}
        </Grid>
      </Grid>

      {/* Gráficos */}
      <Grid container spacing={3} sx={{ mt: 1 }}>
        {/* Remover todos os gráficos do dashboard */}
      </Grid>

      {/* Informações do Sistema */}
      <Paper sx={{ p: 3, mt: 3, bgcolor: 'background.paper', color: 'text.primary' }}>
        <Typography variant="h6" gutterBottom>
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
              Última atualização: {buildDate}
            </Typography>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Typography variant="body2" color="textSecondary">
              Ambiente: {environment}
            </Typography>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Typography variant="body2" color="textSecondary">
              Status: Online
            </Typography>
          </Grid>
        </Grid>
      </Paper>
    </Container>
  );
};

export default Dashboard; 