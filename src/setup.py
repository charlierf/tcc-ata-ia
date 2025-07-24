#!/usr/bin/env python3
"""
Script de configuração e verificação do ambiente do projeto
==========================================================

Este script verifica e configura o ambiente necessário para executar
o scraper de áudios das reuniões CONSU e CONEPE.

Autor: Charlie Rodrigues Fonseca
Data: 24/07/2025
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def check_python_version():
    """Verifica se a versão do Python é adequada."""
    print("🐍 Verificando versão do Python...")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python {version.major}.{version.minor} não é suportado")
        print("   É necessário Python 3.8 ou superior")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
    return True


def check_ffmpeg():
    """Verifica se FFmpeg está instalado."""
    print("\n🎬 Verificando FFmpeg...")
    
    if shutil.which("ffmpeg"):
        try:
            result = subprocess.run(
                ["ffmpeg", "-version"], 
                capture_output=True, 
                text=True, 
                timeout=10
            )
            if result.returncode == 0:
                # Extrair versão do FFmpeg
                version_line = result.stdout.split('\n')[0]
                print(f"✅ {version_line}")
                return True
        except subprocess.TimeoutExpired:
            print("⚠️  FFmpeg responde lentamente")
            return True
        except Exception:
            pass
    
    print("❌ FFmpeg não encontrado")
    print("   Instale o FFmpeg:")
    print("   - Windows: winget install FFmpeg")
    print("   - Linux: sudo apt install ffmpeg")
    print("   - macOS: brew install ffmpeg")
    return False


def check_git():
    """Verifica se Git está disponível."""
    print("\n🗂️  Verificando Git...")
    
    if shutil.which("git"):
        try:
            result = subprocess.run(
                ["git", "--version"], 
                capture_output=True, 
                text=True, 
                timeout=5
            )
            if result.returncode == 0:
                version = result.stdout.strip()
                print(f"✅ {version}")
                return True
        except Exception:
            pass
    
    print("⚠️  Git não encontrado (opcional)")
    return False


def create_directories():
    """Cria a estrutura de diretórios do projeto."""
    print("\n📁 Criando estrutura de diretórios...")
    
    base_dir = Path(__file__).parent.parent
    
    directories = [
        "data/raw/audio/consu",
        "data/raw/audio/conepe", 
        "data/processed",
        "data/transcricoes",
        "data/atas-geradas",
        "models/ner",
        "models/summarizer", 
        "models/whisper"
    ]
    
    created_count = 0
    for dir_path in directories:
        full_path = base_dir / dir_path
        if not full_path.exists():
            full_path.mkdir(parents=True, exist_ok=True)
            created_count += 1
            print(f"   📁 Criado: {dir_path}")
        else:
            print(f"   ✅ Existe: {dir_path}")
    
    if created_count > 0:
        print(f"✅ {created_count} diretórios criados")
    else:
        print("✅ Todos os diretórios já existem")
    
    return True


def test_imports():
    """Testa se as principais dependências podem ser importadas."""
    print("\n🧪 Testando imports...")
    
    test_packages = [
        ("yt_dlp", "yt-dlp"),
        ("requests", "requests"),
        ("pathlib", "pathlib (built-in)"),
    ]
    
    all_ok = True
    for package, display_name in test_packages:
        try:
            __import__(package)
            print(f"   ✅ {display_name}")
        except ImportError:
            print(f"   ❌ {display_name} - Execute: pip install -r requirements.txt")
            all_ok = False
    
    return all_ok


def main():
    """Função principal do script de setup."""
    print("🚀 Verificação do Ambiente - TCC Atas de Reunião")
    print("=" * 50)
    
    success_count = 0
    total_checks = 4
    
    # Verificações essenciais
    if check_python_version():
        success_count += 1
    
    ffmpeg_ok = check_ffmpeg()
    if ffmpeg_ok:
        success_count += 1
    
    if create_directories():
        success_count += 1
    
    if test_imports():
        success_count += 1
    
    # Resultado final
    print("\n" + "=" * 50)
    print("📊 RESULTADO DA VERIFICAÇÃO")
    print(f"✅ {success_count}/{total_checks} verificações passaram")
    
    if success_count == total_checks:
        print("\n🎉 Ambiente configurado corretamente!")
        print("\nPróximos passos:")
        print("1. cd src")
        print("2. python run_scraper.py --test")
        print("3. python run_scraper.py --download-limit 1")
        
    elif not ffmpeg_ok:
        print("\n❗ FFmpeg é obrigatório para o projeto funcionar")
        print("   Instale seguindo as instruções em INSTALACAO.md")
        
    else:
        print("\n❌ Alguns problemas precisam ser resolvidos")
        print("   Verifique as mensagens acima")
    
    return success_count == total_checks


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
