"""
Configurações do projeto TCC - Atas de Reunião com IA
===================================================

Este módulo contém as configurações centralizadas do projeto.

Autor: Charlie Rodrigues Fonseca
Data: 24/07/2025
"""

from pathlib import Path
import os

# Diretório base do projeto
BASE_DIR = Path(__file__).parent.parent.parent

# Estrutura de diretórios
class Directories:
    """Configuração centralizada dos diretórios do projeto."""
    
    # Diretórios principais
    BASE = BASE_DIR
    SRC = BASE / "src"
    DATA = BASE / "data"
    DOCS = BASE / "docs"
    MODELS = BASE / "models"
    NOTEBOOKS = BASE / "notebooks"
    EVALUATION = BASE / "evaluation"
    DIAGRAMS = BASE / "diagrams"
    
    # Subdiretórios de dados
    DATA_RAW = DATA / "raw"
    DATA_PROCESSED = DATA / "processed"
    DATA_TRANSCRICOES = DATA / "transcricoes"
    DATA_ATAS_GERADAS = DATA / "atas-geradas"
    
    # Diretórios de áudio
    AUDIO_RAW = DATA_RAW / "audio"
    AUDIO_CONSU = AUDIO_RAW / "consu"
    AUDIO_CONEPE = AUDIO_RAW / "conepe"
    
    # Diretórios de modelos
    MODELS_NER = MODELS / "ner"
    MODELS_SUMMARIZER = MODELS / "summarizer"
    MODELS_WHISPER = MODELS / "whisper"
    
    # Arquivos de configuração e metadados
    METADATA_FILE = AUDIO_RAW / "metadata.json"
    LOG_FILE = BASE / "scraper.log"

class YouTubeConfig:
    """Configurações específicas para o scraper do YouTube."""
    
    # URL do canal da TV UFS
    CHANNEL_URL = "https://www.youtube.com/@TVUFS/streams"
    
    # Padrões de nomenclatura dos vídeos
    TITLE_PATTERNS = {
        'main': r"Sala dos Conselhos\s*\|\s*(\d{2}/\d{2}/\d{4})\s*\|\s*Sessão\s+(CONEPE|CONSU)\s*\|\s*#(\d+)",
        'alternative': r"(\d{2}/\d{2}/\d{4}).*?(CONEPE|CONSU).*?#(\d+)"
    }
    
    # Configurações de download
    AUDIO_QUALITY = "192"  # kbps
    SAMPLE_RATE = "16000"  # Hz (ideal para speech recognition)
    CHANNELS = "1"         # Mono
    FORMAT = "wav"         # Formato de saída
    
    # Limites padrão
    DEFAULT_SEARCH_LIMIT = 100
    DEFAULT_DOWNLOAD_LIMIT = None  # Sem limite

class AudioConfig:
    """Configurações para processamento de áudio."""
    
    # Configurações de áudio para transcrição
    SAMPLE_RATE = 16000     # Hz
    CHANNELS = 1            # Mono
    BIT_DEPTH = 16          # bits
    
    # Configurações do Whisper (futura implementação)
    WHISPER_MODEL = "base"  # tiny, base, small, medium, large
    LANGUAGE = "pt"         # Português

class FileNaming:
    """Padrões de nomenclatura de arquivos."""
    
    # Formato para arquivos de áudio: AAAA-MM-DD_conselho_#numero.wav
    AUDIO_FORMAT = "{date}_{council}_#{number}.{extension}"
    
    # Formato para transcrições: AAAA-MM-DD_conselho_#numero_transcricao.txt
    TRANSCRIPT_FORMAT = "{date}_{council}_#{number}_transcricao.{extension}"
    
    # Formato para atas geradas: AAAA-MM-DD_conselho_#numero_ata.{format}
    ATA_FORMAT = "{date}_{council}_#{number}_ata.{extension}"
    
    @staticmethod
    def format_date(date_str: str) -> str:
        """
        Converte data de DD/MM/AAAA para AAAA-MM-DD.
        
        Args:
            date_str: Data no formato DD/MM/AAAA
            
        Returns:
            Data no formato AAAA-MM-DD
        """
        day, month, year = date_str.split('/')
        return f"{year}-{month}-{day}"
    
    @staticmethod
    def get_audio_filename(date_str: str, council: str, number: str) -> str:
        """
        Gera nome de arquivo para áudio.
        
        Args:
            date_str: Data no formato DD/MM/AAAA
            council: Nome do conselho (consu ou conepe)
            number: Número da sessão
            
        Returns:
            Nome do arquivo formatado
        """
        formatted_date = FileNaming.format_date(date_str)
        return FileNaming.AUDIO_FORMAT.format(
            date=formatted_date,
            council=council.lower(),
            number=number,
            extension="wav"
        )

def ensure_directories():
    """Cria todos os diretórios necessários do projeto."""
    dirs_to_create = [
        Directories.DATA_RAW,
        Directories.DATA_PROCESSED,
        Directories.DATA_TRANSCRICOES,
        Directories.DATA_ATAS_GERADAS,
        Directories.AUDIO_CONSU,
        Directories.AUDIO_CONEPE,
        Directories.MODELS_NER,
        Directories.MODELS_SUMMARIZER,
        Directories.MODELS_WHISPER,
    ]
    
    for directory in dirs_to_create:
        directory.mkdir(parents=True, exist_ok=True)
    
    return dirs_to_create

def get_project_info():
    """Retorna informações básicas do projeto."""
    return {
        "name": "TCC - Geração Automatizada de Atas de Reunião com IA",
        "author": "Charlie Rodrigues Fonseca",
        "institution": "UFS - Universidade Federal de Sergipe",
        "department": "DCOMP - Departamento de Computação",
        "advisor": "Prof. Dr. Hendrik Macedo",
        "year": "2025",
        "base_dir": str(Directories.BASE),
        "version": "1.0.0"
    }

if __name__ == "__main__":
    # Teste das configurações
    print("=== Configurações do Projeto ===")
    info = get_project_info()
    for key, value in info.items():
        print(f"{key}: {value}")
    
    print("\n=== Diretórios ===")
    created_dirs = ensure_directories()
    for directory in created_dirs:
        exists = "✅" if directory.exists() else "❌"
        print(f"{exists} {directory}")
    
    print(f"\n=== Exemplo de Nomenclatura ===")
    exemplo_data = "21/07/2025"
    exemplo_conselho = "CONEPE"
    exemplo_numero = "63"
    
    filename = FileNaming.get_audio_filename(exemplo_data, exemplo_conselho, exemplo_numero)
    print(f"Arquivo de áudio: {filename}")
    print(f"Caminho completo: {Directories.AUDIO_CONEPE / filename}")
