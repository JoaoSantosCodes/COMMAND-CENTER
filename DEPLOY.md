# 🚀 Deploy em Produção - ConsultaVD v2.0

## 📋 Pré-requisitos

### Software Necessário
- **Docker** (versão 20.10+)
- **Docker Compose** (versão 2.0+)
- **Git** (para clonar o repositório)

### Recursos do Servidor
- **CPU**: Mínimo 2 cores
- **RAM**: Mínimo 4GB
- **Disco**: Mínimo 10GB livre
- **Rede**: Porta 80 e 8000 disponíveis

## 🏗️ Arquitetura de Produção

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Nginx Proxy   │    │  Frontend React │    │  Backend FastAPI│
│   (Porta 80)    │◄──►│   (Container)   │◄──►│   (Container)   │
│                 │    │                 │    │   (Porta 8000)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │   SQLite DB     │
                    │   (Volume)      │
                    └─────────────────┘
```

## 🚀 Deploy Automatizado

### Opção 1: Script Automático (Recomendado)
```bash
# Execute o script de deploy
deploy.bat
```

### Opção 2: Comandos Manuais
```bash
# 1. Parar containers existentes
docker-compose down

# 2. Construir imagens
docker-compose build --no-cache

# 3. Iniciar em modo detached
docker-compose up -d

# 4. Verificar status
docker-compose ps
```

## ⚙️ Configurações de Produção

### Variáveis de Ambiente
Crie um arquivo `.env` na raiz do projeto:

```env
# Ambiente
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO

# Segurança
SECRET_KEY=sua-chave-secreta-muito-segura
CORS_ORIGINS=http://seu-dominio.com,https://seu-dominio.com

# Banco de Dados
DATABASE_PATH=data/consulta_vd.db
BACKUP_PATH=data/backup/

# Performance
BATCH_SIZE=1000
CONNECTION_POOL_SIZE=20
CACHE_TTL_SECONDS=300

# Monitoramento
ENABLE_METRICS=true
METRICS_INTERVAL_SECONDS=60
```

### Configurações de SSL (Opcional)
Para HTTPS, adicione certificados SSL:

```bash
# Criar diretório para certificados
mkdir nginx/ssl

# Copiar certificados
cp seu-certificado.crt nginx/ssl/
cp sua-chave-privada.key nginx/ssl/
```

## 📊 Monitoramento

### Verificar Logs
```bash
# Logs de todos os serviços
docker-compose logs -f

# Logs específicos
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Health Checks
- **Backend**: http://localhost:8000/api/health
- **Frontend**: http://localhost:80

### Métricas
```bash
# Status dos containers
docker-compose ps

# Uso de recursos
docker stats
```

## 🔧 Manutenção

### Backup do Banco de Dados
```bash
# Backup automático (configurado no docker-compose)
# Ou manual:
docker exec consultavd-backend sqlite3 data/consulta_vd.db ".backup data/backup/backup_$(date +%Y%m%d_%H%M%S).db"
```

### Atualizações
```bash
# 1. Parar sistema
docker-compose down

# 2. Atualizar código
git pull origin main

# 3. Reconstruir e reiniciar
docker-compose build --no-cache
docker-compose up -d
```

### Rollback
```bash
# Voltar para versão anterior
git checkout <tag-version>
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

## 🛡️ Segurança

### Configurações Recomendadas
- ✅ Usar HTTPS em produção
- ✅ Configurar firewall
- ✅ Manter certificados SSL atualizados
- ✅ Fazer backups regulares
- ✅ Monitorar logs de acesso

### Firewall
```bash
# Permitir apenas portas necessárias
ufw allow 80/tcp   # HTTP
ufw allow 443/tcp  # HTTPS
ufw allow 22/tcp   # SSH (se necessário)
ufw enable
```

## 📈 Escalabilidade

### Para Alta Demanda
1. **Aumentar workers do backend**:
   ```env
   WORKERS=8
   ```

2. **Configurar load balancer**:
   ```yaml
   # Adicionar ao docker-compose.yml
   services:
     backend:
       deploy:
         replicas: 3
   ```

3. **Usar banco PostgreSQL**:
   - Substituir SQLite por PostgreSQL
   - Configurar connection pooling

## 🚨 Troubleshooting

### Problemas Comuns

#### Container não inicia
```bash
# Verificar logs
docker-compose logs backend

# Verificar recursos
docker system df
```

#### Erro de permissão
```bash
# Corrigir permissões
sudo chown -R $USER:$USER data/
sudo chmod -R 755 data/
```

#### Porta já em uso
```bash
# Verificar portas
netstat -tulpn | grep :80
netstat -tulpn | grep :8000

# Parar serviço conflitante
sudo systemctl stop apache2  # exemplo
```

## 📞 Suporte

### Comandos Úteis
```bash
# Reiniciar serviço específico
docker-compose restart backend

# Ver logs em tempo real
docker-compose logs -f --tail=100

# Executar comando no container
docker-compose exec backend python -c "print('Teste')"

# Backup manual
docker-compose exec backend sqlite3 data/consulta_vd.db ".backup backup_manual.db"
```

### Contatos
- **Documentação**: Ver pasta `docs/`
- **Issues**: Criar issue no repositório
- **Logs**: Verificar `logs/consulta_vd.log`

---

**✅ Sistema ConsultaVD v2.0 pronto para produção!**
