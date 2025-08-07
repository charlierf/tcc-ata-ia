# Configuração do Sistema de Geração de Atas - UFS
# Copie este arquivo para config.py e configure suas chaves

# ===========================================
# CONFIGURAÇÕES DA API OPENAI
# ===========================================

# Sua chave da OpenAI API
# Obtenha em: https://platform.openai.com/api-keys
OPENAI_API_KEY = "your-openai-api-key-here"

# Modelo GPT a usar (opções: gpt-4, gpt-4-turbo, gpt-3.5-turbo, gpt-4o-mini)
OPENAI_MODEL = "gpt-4o-mini"

# Temperatura para geração (0.0-1.0, menor = mais conservador)
OPENAI_TEMPERATURE = 0.2

# Máximo de tokens para resposta
OPENAI_MAX_TOKENS = 3000

# ===========================================
# CONFIGURAÇÕES DO WHISPER
# ===========================================

# Modelo Whisper (tiny, base, small, medium, large)
# tiny = mais rápido, large = mais preciso
WHISPER_MODEL = "small"

# Idioma para transcrição (pt para português)
WHISPER_LANGUAGE = "pt"

# ===========================================
# CONFIGURAÇÕES DA DIARIZAÇÃO
# ===========================================

# Usar diarização (separação de speakers)
USE_DIARIZATION = True

# Modelo de diarização
DIARIZATION_MODEL = "pyannote/speaker-diarization@2.1"

# ===========================================
# CONFIGURAÇÕES DA INTERFACE
# ===========================================

# Porta para executar a interface
GRADIO_PORT = 7860

# Permitir acesso externo
GRADIO_SERVER_NAME = "0.0.0.0"

# Criar link público temporário (Gradio Share)
GRADIO_SHARE = True

# Modo debug
DEBUG_MODE = False

# ===========================================
# CONFIGURAÇÕES DE ARQUIVOS
# ===========================================

# Diretório para salvar resultados
OUTPUT_DIR = "../data/atas-geradas"

# Formatos de áudio aceitos
AUDIO_FORMATS = [".mp3", ".wav", ".m4a", ".flac"]

# Tamanho máximo de arquivo (MB)
MAX_FILE_SIZE_MB = 100

# ===========================================
# CONFIGURAÇÕES AVANÇADAS
# ===========================================

# Usar GPU se disponível
USE_GPU = True

# Número máximo de caracteres da transcrição para mostrar
MAX_TRANSCRIPTION_DISPLAY = 2000

# Salvar arquivos processados automaticamente
AUTO_SAVE_RESULTS = True

# Formato de timestamp para arquivos salvos
TIMESTAMP_FORMAT = "%Y%m%d_%H%M%S"

# ===========================================
# TEMPLATE DA ATA
# ===========================================

# Template personalizado para a ata (opcional)
ATA_TEMPLATE = """
Você é um assistente especializado em gerar atas de reunião para instituições acadêmicas brasileiras.

Crie uma ata formal seguindo este formato:

## ATA DE REUNIÃO

### IDENTIFICAÇÃO
- **Data:** [inferir da análise ou usar data atual]
- **Local:** [mencionar se identificado na transcrição]
- **Participantes:** [listar speakers identificados]

### PAUTA
[Principais tópicos discutidos, organizados por assunto]

### DESENVOLVIMENTO
[Resumo organizado das discussões, identificando pontos principais]

### DELIBERAÇÕES
[Decisões tomadas, votações, consensos alcançados]

### ENCAMINHAMENTOS
[Próximos passos, responsáveis, prazos definidos]

### OBSERVAÇÕES
[Informações adicionais relevantes]

Use linguagem formal acadêmica e seja preciso nas informações.
"""

# ===========================================
# INSTRUÇÕES DE USO
# ===========================================

"""
COMO USAR ESTE ARQUIVO:

1. Copie este arquivo para 'config.py':
   cp config_template.py config.py

2. Edite config.py e configure suas chaves:
   - OPENAI_API_KEY: Sua chave da OpenAI
   - Outras configurações conforme necessário

3. Execute o sistema:
   python ata_demo.py

OBTENÇÃO DE CHAVES:

OpenAI API Key:
- Acesse: https://platform.openai.com/api-keys
- Crie uma nova chave
- Cole em OPENAI_API_KEY acima

Hugging Face (para diarização):
- Acesse: https://huggingface.co/pyannote/speaker-diarization
- Aceite os termos de uso
- Execute: huggingface-cli login

MODELOS WHISPER:
- tiny: Mais rápido, menos preciso (~39 MB)
- base: Equilibrado (~74 MB)
- small: Boa qualidade (~244 MB)
- medium: Muito boa qualidade (~769 MB)
- large: Melhor qualidade (~1550 MB)

DICA: Comece com "small" para testes
"""
