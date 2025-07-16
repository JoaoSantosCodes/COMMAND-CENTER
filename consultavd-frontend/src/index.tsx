import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import Sidebar from './components/Sidebar';
import { Box } from '@mui/material';
import { BrowserRouter as Router } from 'react-router-dom';
import { CustomThemeProvider } from './ThemeProvider';
import './index.css';

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);

root.render(
  <React.StrictMode>
    <CustomThemeProvider>
      <Router>
        <Box sx={{ display: 'flex' }}>
          <Sidebar />
          <Box component="main" sx={{ flexGrow: 1 }}>
            <App />
          </Box>
        </Box>
      </Router>
    </CustomThemeProvider>
  </React.StrictMode>
); 