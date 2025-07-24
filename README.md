# 📝 Geração Automatizada de Atas de Reunião com IA – TCC UFS

Este repositório contém o projeto de Trabalho de Conclusão de Curso (TCC) de **Charlie Rodrigues Fonseca** no curso de Ciência da Computação da Universidade Federal de Sergipe (UFS), orientado pelo Prof. Dr. Hendrik Macedo.

O objetivo central do projeto é o desenvolvimento de uma **solução institucional de código aberto** capaz de **gerar atas de reuniões automaticamente** a partir de áudios gravados, utilizando técnicas de **Inteligência Artificial**, como transcrição automática, identificação de entidades nomeadas e geração de texto com modelos de linguagem (LLMs).

---

## 🎯 Objetivos

- Processar reuniões gravadas (ex: CONSU e Conepe) e transcrevê-las automaticamente.
- Utilizar IA generativa para **produzir atas institucionais compatíveis com o padrão oficial da UFS**.
- Garantir uma solução **open source**, **on-premise** e **respeitosa às restrições de segurança e privacidade** da instituição.
- Avaliar a qualidade das atas geradas com base em métricas objetivas e comparação com atas reais.

---

## 🧠 Tecnologias e Ferramentas

- **Transcrição de áudio:** a definir ([`whisper.cpp`](https://github.com/ggerganov/whisper.cpp), [`faster-whisper`](https://github.com/guillaumekln/faster-whisper))
- **Modelos de sumarização:** a definir (DistilBART, T5-small, Falcon, Mistral (quantizados e leves))
- **NER / análise semântica:** a definir (spaCy, BERT, token classification)
- **Infraestrutura:** a definir (Python, FastAPI (ou equivalente), scripts em notebooks)
- **Repositório de dados:** Reuniões públicas da UFS extraídas do YouTube

---

## 🗂️ Estrutura do Repositório

```plaintext
tcc-ata-ia/
│
├── docs/                     ← Documentos e monografia (TCC1 e TCC2)
├── data/                     ← Áudios, transcrições e atas geradas
├── notebooks/                ← Análises exploratórias e testes com IA
├── src/                      ← Código-fonte do sistema final
├── models/                   ← Modelos locais (transcrição, sumarização, NER)
├── evaluation/               ← Scripts de avaliação de qualidade da ata
├── diagrams/                 ← Arquitetura e fluxos da solução
├── README.md                 ← Este documento
├── requirements.txt          ← Dependências do projeto
└── .gitignore                ← Arquivos a serem ignorados no versionamento
````

---

## 🧪 Base de Dados

As gravações utilizadas são reuniões reais dos Conselhos Superiores da UFS (CONSU e Conepe), extraídas de fontes públicas do [canal da TV UFS no YouTube](https://www.youtube.com/@TVUFS/streams), e servirão como **material de teste, validação e avaliação da solução desenvolvida**.

### 📥 Coleta Automatizada de Dados

O projeto inclui um **scraper automatizado** que baixa os áudios das reuniões diretamente do YouTube:

- **Fonte:** Canal TV UFS - Transmissões ao vivo das reuniões
- **Padrão de títulos:** `"Sala dos Conselhos | DD/MM/AAAA | Sessão CONSELHO | #XX"`
- **Formato de saída:** WAV, 16kHz, Mono (otimizado para transcrição)
- **Organização:** Arquivos categorizados por conselho e data

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
python src/run_scraper.py --test

# 4. Download de teste
python src/run_scraper.py --download-limit 1

# 5. Execução completa
python src/run_scraper.py

# 6. Ver estatísticas
python src/run_scraper.py --stats
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
