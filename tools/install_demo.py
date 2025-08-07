#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Instalação Automática
Sistema de Geração Automática de Atas - UFS

Este script automatiza a instalação de todas as dependências necessárias
para executar o sistema de demonstração.
"""

import subprocess
import sys
import os
import platform

def run_command(command, description):
    """Executa um comando e mostra o progresso"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, 
                              capture_output=True, text=True)
        print(f"✅ {description} - Concluído!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro em {description}:")
        print(f"   {e.stderr}")
        return False

def check_python_version():
    """Verifica se a versão do Python é adequada"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ é necessário")
        print(f"   Versão atual: {version.major}.{version.minor}")
        return False
    print(f"✅ Python {version.major}.{version.minor} - OK!")
    return True

def install_torch():
    """Instala PyTorch com suporte a GPU se disponível"""
    print("🔄 Instalando PyTorch...")
    
    # Detectar se tem GPU NVIDIA
    try:
        result = subprocess.run("nvidia-smi", capture_output=True, text=True)
        has_gpu = result.returncode == 0
    except:
        has_gpu = False
    
    if has_gpu:
        print("🎮 GPU NVIDIA detectada - instalando versão CUDA")
        command = "pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118"
    else:
        print("💾 Instalando versão CPU")
        command = "pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu"
    
    return run_command(command, "Instalação do PyTorch")

def main():
    """Função principal de instalação"""
    print("=" * 60)
    print("🎯 INSTALADOR - Sistema de Geração de Atas UFS")
    print("=" * 60)
    
    # Verificar Python
    if not check_python_version():
        sys.exit(1)
    
    # Lista de dependências para instalar
    dependencies = [
        ("pip install --upgrade pip", "Atualizando pip"),
        ("pip install gradio", "Instalando Gradio"),
        ("pip install openai", "Instalando OpenAI"),
        ("pip install git+https://github.com/openai/whisper.git", "Instalando Whisper"),
        ("pip install pyannote.audio", "Instalando PyAnnote Audio"),
        ("pip install pydub", "Instalando PyDub"),
        ("pip install datasets", "Instalando Datasets"),
        ("pip install transformers", "Instalando Transformers"),
    ]
    
    # Instalar PyTorch primeiro
    if not install_torch():
        print("❌ Falha na instalação do PyTorch")
        sys.exit(1)
    
    # Instalar outras dependências
    failed_installations = []
    
    for command, description in dependencies:
        if not run_command(command, description):
            failed_installations.append(description)
    
    # Resultados
    print("\n" + "=" * 60)
    if failed_installations:
        print("⚠️ INSTALAÇÃO CONCLUÍDA COM AVISOS")
        print("Falhas em:")
        for failed in failed_installations:
            print(f"  - {failed}")
        print("\nVocê pode tentar instalar manualmente:")
        print("pip install gradio openai pyannote.audio pydub")
    else:
        print("✅ INSTALAÇÃO CONCLUÍDA COM SUCESSO!")
    
    print("\n📋 PRÓXIMOS PASSOS:")
    print("1. Configure sua chave da OpenAI API:")
    print("   export OPENAI_API_KEY='sua-chave-aqui'")
    print("\n2. Faça login no Hugging Face:")
    print("   pip install huggingface_hub")
    print("   huggingface-cli login")
    print("\n3. Execute a demonstração:")
    print("   python tools/ata_demo.py")
    
    print("\n🔗 Links importantes:")
    print("- OpenAI API: https://platform.openai.com/api-keys")
    print("- Hugging Face: https://huggingface.co/pyannote/speaker-diarization")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
