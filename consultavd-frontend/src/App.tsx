import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { Box, Container } from '@mui/material';
import Dashboard from './pages/Dashboard';
import BuscaUnificada from './pages/BuscaUnificada';
import Lojas from './pages/Lojas';
import Avancados from './pages/Avancados';
import Documentacao from './pages/Documentacao';
import Ajuda from './pages/Ajuda';
import Sobre from './pages/Sobre';
import GerenciamentoCache from './pages/GerenciamentoCache';
import ConsultaSQL from './pages/ConsultaSQL';
import VisualizarTabelas from './pages/VisualizarTabelas';
import Auditoria from './pages/Auditoria';
import EdicaoDados from './pages/EdicaoDados';
// Placeholders para as demais páginas

function App() {
  return (
    <Box sx={{ minHeight: '100vh', backgroundColor: 'background.default' }}>
      <Container maxWidth="xl" sx={{ py: 2 }}>
        <Routes>
          <Route path="/" element={<Navigate to="/dashboard" />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/busca-unificada" element={<BuscaUnificada />} />
          <Route path="/lojas" element={<Lojas />} />
          <Route path="/edicao-dados" element={<EdicaoDados />} />
          <Route path="/auditoria" element={<Auditoria />} />
          <Route path="/visualizar-tabelas" element={<VisualizarTabelas />} />
          <Route path="/consulta-sql" element={<ConsultaSQL />} />
          <Route path="/gerenciamento-cache" element={<GerenciamentoCache />} />
          <Route path="/documentacao" element={<Documentacao />} />
          <Route path="/ajuda" element={<Ajuda />} />
          <Route path="/sobre" element={<Sobre />} />
          <Route path="/avancados" element={<Avancados />} />
        </Routes>
      </Container>
    </Box>
  );
}

export default App; 