import React, { useEffect, useState, useRef, useCallback } from 'react';
import ReactMarkdown from 'react-markdown';
import { Box, CircularProgress, Typography, InputBase, IconButton, MenuItem, FormControl, OutlinedInput, SelectChangeEvent } from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import ChevronRightIcon from '@mui/icons-material/ChevronRight';
import ArrowUpwardIcon from '@mui/icons-material/ArrowUpward';
import Autocomplete from '@mui/material/Autocomplete';
import TextField from '@mui/material/TextField';
import DescriptionIcon from '@mui/icons-material/Description';
import { useTheme, ThemeProvider, createTheme } from '@mui/material/styles';
import Breadcrumbs from '@mui/material/Breadcrumbs';
import Link from '@mui/material/Link';
import PrintIcon from '@mui/icons-material/Print';
import LightModeIcon from '@mui/icons-material/LightMode';
import DarkModeIcon from '@mui/icons-material/DarkMode';
import ContentCopyIcon from '@mui/icons-material/ContentCopy';

const exemploMarkdown = `
# 📚 Documentação Software de Consulta COMMAND CENTER

---

> Se você está vendo este texto, o componente de Markdown está funcionando!
`;

// Utilitário para slug de heading
function slugify(text: string) {
  return text
    .toLowerCase()
    .replace(/[^a-z0-9\u00C0-\u00FF\s-]/g, '')
    .replace(/\s+/g, '-')
    .replace(/-+/g, '-')
    .replace(/^-|-$/g, '');
}

