# 🎯 Sistema de Geração Automática de Atas - UFS

## Demonstração Interativa para Conselho Universitário

Este sistema implementa uma solução completa de IA para automatização da geração de atas de reunião, desenvolvido especificamente para a Universidade Federal de Sergipe (UFS).

## 🚀 Funcionalidades

- ✅ **Upload de áudio** - Suporte a arquivos .mp3, .wav, .m4a
- ✅ **Diarização automática** - Separação e identificação de speakers
- ✅ **Transcrição precisa** - Conversão áudio → texto com Whisper AI
- ✅ **Geração de ata** - Criação automática de ata estruturada
- ✅ **Interface amigável** - Demonstração visual completa via Gradio
- ✅ **Estatísticas detalhadas** - Tempo de fala por participante
- ✅ **Formato profissional** - Ata adequada para uso oficial

## 📋 Requisitos

### Software
- Python 3.8+
- GPU NVIDIA (recomendado) ou CPU
- Conexão com internet

### APIs
- **OpenAI API** - Para geração da ata com GPT
- **Hugging Face** - Para modelos de diarização (pyannote)

## 🛠️ Instalação

### 1. Clone o repositório
```bash
git clone https://github.com/charlierf/tcc-ata-ia.git
cd tcc-ata-ia
```

### 2. Instale as dependências
```bash
pip install -r requirements.txt

# Dependências específicas da demo
pip install gradio
pip install git+https://github.com/openai/whisper.git
pip install openai
pip install pyannote.audio
pip install torch torchvision torchaudio
pip install pydub
```

### 3. Configure as APIs

#### OpenAI API Key
```bash
# Opção 1: Variável de ambiente
export OPENAI_API_KEY="sua-chave-openai-aqui"

# Opção 2: Via parâmetro na execução
python tools/ata_demo.py --api-key "sua-chave-openai-aqui"
```

#### Hugging Face (pyannote)
1. Acesse: https://huggingface.co/pyannote/speaker-diarization
2. Aceite os termos de uso
3. Configure o token (se necessário):
```bash
huggingface-cli login
```

## 🚀 Como Executar

### Opção 1: Interface Python (Recomendada)
```bash
cd tools
python ata_demo.py --api-key "SUA_CHAVE_OPENAI"
```

### Opção 2: Notebook Jupyter
1. Abra: `notebooks/ata_ia_demo.ipynb`
2. Configure a chave da OpenAI na célula apropriada
3. Execute todas as células em ordem

### Parâmetros de Execução
```bash
python ata_demo.py --help

# Opções:
--api-key        # Chave da OpenAI API
--port 7860      # Porta do servidor (padrão: 7860)
--no-share       # Não criar link público
```

## 🎨 Como Usar a Interface

