# 📝 Geração Automatizada de Atas de Reunião com IA – TCC UFS

Este repositório contém o projeto de Trabalho de Conclusão de Curso (TCC) de **Charlie Rodrigues Fonseca** no curso de Ciência da Computação da Universidade Federal de Sergipe (UFS), orientado pelo Prof. Dr. Hendrik Macedo.

O objetivo central do projeto é o desenvolvimento de uma **solução institucional de código aberto** capaz de **gerar atas de reuniões automaticamente** a partir de áudios gravados, utilizando técnicas de **Inteligência Artificial**, como transcrição automática, identificação de entidades nomeadas e geração de texto com modelos de linguagem (LLMs).

---

## 🎯 Objetivos

- **Sistema principal:** Desenvolver uma aplicação que receba áudios de reuniões da UFS e gere atas automaticamente
- **Processamento de áudio:** Transcrever automaticamente reuniões gravadas (CONSU e CONEPE)
- **Geração de atas:** Utilizar IA generativa para produzir atas institucionais compatíveis com o padrão oficial da UFS
- **Solução institucional:** Garantir uma solução **open source**, **on-premise** e **respeitosa às restrições de segurança e privacidade**
- **Avaliação de qualidade:** Avaliar a qualidade das atas geradas com base em métricas objetivas e comparação com atas reais

---

## 🧠 Sistema de Geração de Atas

### 🔧 **Arquitetura do Sistema**
```
📤 Upload de Áudio → 🎧 Transcrição (Whisper) → 🏷️ NER → 📝 Sumarização → 📄 Ata Final
```

### 🎯 **Componentes Principais**
- **Interface de Upload:** API/Web para receber arquivos de áudio
- **Módulo de Transcrição:** Whisper ou equivalente para conversão áudio→texto  
- **Processamento de Linguagem:** NER e análise semântica do conteúdo
- **Gerador de Atas:** LLM para estruturar e formatar atas oficiais
- **Sistema de Avaliação:** Métricas de qualidade e validação

### 🛠️ **Tecnologias Definidas**
- **Transcrição de áudio:** Whisper (OpenAI) - 16kHz mono WAV
- **Modelos de sumarização:** DistilBART, T5-small para português brasileiro
- **NER:** BERTimbau para reconhecimento de entidades em português
- **Infraestrutura:** Python, FastAPI, interface web responsiva
- **Armazenamento:** Sistema de arquivos local (on-premise)

---

## 📁 Estrutura do Projeto

```
📁 tcc-ata-ia/
├── 📄 README.md
├── 📄 requirements.txt
├── 📁 src/
│   ├── 📁 core/                 # Sistema principal de geração de atas
│   │   ├── 📄 __init__.py
│   │   ├── 📄 transcriber.py    # Módulo de transcrição (Whisper)
│   │   ├── 📄 ner_processor.py  # Reconhecimento de entidades
│   │   ├── 📄 summarizer.py     # Geração de atas
│   │   └── 📄 api.py           # API principal do sistema
│   ├── 📁 utils/               # Utilitários auxiliares
│   │   ├── 📄 audio_processor.py
│   │   ├── 📄 file_handler.py
│   │   └── 📄 validators.py
│   └── 📁 config/
│       └── 📄 project_config.py
├── 📁 data/
│   ├── 📁 raw/                 # Áudios originais
│   ├── 📁 transcricoes/        # Transcrições geradas
│   ├── 📁 atas-geradas/        # Atas produzidas pelo sistema
│   └── 📁 processed/           # Dados processados
├── 📁 models/
│   ├── 📁 whisper/             # Modelos de transcrição
│   ├── 📁 ner/                 # Modelos de NER
│   └── 📁 summarizer/          # Modelos de sumarização
├── 📁 notebooks/               # Análises e experimentos
├── 📁 evaluation/              # Métricas e avaliação
├── 📁 docs/                    # Documentação do TCC
├── 📁 diagrams/                # Diagramas de arquitetura
└── 📁 tools/                   # Ferramentas auxiliares
    ├── 📄 youtube_scraper.py   # Coleta de dados do YouTube
    └── 📄 run_scraper.py       # CLI do scraper
```

### 🎯 Fluxo de Desenvolvimento

1. **🔧 Sistema Core** (`src/core/`): Desenvolvimento da aplicação principal de upload e geração de atas
2. **🤖 Modelos** (`models/`): Configuração e otimização dos modelos de IA (Whisper, NER, Sumarização)
3. **📊 Avaliação** (`evaluation/`): Métricas de qualidade e comparação com atas reais
4. **🛠️ Ferramentas Auxiliares** (`tools/`): YouTube scraper para coleta inicial de dados

---

## 🗂️ Estrutura do Repositório

