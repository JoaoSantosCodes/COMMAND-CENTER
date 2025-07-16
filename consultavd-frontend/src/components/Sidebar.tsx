import React, { useContext } from 'react';
import { Drawer, List, ListItem, ListItemIcon, ListItemText, Toolbar, Divider, Box, Switch, Typography } from '@mui/material';
import DashboardIcon from '@mui/icons-material/Dashboard';
import SearchIcon from '@mui/icons-material/Search';
import EditIcon from '@mui/icons-material/Edit';
import TableChartIcon from '@mui/icons-material/TableChart';
import StorageIcon from '@mui/icons-material/Storage';
import HelpIcon from '@mui/icons-material/Help';
import InfoIcon from '@mui/icons-material/Info';
import TuneIcon from '@mui/icons-material/Tune';
import AssignmentIcon from '@mui/icons-material/Assignment';
import HistoryIcon from '@mui/icons-material/History';
import Brightness4Icon from '@mui/icons-material/Brightness4';
import Brightness7Icon from '@mui/icons-material/Brightness7';
import MenuBookIcon from '@mui/icons-material/MenuBook';
import { Link, useLocation } from 'react-router-dom';
import { ColorModeContext } from '../ThemeProvider';

const drawerWidth = 240;

const menuItems = [
  { text: 'Dashboard', icon: <DashboardIcon />, path: '/dashboard' },
  { text: 'Busca Unificada', icon: <SearchIcon />, path: '/busca-unificada' },
  { text: 'Avançados', icon: <HistoryIcon />, path: '/avancados' },
  { text: 'Edição de Dados', icon: <EditIcon />, path: '/edicao-dados' },
  { text: 'Auditoria', icon: <AssignmentIcon />, path: '/auditoria' },
  { text: 'Visualizar Tabelas', icon: <TableChartIcon />, path: '/visualizar-tabelas' },
  { text: 'Consulta SQL Customizada', icon: <StorageIcon />, path: '/consulta-sql' },
  { text: 'Gerenciamento de Cache', icon: <TuneIcon />, path: '/gerenciamento-cache' },
  { text: 'Documentação', icon: <MenuBookIcon />, path: '/documentacao' },
  { text: 'Ajuda', icon: <HelpIcon />, path: '/ajuda' },
  { text: 'Sobre', icon: <InfoIcon />, path: '/sobre' },
];

const Sidebar: React.FC = () => {
  const location = useLocation();
  const colorMode = useContext(ColorModeContext) as { toggleColorMode: () => void; mode: 'light' | 'dark' };
  const isDark = colorMode.mode === 'dark';
  return (
    <Drawer
      variant="permanent"
      sx={{
        width: drawerWidth,
        flexShrink: 0,
        [`& .MuiDrawer-paper`]: { width: drawerWidth, boxSizing: 'border-box' },
      }}
    >
      <Toolbar />
      <Box display="flex" alignItems="center" justifyContent="center" px={2} py={1}>
        <Brightness7Icon color={isDark ? 'disabled' : 'primary'} />
        <Switch
          checked={isDark}
          onChange={colorMode.toggleColorMode}
          color="default"
          inputProps={{ 'aria-label': 'Alternar tema escuro' }}
        />
        <Brightness4Icon color={isDark ? 'primary' : 'disabled'} />
      </Box>
      <Divider />
      <List>
        {menuItems.map((item) => (
          <ListItem
            button
            key={item.text}
            component={Link}
            to={item.path}
            selected={location.pathname === item.path}
          >
            <ListItemIcon>{item.icon}</ListItemIcon>
            <ListItemText primary={item.text} />
          </ListItem>
        ))}
      </List>
    </Drawer>
  );
};

export default Sidebar; 