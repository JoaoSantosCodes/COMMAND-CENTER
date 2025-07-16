import React, { useState } from 'react';
import {
  DataGrid,
  GridColDef,
  GridValueGetterParams,
  GridActionsCellItem,
  GridRowParams,
  GridToolbar,
  GridPaginationModel,
  GridFilterModel,
  GridSortModel,
  GridRowsProp,
  ptBR,
} from '@mui/x-data-grid';
import {
  Edit as EditIcon,
  Delete as DeleteIcon,
  Visibility as ViewIcon,
  Download as ExportIcon,
} from '@mui/icons-material';
import { Box, Chip, IconButton, Tooltip, useTheme, Paper } from '@mui/material';
import { TableColumn } from '../types';

interface DataTableProps {
  rows: GridRowsProp;
  columns: GridColDef[];
  loading?: boolean;
  onEdit?: (id: number) => void;
  onDelete?: (id: number) => void;
  onView?: (id: number) => void;
  onExport?: () => void;
  pagination?: {
    page: number;
    pageSize: number;
    total: number;
  };
  onPaginationChange?: (model: GridPaginationModel) => void;
  onFilterChange?: (model: GridFilterModel) => void;
  onSortChange?: (model: GridSortModel) => void;
  height?: number | string;
  pageSize?: number;
}

const DataTable: React.FC<DataTableProps> = ({
  rows,
  columns,
  loading = false,
  onEdit,
  onDelete,
  onView,
  onExport,
  pagination,
  onPaginationChange,
  onFilterChange,
  onSortChange,
  height = 400,
  pageSize = 10,
}) => {
  const theme = useTheme();
  const [paginationModel, setPaginationModel] = useState<GridPaginationModel>({
    page: 0,
    pageSize: pageSize,
  });

  const handlePaginationChange = (model: GridPaginationModel) => {
    setPaginationModel(model);
    onPaginationChange?.(model);
  };

  // Converter colunas para o formato do DataGrid
  const gridColumns: GridColDef[] = columns.map((col) => ({
    field: col.field,
    headerName: col.headerName,
    width: col.width || 150,
    sortable: col.sortable !== false,
    filterable: col.filterable !== false,
    renderCell: col.renderCell,
    type: 'string',
  }));

  // Adicionar coluna de ações se necessário
  if (onEdit || onDelete || onView) {
    gridColumns.push({
      field: 'actions',
      type: 'actions',
      headerName: 'Ações',
      width: 120,
      getActions: (params: GridRowParams) => [
        ...(onView ? [
          <GridActionsCellItem
            icon={
              <Tooltip title="Visualizar">
                <IconButton size="small" color="primary">
                  <ViewIcon />
                </IconButton>
              </Tooltip>
            }
            label="Visualizar"
            onClick={() => onView(params.row.id)}
          />
        ] : []),
        ...(onEdit ? [
          <GridActionsCellItem
            icon={
              <Tooltip title="Editar">
                <IconButton size="small" color="secondary">
                  <EditIcon />
                </IconButton>
              </Tooltip>
            }
            label="Editar"
            onClick={() => onEdit(params.row.id)}
          />
        ] : []),
        ...(onDelete ? [
          <GridActionsCellItem
            icon={
              <Tooltip title="Excluir">
                <IconButton size="small" color="error">
                  <DeleteIcon />
                </IconButton>
              </Tooltip>
            }
            label="Excluir"
            onClick={() => onDelete(params.row.id)}
          />
        ] : []),
      ],
    });
  }

  // Adicionar botão de exportação se necessário
  if (onExport) {
    gridColumns.push({
      field: 'export',
      type: 'actions',
      headerName: 'Exportar',
      width: 100,
      getActions: () => [
        <GridActionsCellItem
          icon={
            <Tooltip title="Exportar">
              <IconButton size="small" color="success">
                <ExportIcon />
              </IconButton>
            </Tooltip>
          }
          label="Exportar"
          onClick={onExport}
        />,
      ],
    });
  }

  return (
    <Paper
      sx={{
        p: { xs: 1, md: 2 },
        borderRadius: 3,
        boxShadow: 6,
        bgcolor: 'background.paper',
        color: 'text.primary',
        mb: 2,
        transition: 'box-shadow 0.3s, transform 0.3s',
        '&:hover': {
          boxShadow: 12,
          transform: 'translateY(-2px) scale(1.01)',
        },
      }}
    >
      <Box sx={{ width: '100%', height }}>
        <DataGrid
          columns={gridColumns}
          rows={rows}
          loading={loading}
          pagination
          paginationModel={paginationModel}
          onPaginationModelChange={handlePaginationChange}
          disableRowSelectionOnClick
          autoHeight={false}
          sx={{
            bgcolor: 'background.default',
            color: 'text.primary',
            border: 0,
            '& .MuiDataGrid-cell': {
              borderBottom: `1px solid ${theme.palette.divider}`,
            },
            '& .MuiDataGrid-columnHeaders': {
              bgcolor: theme.palette.mode === 'dark' ? 'rgba(255,255,255,0.03)' : 'rgba(0,0,0,0.03)',
              color: 'text.primary',
              fontWeight: 700,
            },
            '& .MuiDataGrid-footerContainer': {
              bgcolor: 'background.paper',
            },
            '& .MuiDataGrid-row:hover': {
              bgcolor: theme.palette.action.hover,
            },
          }}
          localeText={ptBR.components.MuiDataGrid.defaultProps.localeText}
        />
      </Box>
    </Paper>
  );
};

export default DataTable; 