```plaintext
tcc-ata-ia/
│
├── docs/                     ← Documentação do TCC e referencias científicas
├── src/                      ← Sistema principal de geração de atas
│   ├── ata_generator/        ← Módulo principal do sistema
│   ├── models/              ← Interfaces para modelos de IA
│   ├── api/                 ← Interface web/API para upload
│   ├── utils/               ← Utilitários e ferramentas auxiliares
│   └── tools/               ← Ferramentas de desenvolvimento (scraper, etc.)
├── data/                     ← Dados para desenvolvimento e testes
│   ├── raw/audio/           ← Áudios coletados (dados de treino/teste)
│   ├── processed/           ← Áudios processados e normalizados
│   ├── transcricoes/        ← Transcrições geradas
│   └── atas-geradas/        ← Atas produzidas pelo sistema
├── models/                   ← Modelos locais de IA
│   ├── whisper/             ← Modelos de transcrição
│   ├── summarizer/          ← Modelos de sumarização
│   └── ner/                 ← Modelos de reconhecimento de entidades
├── notebooks/                ← Análises exploratórias e experimentos
├── evaluation/               ← Scripts de avaliação e métricas
├── tests/                    ← Testes automatizados do sistema
└── deployment/               ← Configurações para deploy institucional
````

---

## 🧪 Dados para Validação e Testes

As gravações utilizadas são reuniões reais dos Conselhos Superiores da UFS (CONSU e Conepe), extraídas de fontes públicas do [canal da TV UFS no YouTube](https://www.youtube.com/@TVUFS/streams), e servirão como **material de teste, validação e avaliação da solução desenvolvida**.

### 📥 Ferramenta Auxiliar: Scraper de Dados

O projeto inclui um **scraper automatizado** para coleta inicial de dados de reuniões do YouTube:

- **Propósito:** Coleta de dados para treinamento, teste e validação
- **Fonte:** Canal TV UFS - Transmissões ao vivo das reuniões
- **Padrão de títulos:** `"Sala dos Conselhos | DD/MM/AAAA | Sessão CONSELHO | #XX"`
- **Formato de saída:** WAV, 16kHz, Mono (otimizado para transcrição)
- **Organização:** Arquivos categorizados por conselho e data

> ⚠️ **Nota:** O scraper é uma ferramenta auxiliar para coleta de dados de teste. O sistema principal permite upload de qualquer arquivo de áudio de reuniões da UFS.

#### 🚀 Como usar o scraper:

**📖 Primeiro:** Siga o [Guia de Instalação](INSTALACAO.md) para configurar o ambiente virtual e dependências.

```bash
# 1. Configurar ambiente virtual (primeira vez)
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt

# 2. Verificar instalação
python src/setup.py

# 3. Teste básico (sem downloads)
python tools/run_scraper.py --test

# 4. Download de teste
python tools/run_scraper.py --download-limit 1

# 5. Execução completa
python tools/run_scraper.py

# 6. Ver estatísticas
python tools/run_scraper.py --stats
```
```

#### 📊 Estrutura dos dados coletados:

```
data/raw/audio/
├── consu/                    ← Reuniões do CONSU
│   ├── 2025-07-21_consu_#63.wav
│   └── 2025-06-30_consu_#62.wav
├── conepe/                   ← Reuniões do CONEPE  
│   ├── 2025-07-21_conepe_#63.wav
│   └── 2025-06-15_conepe_#62.wav
└── metadata.json             ← Metadados dos downloads
```

---

## 📄 Documentação do TCC

O desenvolvimento está dividido em duas etapas:

* **TCC1:** Revisão sistemática, proposta de arquitetura, definição de escopo e tecnologias.
* **TCC2:** Desenvolvimento do sistema, testes, avaliação de resultados e escrita final da monografia.

### 📚 Fundamentação Científica

O projeto mantém uma base sólida de **artigos científicos** para fundamentar todas as decisões técnicas:

```bash
# Gerenciar artigos científicos
python src/utils/article_manager.py setup    # Configurar estrutura
python src/utils/article_manager.py list     # Listar artigos prioritários
python src/utils/article_manager.py search whisper  # Buscar artigo específico
```

**Artigos prioritários:**
- **Whisper (Radford et al., 2022)** - Fundamenta configurações de áudio 16kHz
- **BERTimbau (Souza et al., 2020)** - NLP em português brasileiro
- **ROUGE (Lin, 2004)** - Métricas de avaliação para sumarização

📁 **Localização:** `docs/referencias/` - Artigos organizados por categoria (ASR, NLP, Evaluation)

---

## 📫 Contato

Desenvolvido por [Charlie Fonseca](mailto:dev@charliefonseca.com.br)

---

**UFS - Universidade Federal de Sergipe**
**Departamento de Computação – DCOMP**
2025
