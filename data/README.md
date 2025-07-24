# 📂 Pasta `data` - Dados do Projeto

Esta pasta armazena todos os dados utilizados no projeto TCC, organizados por tipo e estágio de processamento.

## 🗂️ Estrutura de Organização

```plaintext
data/
├── raw/                      ← Dados brutos originais
│   └── audio/               ← Áudios das reuniões
│       ├── consu/           ← Reuniões do CONSU
│       ├── conepe/          ← Reuniões do CONEPE
│       └── metadata.json    ← Metadados dos downloads
├── processed/               ← Dados processados e limpos
├── transcricoes/           ← Transcrições dos áudios
└── atas-geradas/           ← Atas geradas automaticamente
```

## 🎵 Nomenclatura dos Arquivos de Áudio

Os arquivos de áudio seguem o padrão:
```
AAAA-MM-DD_conselho_#numero.wav
```

**Exemplos:**
- `2025-07-21_conepe_#63.wav` - Reunião CONEPE de 21/07/2025, sessão #63
- `2025-06-30_consu_#63.wav` - Reunião CONSU de 30/06/2025, sessão #63

## 📊 Metadados (metadata.json)

O arquivo `raw/audio/metadata.json` contém informações sobre todos os downloads:

```json
{
  "downloads": [
    {
      "video_id": "ID_do_YouTube",
      "title": "Título original do vídeo",
      "output_path": "Caminho do arquivo baixado",
      "download_date": "Data/hora do download",
      "conselho": "consu|conepe",
      "data_reuniao": "DD/MM/AAAA",
      "numero_sessao": "XX",
      "file_size_mb": 123.4
    }
  ],
  "last_update": "2025-07-24T10:30:00"
}
```

## 🔍 Padrões de Títulos dos Vídeos

O scraper busca vídeos com os seguintes padrões de título:
- `"Sala dos Conselhos | DD/MM/AAAA | Sessão CONEPE | #XX"`
- `"Sala dos Conselhos | DD/MM/AAAA | Sessão CONSU | #XX"`

## ⚙️ Configurações de Áudio

Os áudios são baixados com as seguintes especificações **cientificamente fundamentadas** para ASR (Automatic Speech Recognition):

- **Formato:** WAV (PCM sem compressão) - Preserva qualidade para análise científica
- **Sample Rate:** 16 kHz - Otimizado para modelos ASR modernos (Whisper, Wav2Vec2)¹²
- **Canais:** Mono (1 canal) - Eficiência computacional mantendo qualidade linguística
- **Bit Depth:** 16-bit PCM - Padrão para processamento de fala

### 📚 Fundamentação Científica

Esta configuração baseia-se em:

1. **Teorema de Nyquist:** 16kHz captura completamente o espectro da fala humana (85Hz-8kHz)
2. **Literatura ASR:** Modelos state-of-the-art otimizados para 16kHz (Radford et al., 2022)¹
3. **Eficiência computacional:** Redução de ~82% no tamanho vs 44.1kHz estéreo sem perda de qualidade
4. **Reprodutibilidade:** Formato determinístico para experimentos científicos

**Referências:**
1. Radford, A. et al. (2022). Robust Speech Recognition via Large-Scale Weak Supervision
2. Baevski, A. et al. (2020). wav2vec 2.0: A Framework for Self-Supervised Learning

## 📈 Estatísticas de Uso

Para verificar estatísticas dos downloads, execute:
```bash
cd src
python run_scraper.py --stats
```

## 🔄 Atualização dos Dados

Para baixar novos áudios das reuniões:
```bash
cd src
python run_scraper.py
```

## ⚠️ Considerações

1. **Espaço em disco:** Cada reunião pode ocupar 50-200 MB
2. **Conectividade:** Downloads requerem conexão estável com a internet
3. **FFmpeg:** Necessário ter FFmpeg instalado no sistema
4. **Backup:** Considere fazer backup dos áudios antes de processos intensivos

## 📋 Histórico de Mudanças

- **24/07/2025:** Estrutura inicial criada
- **24/07/2025:** Implementação do scraper YouTube
- **24/07/2025:** Sistema de metadados adicionado

---

**Nota:** Esta estrutura foi projetada para facilitar o processamento posterior com ferramentas de IA para transcrição e geração de atas.
