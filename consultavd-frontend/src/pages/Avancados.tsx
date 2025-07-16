import React, { useState, useEffect } from 'react';
import { Box, Typography, Tabs, Tab, Paper, TextField, Button, MenuItem, Divider, Alert, IconButton, InputAdornment, Card, CardContent, Stack, Grid } from '@mui/material';
import ContentCopyIcon from '@mui/icons-material/ContentCopy';
import ReportProblemIcon from '@mui/icons-material/ReportProblem';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import RestartAltIcon from '@mui/icons-material/RestartAlt';
import DeleteIcon from '@mui/icons-material/Delete';
import AddIcon from '@mui/icons-material/Add';
import SaveIcon from '@mui/icons-material/Save';
import { alpha } from '@mui/material/styles';
import { Fade } from '@mui/material';
import apiService from '../services/api';

const mainTabs = ['Informativos', 'Navegação', 'Utilitários'];
const infoTabs = ['Informativo de Incidente', 'Alerta de Monitoramento', 'Templates', 'Histórico'];

// Defina antes de tudo:
type IncidentForm = {
  operacao: string;
  natureza: string;
  impacto: string;
  descricao: string;
  inicio: string;
  termino: string;
  acao: string;
  status: string;
};

// Template type (agora alinhado ao backend)
type Template = {
  id: number;
  tipo: string;
  nome: string;
  conteudo: IncidentForm;
  criado_em: string;
};

// Alerta form type
type AlertaForm = {
  alarme: string;
  impacto: string;
  abrangencia: string;
  inicio: string;
  termino: string;
  equipes: string;
  acao: string;
};

// Alerta template type
type AlertaTemplate = {
  id: number;
  tipo: string;
  nome: string;
  conteudo: AlertaForm;
  criado_em: string;
};

