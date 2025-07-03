import React, { useState, useEffect } from 'react';
import {
  Box,
  Grid,
  Typography,
  Paper,
  CircularProgress,
  Alert,
  Container,
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

  return (
    <Container maxWidth="xl" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom fontWeight="bold">
        📊 Dashboard - ConsultaVD
      </Typography>
      
      <Typography variant="body1" color="textSecondary" sx={{ mb: 4 }}>
        Visão geral do sistema de consulta de lojas, circuitos e inventário
      </Typography>

      {/* Painel Infográfico - Mapa do Brasil com Indicadores e Imagem */}
      <Box sx={{ my: 4, p: { xs: 1, md: 3 }, bgcolor: 'background.paper', borderRadius: 4, boxShadow: 6 }}>
        <Typography variant="h5" gutterBottom fontWeight={900} fontSize={28} color="primary.main">
          🗺️ Distribuição Geográfica das Lojas
        </Typography>
        <Typography variant="body1" color="text.secondary" mb={3}>
          Visualização aproximada das regiões com maior concentração de lojas.
        </Typography>
        <Box display="flex" flexWrap="wrap" justifyContent="center" alignItems="center" gap={3} mb={3}>
          {[{ label: 'SÃO PAULO', value: 85, color: '#2196f3' }, { label: 'MINAS GERAIS', value: 60, color: '#43a047' }, { label: 'RIO DE JANEIRO', value: 40, color: '#fbc02d' }, { label: 'PARANÁ', value: 25, color: '#e53935' }, { label: 'OUTROS', value: 15, color: '#8e24aa' }].map((item, idx) => (
            <Box key={item.label} sx={{
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
                <CircularProgress variant="determinate" value={item.value} size={70} thickness={6} sx={{ color: item.color, bgcolor: item.color + '22', borderRadius: '50%', boxShadow: 2 }} />
                <Typography variant="h5" fontWeight={900} position="absolute" top={18} left={0} right={0} textAlign="center" color={item.color}>{item.value}%</Typography>
              </Box>
              <Typography variant="subtitle2" fontWeight={700} color={item.color} textAlign="center" sx={{ textShadow: '0 1px 2px #0006' }}>{item.label}</Typography>
            </Box>
          ))}
        </Box>
        <Box display="flex" justifyContent="center">
          <Box sx={{ width: '100%', maxWidth: 420, height: 350, position: 'relative', borderRadius: 3, overflow: 'hidden', boxShadow: 3, mx: 'auto', bgcolor: '#23272f' }}>
            <img src={Mapav2Img} alt="Mapa do Brasil" style={{ width: '100%', height: '100%', objectFit: 'cover', filter: 'brightness(0.98) contrast(1.1)' }} />
            {/* Marcadores coloridos - cores padronizadas conforme os cards, sem OUTROS */}
            <Box sx={{ position: 'absolute', top: '68%', left: '56%' }}><Box width={24} height={24} bgcolor="#2196f3" borderRadius={12} border="3px solid #fff" boxShadow={6} sx={{ boxShadow: '0 0 12px 4px #2196f388' }} /></Box> {/* SP - azul */}
            <Box sx={{ position: 'absolute', top: '58%', left: '62%' }}><Box width={24} height={24} bgcolor="#43a047" borderRadius={12} border="3px solid #fff" boxShadow={6} sx={{ boxShadow: '0 0 12px 4px #43a04788' }} /></Box> {/* MG - verde */}
            <Box sx={{ position: 'absolute', top: '70%', left: '67%' }}><Box width={24} height={24} bgcolor="#fbc02d" borderRadius={12} border="3px solid #fff" boxShadow={6} sx={{ boxShadow: '0 0 12px 4px #fbc02d88' }} /></Box> {/* RJ - amarelo */}
            <Box sx={{ position: 'absolute', top: '80%', left: '53%' }}><Box width={24} height={24} bgcolor="#e53935" borderRadius={12} border="3px solid #fff" boxShadow={6} sx={{ boxShadow: '0 0 12px 4px #e5393588' }} /></Box> {/* PR - vermelho */}
          </Box>
        </Box>
      </Box>

      {/* Cards principais */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <DashboardCard
            title="Total de Lojas"
            value={stats?.total_lojas.toLocaleString() || '0'}
            icon="🏪"
            color="primary"
            trend={{ value: 5, isPositive: true }}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <DashboardCard
            title="Total de Circuitos"
            value={stats?.total_circuitos.toLocaleString() || '0'}
            icon="🔗"
            color="success"
            trend={{ value: 12, isPositive: true }}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <DashboardCard
            title="Lojas Ativas"
            value={stats?.lojas_por_status.ATIVA?.toLocaleString() || '0'}
            icon="🟢"
            color="success"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <DashboardCard
            title="Lojas Inativas"
            value={stats?.lojas_por_status.INATIVA?.toLocaleString() || '0'}
            icon="🔴"
            color="error"
          />
        </Grid>
      </Grid>

      {/* Painel de Mapa de Lojas */}
      <Box sx={{ my: 4 }}>
        <Typography variant="h6" gutterBottom>
          🗺️ Mapa de Lojas (visualização geral)
        </Typography>
        <Box sx={{ width: '100%', height: { xs: 300, md: 400 }, borderRadius: 3, overflow: 'hidden', boxShadow: 3 }}>
          <iframe
            title="Mapa de Lojas"
            width="100%"
            height="100%"
            style={{ border: 0 }}
            loading="lazy"
            allowFullScreen
            referrerPolicy="no-referrer-when-downgrade"
            src="https://www.google.com/maps/embed/v1/view?key=AIzaSyB8JXj4jYlqW6MpppD24XB7x2Ef5oWdJxw&center=-23.55052,-46.633308&zoom=10"
          />
        </Box>
        <Typography variant="body2" color="text.secondary" mt={1}>
          * Mapa centralizado em São Paulo/SP. Para ver o endereço de uma loja específica, clique no ícone de mapa na lista de lojas.
        </Typography>
      </Box>

      {/* Gráficos */}
      <Grid container spacing={3}>
        {/* Gráfico de Pizza - Status das Lojas */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3, height: 400, bgcolor: 'background.paper', color: 'text.primary' }}>
            <Typography variant="h6" gutterBottom>
              📈 Distribuição por Status
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={chartData.status}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {chartData.status.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        {/* Gráfico de Barras - Circuitos por Operadora */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3, height: 400, bgcolor: 'background.paper', color: 'text.primary' }}>
            <Typography variant="h6" gutterBottom>
              📡 Circuitos por Operadora
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={chartData.operadora}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="value" fill="#8884d8" />
              </BarChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        {/* Gráfico de Barras - Top 10 Lojas por UF */}
        <Grid item xs={12}>
          <Paper sx={{ p: 3, height: 400, bgcolor: 'background.paper', color: 'text.primary' }}>
            <Typography variant="h6" gutterBottom>
              🗺️ Top 10 - Lojas por UF
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={chartData.uf} layout="horizontal">
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis type="number" />
                <YAxis dataKey="name" type="category" width={80} />
                <Tooltip />
                <Legend />
                <Bar dataKey="value" fill="#82ca9d" />
              </BarChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>
      </Grid>

      {/* Informações do Sistema */}
      <Paper sx={{ p: 3, mt: 3, bgcolor: 'background.paper', color: 'text.primary' }}>
        <Typography variant="h6" gutterBottom>
          ℹ️ Informações do Sistema
        </Typography>
        <Grid container spacing={2}>
          <Grid item xs={12} sm={6} md={3}>
            <Typography variant="body2" color="textSecondary">
              Versão: 2.0 (React/TypeScript)
            </Typography>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Typography variant="body2" color="textSecondary">
              Última atualização: {new Date().toLocaleString('pt-BR')}
            </Typography>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Typography variant="body2" color="textSecondary">
              Ambiente: Desenvolvimento
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