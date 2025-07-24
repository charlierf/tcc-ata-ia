# 🚀 Guia de Instalação e Configuração

## 📋 Pré-requisitos

### 1. Python 3.8+
Verifique se Python está instalado:
```bash
python --version
```

### 2. FFmpeg (obrigatório)
**Windows:**
```bash
winget install FFmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

Verifique a instalação:
```bash
ffmpeg -version
```

## 🔧 Instalação Rápida

### Opção 1: Script Automático (Recomendado)
```bash
# 1. Clone o repositório
git clone https://github.com/charlierf/tcc-ata-ia.git
cd tcc-ata-ia

# 2. Execute o script de configuração
python criar_ambiente.py

# 3. Ative o ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# 4. Verifique a instalação
python src/setup.py
```

### Opção 2: Manual
```bash
# 1. Clone o repositório
git clone https://github.com/charlierf/tcc-ata-ia.git
cd tcc-ata-ia

# 2. Criar ambiente virtual
python -m venv venv

# 3. Ativar ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# 4. Instalar dependências
pip install --upgrade pip
pip install -r requirements.txt

# 5. Verificar instalação
python src/setup.py
```

## ✅ Teste Básico

### 1. Teste sem downloads
```bash
cd src
python run_scraper.py --test
```

### 2. Download de teste (1 vídeo)
```bash
python run_scraper.py --download-limit 1
```

### 3. Ver estatísticas
```bash
python run_scraper.py --stats
```

## 🎯 Uso Regular

### Download completo
```bash
cd src
python run_scraper.py
```

### Com limites
```bash
# Buscar apenas 20 vídeos mais recentes
python run_scraper.py --limit 20

# Baixar no máximo 5 vídeos por execução
python run_scraper.py --download-limit 5
```

## 🔍 Solução de Problemas

### Erro: FFmpeg não encontrado
- Verifique se FFmpeg está no PATH do sistema
- Reinicie o terminal após instalar
- No Windows, pode ser necessário reiniciar o computador

### Erro: yt-dlp falha no download
- Verifique conexão com internet
- Alguns vídeos podem estar privados/removidos
- Tente novamente após alguns minutos

### Erro: Permissão negada
- Verifique permissões da pasta `data/`
- Execute como administrador se necessário

### Ambiente virtual não ativa
```bash
# Windows - se venv\Scripts\activate não funcionar:
venv\Scripts\Activate.ps1

# Se houver erro de política de execução:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## 📁 Estrutura de Arquivos

Após configuração bem-sucedida:
```
tcc-ata-ia/
├── venv/                     ← Ambiente virtual (não versionado)
├── data/raw/audio/           ← Áudios baixados
│   ├── consu/               ← Reuniões CONSU
│   ├── conepe/              ← Reuniões CONEPE
│   └── metadata.json        ← Metadados
├── src/                     ← Código fonte
└── scraper.log              ← Logs de execução
```

**✅ Corrigido:** O scraper agora detecta automaticamente o diretório raiz e salva os arquivos em `data/raw/audio/` independente de onde seja executado.

## 🎓 Para Desenvolvimento

### Ativar ambiente virtual (sempre)
```bash
# Antes de trabalhar no projeto:
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate
```

### Instalar novas dependências
```bash
# Instalar pacote
pip install nome-do-pacote

# Atualizar requirements.txt
pip freeze > requirements.txt
```

### Desativar ambiente virtual
```bash
deactivate
```

---

**💡 Dica:** Sempre ative o ambiente virtual antes de executar qualquer script do projeto!