1. **Inicie a aplicação** seguindo as instruções acima
2. **Acesse o link** exibido no terminal (ex: http://localhost:7860)
3. **Faça upload** de um arquivo de áudio
4. **Clique em "Processar Áudio"** e aguarde
5. **Visualize os resultados** nas abas:
   - 📊 **Status & Estatísticas** - Informações gerais e participação
   - 🎤 **Transcrição** - Texto completo da reunião
   - 📋 **Ata Gerada** - Documento final estruturado

## 📁 Formatos de Áudio Suportados

| Formato | Extensão | Qualidade | Observações |
|---------|----------|-----------|-------------|
| WAV | `.wav` | Excelente | Melhor qualidade, arquivos grandes |
| MP3 | `.mp3` | Boa | Formato mais comum, compactado |
| M4A | `.m4a` | Boa | Formato do iPhone/iOS |

## 🏗️ Arquitetura do Sistema

```
📁 Audio Input (.mp3, .wav, .m4a)
    ↓
🎭 Speaker Diarization (pyannote.audio)
    ↓
🎤 Speech-to-Text (Whisper AI)
    ↓
📊 Statistics Generation (Python)
    ↓
📝 Meeting Minutes Generation (OpenAI GPT)
    ↓
📋 Formatted Output (Markdown)
```

## 🔧 Tecnologias Utilizadas

- **[Whisper AI](https://github.com/openai/whisper)** - Transcrição de áudio
- **[PyAnnote Audio](https://github.com/pyannote/pyannote-audio)** - Diarização de speakers
- **[OpenAI GPT](https://openai.com/api/)** - Geração de ata estruturada
- **[Gradio](https://gradio.app/)** - Interface web interativa
- **[PyTorch](https://pytorch.org/)** - Framework de machine learning

## 📊 Métricas de Performance

### Precisão Esperada
- **Transcrição**: 85-95% (dependendo da qualidade do áudio)
- **Diarização**: 80-90% (reuniões com 2-6 participantes)
- **Geração de Ata**: 90-95% (estrutura e conteúdo)

### Tempos de Processamento
- **Áudio de 10 min**: ~3-5 minutos
- **Áudio de 30 min**: ~8-12 minutos  
- **Áudio de 60 min**: ~15-20 minutos

*Tempos variam conforme hardware (GPU vs CPU)*

## 📝 Exemplo de Saída

### Estatísticas Geradas
```
📊 Estatísticas da Reunião
Participantes identificados: 4
Duração da transcrição: 2.847 caracteres
Processado em: 07/08/2025 às 14:30:25

Participação por Speaker:
- SPEAKER_00: 45.2s (8 intervenções, 127 palavras)
- SPEAKER_01: 32.1s (12 intervenções, 98 palavras)  
- SPEAKER_02: 28.7s (6 intervenções, 89 palavras)
- SPEAKER_03: 51.4s (9 intervenções, 156 palavras)
```

### Ata Estruturada
```markdown
# ATA DE REUNIÃO

## CABEÇALHO
Data: 07 de Agosto de 2025
Participantes: 4 pessoas identificadas
Duração: Aproximadamente 15 minutos

## PAUTA
1. Discussão sobre implementação do sistema...
2. Análise dos resultados obtidos...
3. Próximos passos do projeto...

## DELIBERAÇÕES
- Aprovada a continuidade do projeto...
- Definidos os prazos para próxima fase...

## ENCAMINHAMENTOS
- Responsável A: Preparar relatório até 15/08
- Responsável B: Agendar próxima reunião...
```

## 🔒 Segurança e Privacidade

### Dados Processados
- ✅ Arquivos de áudio são processados **localmente**
- ✅ Apenas **transcrições** são enviadas para OpenAI
- ✅ Nenhum áudio original é enviado para serviços externos
- ✅ Resultados podem ser salvos localmente

### Recomendações
- Use em ambiente controlado para dados sensíveis
- Configure firewall adequadamente se expor publicamente
- Mantenha as APIs keys seguras

## 🐛 Solução de Problemas

### Erro: "OpenAI API Key não configurada"
```bash
# Configure a variável de ambiente
export OPENAI_API_KEY="sua-chave-aqui"
```

### Erro: "pyannote.audio não configurado" 
```bash
# Faça login no Hugging Face
huggingface-cli login
# Aceite os termos nos links mencionados
```

### Performance lenta
- Use GPU se disponível
- Reduza o tamanho do áudio
- Use modelo Whisper menor (`tiny` ou `base`)

### Problemas de memória
```bash
# Reduza o tamanho do modelo Whisper
whisper_model = whisper.load_model("base")  # ao invés de "small"
```

## 📞 Suporte

### Para Representantes da UFS
- Email: [seu-email@ufs.br]
- Demonstração agendada: [agendar link]
- Documentação técnica: `/docs/`

### Para Desenvolvedores
- Issues: https://github.com/charlierf/tcc-ata-ia/issues
- Documentação: `/docs/scraper-documentation.md`
- Testes: `/evaluation/`

## 📄 Licença

Este projeto foi desenvolvido como Trabalho de Conclusão de Curso (TCC) para a Universidade Federal de Sergipe.

---

**🎓 Desenvolvido para UFS - Conselho Universitário**  
**Tecnologia:** Whisper AI + PyAnnote + OpenAI GPT + Gradio  
**Objetivo:** Automatização de atas de reunião com IA
