# 📂 Pasta `notebooks`

Esta pasta contém notebooks para análises exploratórias e testes com modelos de IA.

## Notebooks disponíveis

- [`ata_ia_demo.ipynb`](ata_ia_demo.ipynb) - **🎯 Sistema Completo com Interface Visual**  
  Demonstração interativa para UFS com interface Gradio integrada  
  [![Abrir no Google Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/charlierf/tcc-ata-ia/blob/main/notebooks/ata_ia_demo.ipynb)

- [`ata_ia_poc.ipynb`](ata_ia_poc.ipynb) - **POC Simplificada de Geração de Atas**  
  Pipeline otimizado: carregamento de áudio → diarização → transcrição → geração de ata com OpenAI API  
  [![Abrir no Google Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/charlierf/tcc-ata-ia/blob/main/notebooks/ata_ia_poc.ipynb)

- [`ssp_transcricao_entidades.ipynb`](ssp_transcricao_entidades.ipynb) - **Exemplo de Transcrição e NER**  
  Interface Gradio para processamento de áudios de ocorrências policiais

## 🎯 Demonstração para UFS

O notebook `ata_ia_demo.ipynb` é a **versão principal** para apresentação ao Conselho Universitário da UFS. Inclui:

- ✅ Interface visual completa com Gradio
- ✅ Upload de arquivos de áudio (.mp3, .wav, .m4a)
- ✅ Processamento automático com diarização
- ✅ Geração de ata estruturada com GPT
- ✅ Estatísticas detalhadas de participação
- ✅ Resultados organizados em abas interativas

**Alternativa standalone:** Execute diretamente com `python tools/ata_demo.py`

## Como usar

1. **Configure a API OpenAI** na célula apropriada
2. **Execute todas as células** em ordem
3. **Faça upload de um arquivo de áudio** na interface
4. **Visualize os resultados** nas abas da interface

Consulte o [`DEMO_README.md`](../DEMO_README.md) para instruções completas de instalação e uso.
