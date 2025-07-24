# 📚 Referências Bibliográficas - Literatura Científica

Esta pasta contém os artigos científicos que fundamentam as decisões técnicas do projeto.

## 🗂️ Estrutura de Organização

```plaintext
docs/referencias/
├── asr/                      ← Automatic Speech Recognition
│   ├── whisper/             ← Modelo Whisper (OpenAI)
│   ├── wav2vec/             ← Wav2Vec2 (Meta/Facebook)
│   └── general/             ← ASR geral
├── nlp/                     ← Natural Language Processing
│   ├── summarization/       ← Sumarização de texto
│   ├── ner/                 ← Named Entity Recognition
│   └── llm/                 ← Large Language Models
├── evaluation/              ← Métricas e avaliação
└── related-work/            ← Trabalhos relacionados
```

## 📖 Artigos Principais

### 🎙️ **Automatic Speech Recognition (ASR)**

#### Whisper - OpenAI (2022)
- **Artigo:** "Robust Speech Recognition via Large-Scale Weak Supervision"
- **Autores:** Alec Radford, Jong Wook Kim, Tao Xu, Greg Brockman, Christine McLeavey, Ilya Sutskever
- **Relevância:** Modelo base para transcrição, justifica configuração 16kHz
- **Status:** 🔍 **BUSCAR** - Fundamental para o projeto

#### Wav2Vec2 - Meta (2020)
- **Artigo:** "wav2vec 2.0: A Framework for Self-Supervised Learning of Speech Representations"
- **Autores:** Alexei Baevski, Henry Zhou, Abdelrahman Mohamed, Michael Auli
- **Relevância:** Comparação com Whisper, fundamentação teórica ASR
- **Status:** 🔍 **BUSCAR** - Importante para comparações

### 🤖 **Natural Language Processing**

#### BART - Facebook (2019)
- **Artigo:** "BART: Denoising Sequence-to-Sequence Pre-training for Natural Language Generation, Translation, and Comprehension"
- **Autores:** Mike Lewis, Yinhan Liu, Naman Goyal, et al.
- **Relevância:** Modelo de sumarização, base para DistilBART
- **Status:** 🔍 **BUSCAR** - Para módulo de sumarização

#### T5 - Google (2019)
- **Artigo:** "Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer"
- **Autores:** Colin Raffel, Noam Shazeer, Adam Roberts, et al.
- **Relevância:** Alternativa para sumarização e geração de texto
- **Status:** 🔍 **BUSCAR** - Comparação de modelos

### 🏷️ **Named Entity Recognition**

#### SpaCy Portuguese Models
- **Documentação:** Models and datasets for Portuguese NER
- **Relevância:** Identificação de participantes, locais, datas nas atas
- **Status:** 🔍 **BUSCAR** - Documentação técnica

#### BERT for Portuguese
- **Artigo:** "BERTimbau: Portuguese BERT for Brazilian Portuguese"
- **Autores:** Fábio Souza, Rodrigo Nogueira, Roberto Lotufo
- **Relevância:** Modelo específico para português brasileiro
- **Status:** 🔍 **BUSCAR** - Importante para NER em português

### 📊 **Evaluation Metrics**

#### ROUGE for Summarization
- **Artigo:** "ROUGE: A Package for Automatic Evaluation of Summaries"
- **Autor:** Chin-Yew Lin
- **Relevância:** Métrica padrão para avaliação de sumarização
- **Status:** 🔍 **BUSCAR** - Essencial para avaliação

#### WER for ASR
- **Documentação:** Word Error Rate calculation and significance
- **Relevância:** Métrica padrão para avaliação de transcrição
- **Status:** 🔍 **BUSCAR** - Documentação técnica

## 🎯 **Prioridade de Busca**

### ⭐ **Alta Prioridade** (Fundamentais)
1. **Whisper (Radford et al., 2022)** - Base do projeto
2. **ROUGE (Lin, 2004)** - Avaliação de sumarização
3. **BERTimbau (Souza et al., 2020)** - NLP em português

### 🔥 **Média Prioridade** (Importantes)
4. **Wav2Vec2 (Baevski et al., 2020)** - Comparação ASR
5. **BART (Lewis et al., 2019)** - Sumarização
6. **T5 (Raffel et al., 2019)** - Alternativa de sumarização

### 📚 **Baixa Prioridade** (Complementares)
7. Trabalhos relacionados sobre atas automáticas
8. Estudos de caso institucionais
9. Métricas específicas de domínio

## 🔍 **Onde Buscar**

### Bases de Dados Acadêmicas
- **arXiv.org** - Pré-prints (acesso livre)
- **Google Scholar** - Busca ampla
- **IEEE Xplore** - Conferências técnicas
- **ACL Anthology** - NLP específico
- **Portal CAPES** - Via UFS (acesso institucional)

### Repositórios Específicos
- **Papers With Code** - Artigos com implementações
- **Hugging Face Papers** - Modelos e documentação
- **OpenAI Research** - Artigos da OpenAI
- **Meta Research** - Artigos da Meta/Facebook

## 📝 **Como Usar**

1. **Baixar PDFs** e salvar nas subpastas apropriadas
2. **Nomear arquivos:** `autor_ano_titulo-curto.pdf`
3. **Criar resumos:** Para cada artigo, criar um `.md` com resumo
4. **Citar no TCC:** Usar referências completas na monografia

### Exemplo de Estrutura:
```
docs/referencias/asr/whisper/
├── radford_2022_robust-speech-recognition.pdf
├── radford_2022_resumo.md
└── whisper_technical_specs.md
```

## 🎓 **Importância para o TCC**

### **Credibilidade Científica**
- Fundamenta escolhas técnicas com literatura peer-reviewed
- Demonstra conhecimento do estado da arte
- Permite comparações metodológicas válidas

### **Metodologia Robusta**
- Justifica configurações específicas (16kHz, mono, WAV)
- Embasa métricas de avaliação (ROUGE, WER)
- Suporta decisões arquiteturais

### **Contribuição Original**
- Identifica gaps na literatura
- Posiciona o trabalho no contexto científico
- Facilita discussão de resultados

---

**Próximos passos:**
1. Buscar artigos marcados como "BUSCAR"
2. Criar resumos executivos
3. Integrar citações no texto do TCC
4. Manter bibliografia atualizada