// Extrai headings do markdown (H2, H3, H4)
function extractHeadings(markdown: string) {
  const lines = markdown.split('\n');
  const headings = [];
  for (let i = 0; i < lines.length; i++) {
    const match = lines[i].match(/^(#{2,4})\s+(.+)/);
    if (match) {
      const level = match[1].length;
      const text = match[2].replace(/[#*`_]+/g, '').trim();
      const id = slugify(text);
      headings.push({ id, text, level, children: [] });
    }
  }
  // Monta árvore de headings
  const tree: any[] = [];
  const stack: any[] = [];
  headings.forEach((h) => {
    while (stack.length && stack[stack.length - 1].level >= h.level) stack.pop();
    if (stack.length === 0) {
      tree.push(h);
      stack.push(h);
    } else {
      stack[stack.length - 1].children.push(h);
      stack.push(h);
    }
  });
  return tree;
}

// Lista linear de headings para o seletor
function flattenHeadings(nodes: any[], arr: any[] = [], prefix = '') {
  nodes.forEach((h) => {
    arr.push({ id: h.id, text: h.text, level: h.level });
    if (h.children) flattenHeadings(h.children, arr, prefix + '  ');
  });
  return arr;
}

const Documentacao: React.FC = () => {
  const [markdown, setMarkdown] = useState<string>('');
  const [loading, setLoading] = useState(true);
  const [headings, setHeadings] = useState<any[]>([]);
  const [collapsed, setCollapsed] = useState<{ [key: string]: boolean }>({});
  const [activeId, setActiveId] = useState<string>('');
  const [search, setSearch] = useState('');
  const observerRef = useRef<IntersectionObserver | null>(null);
  const headingIndexRef = useRef(0);
  const [showScrollTop, setShowScrollTop] = useState(false);
  const [highlightId, setHighlightId] = useState<string | null>(null);
  const [fadeKey, setFadeKey] = useState(0);
  const [docTheme, setDocTheme] = useState<'dark' | 'light'>('dark');
  const [scrollProgress, setScrollProgress] = useState(0);

  // Busca headings ao carregar markdown
  useEffect(() => {
    fetch('/DOCUMENTACAO_UNIFICADA.md')
      .then((res) => {
        if (!res.ok) throw new Error('Arquivo não encontrado');
        return res.text();
      })
      .then((text) => {
        setMarkdown(text);
        setHeadings(extractHeadings(text));
        setLoading(false);
      })
      .catch(() => {
        setMarkdown(exemploMarkdown);
        setHeadings(extractHeadings(exemploMarkdown));
        setLoading(false);
      });
  }, []);

  // Scrollspy para qualquer heading
  useEffect(() => {
    if (loading) return;
    const allIds: string[] = [];
    function collectIds(nodes: any[]) {
      nodes.forEach((n) => {
        allIds.push(n.id);
        if (n.children) collectIds(n.children);
      });
    }
    collectIds(headings);
    const handleIntersect = (entries: IntersectionObserverEntry[]) => {
      const visible = entries.filter((e) => e.isIntersecting);
      if (visible.length > 0) {
        const topSection = visible.sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top)[0];
        setActiveId(topSection.target.id);
      }
    };
    const observer = new window.IntersectionObserver(handleIntersect, {
      root: null,
      rootMargin: '0px 0px -70% 0px',
      threshold: 0.1,
    });
    allIds.forEach((id) => {
      const el = document.getElementById(id);
      if (el) observer.observe(el);
    });
    observerRef.current = observer;
    return () => {
      observer.disconnect();
    };
  }, [loading, headings]);

  // Scroll progress bar
  useEffect(() => {
    const onScroll = () => {
      const scrollTop = window.scrollY;
      const docHeight = document.documentElement.scrollHeight - window.innerHeight;
      setScrollProgress(docHeight > 0 ? (scrollTop / docHeight) * 100 : 0);
    };
    window.addEventListener('scroll', onScroll);
    return () => window.removeEventListener('scroll', onScroll);
  }, []);

  // Breadcrumbs
  function getBreadcrumb(activeId: string) {
    const path: any[] = [];
    function findPath(nodes: any[]): boolean {
      for (const n of nodes) {
        if (n.id === activeId) {
          path.unshift(n);
          return true;
        }
        if (n.children && findPath(n.children)) {
          path.unshift(n);
          return true;
        }
      }
      return false;
    }
    findPath(headings);
    return path;
  }
  const breadcrumb = getBreadcrumb(activeId);

  // Destaque temporário ao navegar
  const handleHighlight = (id: string) => {
    setHighlightId(id);
    setTimeout(() => setHighlightId(null), 1200);
  };

  // Modo claro/escuro independente
  const muiTheme = createTheme({
    palette: {
      mode: docTheme,
      background: { default: docTheme === 'dark' ? '#181820' : '#fff' },
      text: { primary: docTheme === 'dark' ? '#fff' : '#181820' },
    },
  });

  // Impressão
  const handlePrint = () => {
    window.print();
  };

  // Copiar link do heading
  const handleCopyLink = (id: string) => {
    const url = `${window.location.origin}${window.location.pathname}#${id}`;
    navigator.clipboard.writeText(url);
  };

  // Navegação automática com destaque e fade
  const handleIndexClick = useCallback((id: string) => {
    setActiveId(id);
    setFadeKey(k => k + 1);
    let attempts = 0;
    const tryScroll = () => {
      const el = document.getElementById(id);
      if (el) {
        el.scrollIntoView({ behavior: 'smooth', block: 'start' });
        setTimeout(() => setActiveId(id), 400);
        handleHighlight(id);
      } else if (attempts < 20) {
        attempts++;
        setTimeout(tryScroll, 50);
      }
    };
    tryScroll();
  }, []);

  // Busca no índice
  function filterHeadings(nodes: any[], query: string) {
    if (!query) return nodes;
    const q = query.toLowerCase();
    function filterNode(node: any): any | null {
      if (node.text.toLowerCase().includes(q)) {
        return { ...node, children: node.children.map(filterNode).filter(Boolean) };
      }
      const filteredChildren = node.children.map(filterNode).filter(Boolean);
      if (filteredChildren.length > 0) {
        return { ...node, children: filteredChildren };
      }
      return null;
    }
    return nodes.map(filterNode).filter(Boolean);
  }

  // Renderização recursiva do índice
  function renderIndex(nodes: any[], level = 2) {
    return (
      <ul className={`doc-index-list level-${level}`}> 
        {nodes.map((h: any) => (
          <li key={h.id} className={`level-${h.level}`}> 
            {h.children && h.children.length > 0 ? (
              <>
                <span
                  className={`collapsible ${collapsed[h.id] ? 'collapsed' : ''}`}
                  onClick={() => setCollapsed((prev) => ({ ...prev, [h.id]: !prev[h.id] }))}
                  tabIndex={0}
                  role="button"
                  aria-expanded={!collapsed[h.id]}
                  style={{ display: 'flex', alignItems: 'center', cursor: 'pointer', userSelect: 'none' }}
                >
                  {collapsed[h.id] ? <ChevronRightIcon fontSize="small" /> : <ExpandMoreIcon fontSize="small" />}
                  <a
                    href={`#${h.id}`}
                    className={activeId === h.id ? 'active' : ''}
                    onClick={e => { e.preventDefault(); handleIndexClick(h.id); }}
                    tabIndex={-1}
                  >
                    {h.text}
                  </a>
                </span>
                {!collapsed[h.id] && renderIndex(h.children, h.level + 1)}
              </>
            ) : (
              <a
                href={`#${h.id}`}
                className={activeId === h.id ? 'active' : ''}
                onClick={e => { e.preventDefault(); handleIndexClick(h.id); }}
              >
                {h.text}
              </a>
            )}
          </li>
        ))}
      </ul>
    );
  }

  // Exibe botão de voltar ao topo após rolar 300px
  useEffect(() => {
    const onScroll = () => {
      setShowScrollTop(window.scrollY > 300);
    };
    window.addEventListener('scroll', onScroll);
    return () => window.removeEventListener('scroll', onScroll);
  }, []);

  // Seletor de tópicos (dropdown)
  const flatHeadings = flattenHeadings(headings);
  const headingIds = flatHeadings.map(h => h.id);

  // Permite selecionar o mesmo item várias vezes no seletor (Autocomplete)
  const handleAutocompleteChange = (_event: any, value: any) => {
    if (value && value.id) {
      handleIndexClick(value.id);
    }
  };

  return (
    <ThemeProvider theme={muiTheme}>
      {/* Barra de progresso de leitura */}
      <div style={{ position: 'fixed', top: 0, left: 0, width: `${scrollProgress}%`, height: 4, background: '#FFA500', zIndex: 2000, transition: 'width 0.2s' }} aria-label="Progresso de leitura" />
      {/* Botão de voltar ao topo */}
      {showScrollTop && (
        <button
          onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}
          style={{
            position: 'fixed',
            bottom: 32,
            right: 32,
            zIndex: 1000,
            background: '#23232b',
            color: '#FFA500',
            border: 'none',
            borderRadius: '50%',
            width: 48,
            height: 48,
            boxShadow: '0 2px 12px #0006',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            cursor: 'pointer',
            transition: 'background 0.2s',
          }}
          aria-label="Voltar ao topo"
        >
          <ArrowUpwardIcon fontSize="medium" />
        </button>
      )}
      <Box p={3} sx={{ maxWidth: 1200, margin: '0 auto', display: 'flex', flexDirection: 'column', background: docTheme === 'dark' ? '#181820' : '#fff', color: docTheme === 'dark' ? '#fff' : '#181820' }}>
        {/* Barra de ações */}
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 1, gap: 2 }}>
          <Typography variant="h6" sx={{ color: '#FFA500', fontWeight: 600, mr: 2 }}>
            Índice
          </Typography>
          <IconButton onClick={handlePrint} aria-label="Imprimir documentação" size="small">
            <PrintIcon />
          </IconButton>
          <IconButton onClick={() => setDocTheme(docTheme === 'dark' ? 'light' : 'dark')} aria-label="Alternar modo claro/escuro" size="small">
            {docTheme === 'dark' ? <LightModeIcon /> : <DarkModeIcon />}
          </IconButton>
        </Box>
        {/* Breadcrumb */}
        <Breadcrumbs aria-label="breadcrumb" sx={{ mb: 2 }}>
          {breadcrumb.map((b, i) => (
            <Link key={b.id} underline="hover" color={i === breadcrumb.length - 1 ? 'inherit' : 'primary'} href={`#${b.id}`} onClick={e => { e.preventDefault(); handleIndexClick(b.id); }}>
              {b.text}
            </Link>
          ))}
        </Breadcrumbs>
        {/* Seletor de tópicos */}
        <FormControl fullWidth size="small" sx={{ mb: 2, maxWidth: 420 }}>
          <Autocomplete
            disablePortal
            options={flatHeadings}
            getOptionLabel={option => option.text}
            value={flatHeadings.find(h => h.id === activeId) || null}
            onChange={handleAutocompleteChange}
            renderInput={(params) => (
              <TextField {...params} label="Selecione ou busque um tópico..." size="small" sx={{ background: docTheme === 'dark' ? '#181820' : '#fff', borderRadius: 2 }} />
            )}
            renderOption={(props, option) => (
              <li {...props} key={option.id} style={{ display: 'flex', alignItems: 'center', paddingLeft: (option.level - 2) * 18 + 8 }}>
                <DescriptionIcon fontSize="small" sx={{ color: '#FFA500', mr: 1 }} />
                <span style={{ opacity: option.level > 2 ? 0.7 : 1 }}>{option.text}</span>
              </li>
            )}
            isOptionEqualToValue={(option, value) => option.id === value.id}
            sx={{ mb: 2, maxWidth: 420 }}
            autoHighlight
            clearOnBlur={false}
            openOnFocus
            noOptionsText="Nenhum tópico encontrado"
          />
        </FormControl>
        {loading ? (
          <CircularProgress />
        ) : (
          <div className="markdown-content" key={fadeKey} style={{ animation: 'fadein 0.7s' }}>
            {(() => {
              headingIndexRef.current = 0;
              return (
                <ReactMarkdown
                  components={{
                    h2: ({ node, ...props }) => {
                      const idx = headingIndexRef.current++;
                      const id = headingIds[idx] || undefined;
                      return (
                        <h2
                          id={id}
                          {...props}
                          tabIndex={-1}
                          aria-label={props.children?.toString()}
                          style={{
                            background: highlightId === id ? '#fff8c4' : undefined,
                            transition: 'background 0.7s',
                            scrollMarginTop: 90,
                            position: 'relative',
                          }}
                        >
                          {props.children}
                          <IconButton size="small" sx={{ ml: 1 }} aria-label="Copiar link da seção" onClick={() => handleCopyLink(id)}>
                            <ContentCopyIcon fontSize="inherit" />
                          </IconButton>
                        </h2>
                      );
                    },
                    h3: ({ node, ...props }) => {
                      const idx = headingIndexRef.current++;
                      const id = headingIds[idx] || undefined;
                      return (
                        <h3
                          id={id}
                          {...props}
                          tabIndex={-1}
                          aria-label={props.children?.toString()}
                          style={{
                            background: highlightId === id ? '#fff8c4' : undefined,
                            transition: 'background 0.7s',
                            scrollMarginTop: 90,
                            position: 'relative',
                          }}
                        >
                          {props.children}
                          <IconButton size="small" sx={{ ml: 1 }} aria-label="Copiar link da seção" onClick={() => handleCopyLink(id)}>
                            <ContentCopyIcon fontSize="inherit" />
                          </IconButton>
                        </h3>
                      );
                    },
                    h4: ({ node, ...props }) => {
                      const idx = headingIndexRef.current++;
                      const id = headingIds[idx] || undefined;
                      return (
                        <h4
                          id={id}
                          {...props}
                          tabIndex={-1}
                          aria-label={props.children?.toString()}
                          style={{
                            background: highlightId === id ? '#fff8c4' : undefined,
                            transition: 'background 0.7s',
                            scrollMarginTop: 90,
                            position: 'relative',
                          }}
                        >
                          {props.children}
                          <IconButton size="small" sx={{ ml: 1 }} aria-label="Copiar link da seção" onClick={() => handleCopyLink(id)}>
                            <ContentCopyIcon fontSize="inherit" />
                          </IconButton>
                        </h4>
                      );
                    },
                  }}
                >
                  {markdown}
                </ReactMarkdown>
              );
            })()}
          </div>
        )}
      </Box>
      {/* Fade-in animation */}
      <style>{`
        @keyframes fadein {
          from { opacity: 0; }
          to { opacity: 1; }
        }
      `}</style>
    </ThemeProvider>
  );
};

export default Documentacao; 