const Avancados: React.FC = () => {
  const [tab, setTab] = useState(0);
  const [infoTab, setInfoTab] = useState(0);

  // Campos do informativo
  const [form, setForm] = useState<IncidentForm>({
    operacao: '',
    natureza: '',
    impacto: '',
    descricao: '',
    inicio: '',
    termino: '',
    acao: '',
    status: '⚠️',
  });
  const [informativo, setInformativo] = useState('');
  const [copied, setCopied] = useState(false);
  const [error, setError] = useState('');

  // Templates state
  const [templates, setTemplates] = useState<Template[]>([]);
  const [templateName, setTemplateName] = useState('');
  const [showSaveTemplate, setShowSaveTemplate] = useState(false);

  // Estado para alerta de monitoramento
  const [alerta, setAlerta] = useState<AlertaForm>({
    alarme: '',
    impacto: '',
    abrangencia: '',
    inicio: '',
    termino: '',
    equipes: '',
    acao: '',
  });
  const [alertaGerado, setAlertaGerado] = useState('');
  const [alertaCopied, setAlertaCopied] = useState(false);

  // Alerta templates state
  const [alertaTemplates, setAlertaTemplates] = useState<AlertaTemplate[]>([]);
  const [alertaTemplateName, setAlertaTemplateName] = useState('');
  const [showSaveAlertaTemplate, setShowSaveAlertaTemplate] = useState(false);

  // Carregar templates do backend ao iniciar
  useEffect(() => {
    apiService.getTemplates('informativo').then(setTemplates);
    apiService.getTemplates('alerta').then(setAlertaTemplates);
  }, []);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleStatus = (status: string) => setForm({ ...form, status });

  const gerarInformativo = () => {
    // Validação obrigatória
    if (!form.operacao || !form.natureza || !form.impacto || !form.descricao || !form.inicio || !form.acao) {
      setError('Preencha todos os campos obrigatórios.');
      return;
    }
    setError('');
    const texto = `${form.status} Informativo incidente: \n` +
      `Operação afetada: ${form.operacao}\n` +
      `Natureza do incidente: ${form.natureza}\n` +
      `Tipo de impacto: ${form.impacto}\n` +
      `Descrição do impacto: ${form.descricao}\n` +
      `Horário de início do incidente: ${form.inicio}\n` +
      `Horário do término do incidente: ${form.termino || 'Sem previsão'}\n` +
      `Ação: ${form.acao}`;
    setInformativo(texto);
    setCopied(false);
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(informativo);
    setCopied(true);
  };

  const handleClear = () => {
    setForm({
      operacao: '', natureza: '', impacto: '', descricao: '', inicio: '', termino: '', acao: '', status: '⚠️',
    });
    setInformativo('');
    setCopied(false);
    setError('');
  };

  // Salvar template de informativo no backend
  const handleSaveTemplate = async () => {
    if (!templateName.trim()) return;
    const novo = await apiService.createTemplate({
      tipo: 'informativo',
      nome: templateName.trim(),
      conteudo: form,
    });
    setTemplates(prev => [novo, ...prev]);
    setTemplateName('');
    setShowSaveTemplate(false);
  };
  // Aplicar template de informativo
  const handleApplyTemplate = (tpl: Template) => {
    setForm(tpl.conteudo);
    setInfoTab(0);
  };
  // Excluir template de informativo
  const handleDeleteTemplate = async (id: number) => {
    await apiService.deleteTemplate(id);
    setTemplates(prev => prev.filter(t => t.id !== id));
  };

  const gerarAlerta = () => {
    const texto = `📢Alerta de monitoramento - Central de Comando:\n` +
      `Alarme: ${alerta.alarme}\n` +
      `Impacto: ${alerta.impacto}\n` +
      `Abrangência: ${alerta.abrangencia}\n` +
      `Horário de início: ${alerta.inicio}\n` +
      `Horário de término: ${alerta.termino || 'Sem previsão'}\n` +
      `Equipes em atuação: ${alerta.equipes}\n` +
      `Ação/Status: ${alerta.acao}`;
    setAlertaGerado(texto);
    setAlertaCopied(false);
  };
  const handleAlertaChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setAlerta({ ...alerta, [e.target.name]: e.target.value });
  };
  const handleAlertaCopy = () => {
    navigator.clipboard.writeText(alertaGerado);
    setAlertaCopied(true);
  };

  // Salvar template de alerta no backend
  const handleSaveAlertaTemplate = async () => {
    if (!alertaTemplateName.trim()) return;
    const novo = await apiService.createTemplate({
      tipo: 'alerta',
      nome: alertaTemplateName.trim(),
      conteudo: alerta,
    });
    setAlertaTemplates(prev => [novo, ...prev]);
    setAlertaTemplateName('');
    setShowSaveAlertaTemplate(false);
  };
  // Aplicar template de alerta
  const handleApplyAlertaTemplate = (tpl: AlertaTemplate) => {
    setAlerta(tpl.conteudo);
    setInfoTab(3);
  };
  // Excluir template de alerta
  const handleDeleteAlertaTemplate = async (id: number) => {
    await apiService.deleteTemplate(id);
    setAlertaTemplates(prev => prev.filter(t => t.id !== id));
  };

  return (
    <Box>
      <Typography variant="h5" fontWeight={700} mb={2}>Avançados</Typography>
      <Paper sx={{ mb: 2, bgcolor: 'background.paper', color: 'text.primary' }}>
        <Tabs value={tab} onChange={(_, v) => setTab(v)} indicatorColor="primary" textColor="primary">
          {mainTabs.map((label, idx) => (
            <Tab label={label} key={label} />
          ))}
        </Tabs>
      </Paper>
      {tab === 0 && (
        <Box>
          <Paper sx={{ mb: 2, bgcolor: 'background.paper', color: 'text.primary' }}>
            <Tabs value={infoTab} onChange={(_, v) => setInfoTab(v)} indicatorColor="secondary" textColor="secondary">
              {infoTabs.map((label, idx) => (
                <Tab label={label} key={label} />
              ))}
            </Tabs>
          </Paper>
          {infoTab === 0 && (
            <Box p={2} display="flex" justifyContent="center">
              <Card sx={{ width: '100%', maxWidth: 480, boxShadow: 6, px: 2, borderRadius: 4, background: t => `linear-gradient(135deg, ${alpha(t.palette.background.paper, 0.95)} 80%, ${alpha(t.palette.primary.light, 0.08)})` }}>
                <CardContent>
                  <Box display="flex" alignItems="center" gap={1} mb={1}>
                    <ReportProblemIcon color="warning" fontSize="large" />
                    <Typography variant="h6" fontWeight={700} sx={{ fontSize: 20 }}>Gerar Informativo de Incidente</Typography>
                  </Box>
                  <Box sx={{ height: 3, width: 60, bgcolor: 'primary.main', borderRadius: 2, mb: 2 }} />
                  <Stack spacing={1.5}>
                    <Grid container spacing={1} alignItems="center">
                      <Grid item xs={6}>
                        <Button
                          fullWidth
                          variant={form.status === '⚠️' ? 'contained' : 'outlined'}
                          color="warning"
                          onClick={() => handleStatus('⚠️')}
                          startIcon={<ReportProblemIcon />}
                          sx={{ bgcolor: form.status === '⚠️' ? 'warning.light' : undefined, transition: '0.2s', fontWeight: 700, fontSize: 16, '&:hover': { bgcolor: 'warning.main', color: 'white' } }}
                        >
                          Em andamento
                        </Button>
                      </Grid>
                      <Grid item xs={6}>
                        <Button
                          fullWidth
                          variant={form.status === '✅' ? 'contained' : 'outlined'}
                          color="success"
                          onClick={() => handleStatus('✅')}
                          startIcon={<CheckCircleIcon />}
                          sx={{ bgcolor: form.status === '✅' ? 'success.light' : undefined, transition: '0.2s', fontWeight: 700, fontSize: 16, '&:hover': { bgcolor: 'success.main', color: 'white' } }}
                        >
                          Normalizado
                        </Button>
                      </Grid>
                    </Grid>
                    <Divider sx={{ my: 1 }} />
                    <TextField label="Operação afetada *" name="operacao" value={form.operacao} onChange={handleChange} fullWidth required placeholder="Ex: 1131 | DP VILAR DOS TELES 1" autoComplete="off" InputProps={{ sx: { fontSize: 17 } }} InputLabelProps={{ sx: { fontSize: 16 } }} focused color="primary" />
                    <TextField label="Natureza do incidente *" name="natureza" value={form.natureza} onChange={handleChange} fullWidth required placeholder="Ex: Loja isolada por energia" autoComplete="off" InputProps={{ sx: { fontSize: 17 } }} InputLabelProps={{ sx: { fontSize: 16 } }} focused color="primary" />
                    <TextField label="Tipo de impacto *" name="impacto" value={form.impacto} onChange={handleChange} select fullWidth required InputProps={{ sx: { fontSize: 17 } }} InputLabelProps={{ sx: { fontSize: 16 } }} focused color="primary">
                      <MenuItem value="Alto">Alto</MenuItem>
                      <MenuItem value="Médio">Médio</MenuItem>
                      <MenuItem value="Baixo">Baixo</MenuItem>
                    </TextField>
                    <TextField label="Descrição do impacto *" name="descricao" value={form.descricao} onChange={handleChange} fullWidth required placeholder="Ex: Sem energia elétrica na região" autoComplete="off" InputProps={{ sx: { fontSize: 17 } }} InputLabelProps={{ sx: { fontSize: 16 } }} focused color="primary" />
                    <Box sx={{ bgcolor: t => alpha(t.palette.primary.light, 0.08), borderRadius: 2, p: 1, mb: 1 }}>
                      <Grid container spacing={1} alignItems="center">
                        <Grid item xs={6}>
                          <TextField label="Início *" name="inicio" value={form.inicio} onChange={handleChange} type="time" InputLabelProps={{ shrink: true, sx: { fontSize: 15 } }} fullWidth required size="small" color="primary" focused />
                        </Grid>
                        <Grid item xs={6}>
                          <TextField label="Término" name="termino" value={form.termino} onChange={handleChange} type="time" InputLabelProps={{ shrink: true, sx: { fontSize: 15 } }} fullWidth size="small" color="primary" focused />
                        </Grid>
                      </Grid>
                    </Box>
                    <TextField label="Ação *" name="acao" value={form.acao} onChange={handleChange} fullWidth required placeholder="Ex: Acompanhando até a normalização." autoComplete="off" multiline minRows={2} InputProps={{ sx: { fontSize: 17 } }} InputLabelProps={{ sx: { fontSize: 16 } }} focused color="primary" />
                    {error && <Alert severity="error">{error}</Alert>}
                    <Divider sx={{ my: 1 }} />
                    <Grid container spacing={1}>
                      <Grid item xs={6}>
                        <Button variant="contained" color="primary" size="large" onClick={gerarInformativo} sx={{ fontWeight: 700, py: 1.5, fontSize: 17, transition: '0.2s', '&:hover': { bgcolor: 'primary.dark' } }} fullWidth>Gerar Informativo</Button>
                      </Grid>
                      <Grid item xs={6}>
                        <Button variant="outlined" color="secondary" size="large" onClick={handleClear} startIcon={<RestartAltIcon />} sx={{ fontWeight: 700, py: 1.5, fontSize: 17, transition: '0.2s', '&:hover': { bgcolor: 'secondary.light' } }} fullWidth>Limpar</Button>
                      </Grid>
                    </Grid>
                    <Button variant="outlined" color="info" startIcon={<SaveIcon />} sx={{ mt: 1, fontWeight: 700 }} onClick={() => setShowSaveTemplate(true)} fullWidth>Salvar como template</Button>
                  </Stack>
                </CardContent>
              </Card>
              <Fade in={!!informativo} timeout={400}>
                <div>
                  {informativo && (
                    <Card sx={{ width: '100%', maxWidth: 480, mx: 2, mt: 4, boxShadow: 6, border: '1.5px solid', borderColor: form.status === '⚠️' ? 'warning.main' : 'success.main', borderRadius: 4, bgcolor: 'background.paper', color: 'text.primary', position: 'relative' }}>
                      <CardContent>
                        <Box display="flex" alignItems="center" justifyContent="space-between" mb={1}>
                          <Typography variant="subtitle1" fontWeight={700} sx={{ fontSize: 18, color: form.status === '⚠️' ? 'warning.main' : 'success.main', display: 'flex', alignItems: 'center' }}>
                            {form.status === '⚠️' ? <ReportProblemIcon color="warning" sx={{ verticalAlign: 'middle', mr: 1 }} /> : <CheckCircleIcon color="success" sx={{ verticalAlign: 'middle', mr: 1 }} />} Informativo Gerado
                          </Typography>
                          <Button
                            onClick={handleCopy}
                            variant="contained"
                            color={form.status === '⚠️' ? 'warning' : 'success'}
                            size="small"
                            startIcon={<ContentCopyIcon />}
                            sx={{ fontWeight: 700, minWidth: 0, px: 2, py: 0.5, borderRadius: 2, boxShadow: 1, color: 'background.paper' }}
                          >
                            Copiar
                          </Button>
                        </Box>
                        <Divider sx={{ mb: 2, borderColor: form.status === '⚠️' ? 'warning.main' : 'success.main' }} />
                        <Box sx={{ fontSize: 17, color: 'text.primary', lineHeight: 1.7, fontFamily: 'inherit', whiteSpace: 'pre-line', wordBreak: 'break-word' }}>
                          {informativo}
                        </Box>
                        {copied && <Typography color="success.main" mt={2} align="center" fontWeight={600}>Copiado para a área de transferência!</Typography>}
                      </CardContent>
                    </Card>
                  )}
                </div>
              </Fade>
            </Box>
          )}
          {infoTab === 1 && (
            <Box p={2} display="flex" justifyContent="center">
              <Card sx={{ width: '100%', maxWidth: 480, boxShadow: 6, px: 2, borderRadius: 4, background: t => `linear-gradient(135deg, ${alpha(t.palette.background.paper, 0.95)} 80%, ${alpha(t.palette.info.light, 0.08)})` }}>
                <CardContent>
                  <Box display="flex" alignItems="center" gap={1} mb={1}>
                    <ReportProblemIcon color="info" fontSize="large" />
                    <Typography variant="h6" fontWeight={700} sx={{ fontSize: 20 }}>Gerar Alerta de Monitoramento</Typography>
                  </Box>
                  <Box sx={{ height: 3, width: 60, bgcolor: 'info.main', borderRadius: 2, mb: 2 }} />
                  <Stack spacing={1.5}>
                    <TextField label="Alarme *" name="alarme" value={alerta.alarme} onChange={handleAlertaChange} fullWidth required placeholder="Ex: Identificamos um alerta em nossa monitoria relacionado ao GDB - epharma" autoComplete="off" InputProps={{ sx: { fontSize: 17 } }} InputLabelProps={{ sx: { fontSize: 16 } }} focused color="info" />
                    <TextField label="Impacto *" name="impacto" value={alerta.impacto} onChange={handleAlertaChange} fullWidth required placeholder="Ex: O tempo de resposta da autorização está acima do normal..." autoComplete="off" InputProps={{ sx: { fontSize: 17 } }} InputLabelProps={{ sx: { fontSize: 16 } }} focused color="info" />
                    <TextField label="Abrangência *" name="abrangencia" value={alerta.abrangencia} onChange={handleAlertaChange} fullWidth required placeholder="Ex: Lojas" autoComplete="off" InputProps={{ sx: { fontSize: 17 } }} InputLabelProps={{ sx: { fontSize: 16 } }} focused color="info" />
                    <Box sx={{ bgcolor: t => alpha(t.palette.info.light, 0.08), borderRadius: 2, p: 1, mb: 1 }}>
                      <Grid container spacing={1} alignItems="center">
                        <Grid item xs={6}>
                          <TextField label="Início *" name="inicio" value={alerta.inicio} onChange={handleAlertaChange} type="time" InputLabelProps={{ shrink: true, sx: { fontSize: 15 } }} fullWidth required size="small" color="info" focused />
                        </Grid>
                        <Grid item xs={6}>
                          <TextField label="Término" name="termino" value={alerta.termino} onChange={handleAlertaChange} type="time" InputLabelProps={{ shrink: true, sx: { fontSize: 15 } }} fullWidth size="small" color="info" focused />
                        </Grid>
                        <Grid item xs={12} mt={1}>
                          <TextField label="Equipes em atuação *" name="equipes" value={alerta.equipes} onChange={handleAlertaChange} fullWidth required placeholder="Ex: Time GDB, Fornecedor Epharma." InputProps={{ sx: { fontSize: 17 } }} InputLabelProps={{ sx: { fontSize: 16 } }} focused color="info" />
                        </Grid>
                      </Grid>
                    </Box>
                    <TextField label="Ação/Status *" name="acao" value={alerta.acao} onChange={handleAlertaChange} fullWidth required placeholder="Ex: Em acompanhamento" autoComplete="off" InputProps={{ sx: { fontSize: 17 } }} InputLabelProps={{ sx: { fontSize: 16 } }} focused color="info" />
                    <Divider sx={{ my: 1 }} />
                    <Button variant="contained" color="info" size="large" onClick={gerarAlerta} sx={{ fontWeight: 700, py: 1.5, fontSize: 17, transition: '0.2s', '&:hover': { bgcolor: 'info.dark' } }} fullWidth>Gerar Alerta</Button>
                    <Button variant="outlined" color="info" startIcon={<SaveIcon />} sx={{ mt: 1, fontWeight: 700 }} onClick={() => setShowSaveAlertaTemplate(true)} fullWidth>Salvar como template</Button>
                  </Stack>
                </CardContent>
              </Card>
              <Fade in={!!alertaGerado} timeout={400}>
                <div>
                  {alertaGerado && (
                    <Card sx={{ width: '100%', maxWidth: 480, mx: 2, mt: 4, boxShadow: 6, border: '1.5px solid', borderColor: 'info.main', borderRadius: 4, bgcolor: 'background.paper', color: 'text.primary', position: 'relative' }}>
                      <CardContent>
                        <Box display="flex" alignItems="center" justifyContent="space-between" mb={1}>
                          <Typography variant="subtitle1" fontWeight={700} sx={{ fontSize: 18, color: 'info.main', display: 'flex', alignItems: 'center' }}>
                            <ReportProblemIcon color="info" sx={{ verticalAlign: 'middle', mr: 1 }} /> Alerta Gerado
                          </Typography>
                          <Button
                            onClick={handleAlertaCopy}
                            variant="contained"
                            color="info"
                            size="small"
                            startIcon={<ContentCopyIcon />}
                            sx={{ fontWeight: 700, minWidth: 0, px: 2, py: 0.5, borderRadius: 2, boxShadow: 1, color: 'background.paper' }}
                          >
                            Copiar
                          </Button>
                        </Box>
                        <Divider sx={{ mb: 2, borderColor: 'info.main' }} />
                        <Box sx={{ fontSize: 17, color: 'text.primary', lineHeight: 1.7, fontFamily: 'inherit', whiteSpace: 'pre-line', wordBreak: 'break-word' }}>
                          {alertaGerado}
                        </Box>
                        {alertaCopied && <Typography color="success.main" mt={2} align="center" fontWeight={600}>Copiado para a área de transferência!</Typography>}
                      </CardContent>
                    </Card>
                  )}
                </div>
              </Fade>
            </Box>
          )}
          {infoTab === 2 && (
            <Box p={2} display="flex" justifyContent="center">
              <Card sx={{ width: '100%', maxWidth: 600, boxShadow: 4, borderRadius: 4, bgcolor: 'background.paper', color: 'text.primary', px: 2 }}>
                <CardContent>
                  <Box display="flex" alignItems="center" gap={1} mb={2}>
                    <AddIcon color="info" />
                    <Typography variant="h6" fontWeight={700}>Templates de Informativo</Typography>
                  </Box>
                  {templates.length === 0 ? (
                    <Typography color="text.secondary" mt={2}>Nenhum template salvo ainda.</Typography>
                  ) : (
                    <Stack spacing={2}>
                      {templates.map(tpl => (
                        <Card key={tpl.id} sx={{ bgcolor: 'background.default', border: '1px solid', borderColor: 'divider', borderRadius: 2, boxShadow: 1 }}>
                          <CardContent>
                            <Box display="flex" alignItems="center" justifyContent="space-between">
                              <Box>
                                <Typography fontWeight={700}>{tpl.nome}</Typography>
                                <Typography variant="caption" color="text.secondary">Salvo em: {tpl.criado_em}</Typography>
                              </Box>
                              <Box>
                                <Button size="small" variant="contained" color="primary" sx={{ mr: 1 }} onClick={() => handleApplyTemplate(tpl)}>Aplicar</Button>
                                <IconButton color="error" onClick={() => handleDeleteTemplate(tpl.id)}><DeleteIcon /></IconButton>
                              </Box>
                            </Box>
                          </CardContent>
                        </Card>
                      ))}
                    </Stack>
                  )}
                  <Divider sx={{ my: 3 }} />
                  <Box display="flex" alignItems="center" gap={1} mb={2} mt={2}>
                    <AddIcon color="info" />
                    <Typography variant="h6" fontWeight={700}>Templates de Alerta de Monitoramento</Typography>
                  </Box>
                  {alertaTemplates.length === 0 ? (
                    <Typography color="text.secondary" mt={2}>Nenhum template salvo ainda.</Typography>
                  ) : (
                    <Stack spacing={2}>
                      {alertaTemplates.map(tpl => (
                        <Card key={tpl.id} sx={{ bgcolor: 'background.default', border: '1px solid', borderColor: 'divider', borderRadius: 2, boxShadow: 1 }}>
                          <CardContent>
                            <Box display="flex" alignItems="center" justifyContent="space-between">
                              <Box>
                                <Typography fontWeight={700}>{tpl.nome}</Typography>
                                <Typography variant="caption" color="text.secondary">Salvo em: {tpl.criado_em}</Typography>
                              </Box>
                              <Box>
                                <Button size="small" variant="contained" color="info" sx={{ mr: 1 }} onClick={() => handleApplyAlertaTemplate(tpl)}>Aplicar</Button>
                                <IconButton color="error" onClick={() => handleDeleteAlertaTemplate(tpl.id)}><DeleteIcon /></IconButton>
                              </Box>
                            </Box>
                          </CardContent>
                        </Card>
                      ))}
                    </Stack>
                  )}
                </CardContent>
              </Card>
              {/* Modal para salvar template de informativo */}
              {showSaveTemplate && (
                <Box position="fixed" top={0} left={0} width="100vw" height="100vh" display="flex" alignItems="center" justifyContent="center" bgcolor="rgba(0,0,0,0.3)" zIndex={9999}>
                  <Card sx={{ minWidth: 320, p: 2 }}>
                    <CardContent>
                      <Typography fontWeight={700} mb={2}>Salvar template</Typography>
                      <TextField label="Nome do template" value={templateName} onChange={e => setTemplateName(e.target.value)} fullWidth autoFocus />
                      <Box mt={2} display="flex" gap={2}>
                        <Button variant="contained" color="primary" onClick={handleSaveTemplate} disabled={!templateName.trim()}>Salvar</Button>
                        <Button variant="outlined" color="secondary" onClick={() => setShowSaveTemplate(false)}>Cancelar</Button>
                      </Box>
                    </CardContent>
                  </Card>
                </Box>
              )}
              {/* Modal para salvar template de alerta */}
              {showSaveAlertaTemplate && (
                <Box position="fixed" top={0} left={0} width="100vw" height="100vh" display="flex" alignItems="center" justifyContent="center" bgcolor="rgba(0,0,0,0.3)" zIndex={9999}>
                  <Card sx={{ minWidth: 320, p: 2 }}>
                    <CardContent>
                      <Typography fontWeight={700} mb={2}>Salvar template de alerta</Typography>
                      <TextField label="Nome do template" value={alertaTemplateName} onChange={e => setAlertaTemplateName(e.target.value)} fullWidth autoFocus />
                      <Box mt={2} display="flex" gap={2}>
                        <Button variant="contained" color="info" onClick={handleSaveAlertaTemplate} disabled={!alertaTemplateName.trim()}>Salvar</Button>
                        <Button variant="outlined" color="secondary" onClick={() => setShowSaveAlertaTemplate(false)}>Cancelar</Button>
                      </Box>
                    </CardContent>
                  </Card>
                </Box>
              )}
            </Box>
          )}
          {infoTab === 3 && (
            <Box p={2}><Typography>Histórico (placeholder)</Typography></Box>
          )}
        </Box>
      )}
      {tab === 1 && <Box p={2}><Typography>Navegação (placeholder)</Typography></Box>}
      {tab === 2 && <Box p={2}><Typography>Utilitários (placeholder)</Typography></Box>}
    </Box>
  );
};

export default Avancados; 