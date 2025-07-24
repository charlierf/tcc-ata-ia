#!/usr/bin/env python3
"""
Script para criar e configurar ambiente virtual do projeto
========================================================

Este script automatiza a criação do ambiente virtual e instalação
das dependências necessárias para o projeto.

Uso:
    python criar_ambiente.py

Autor: Charlie Rodrigues Fonseca
Data: 24/07/2025
"""

import os
import sys
import subprocess
import platform
from pathlib import Path


def check_python_version():
    """Verifica se a versão do Python é adequada."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python {version.major}.{version.minor} não é suportado")
        print("   É necessário Python 3.8 ou superior")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True


def create_virtual_environment():
    """Cria o ambiente virtual."""
    base_dir = Path(__file__).parent
    venv_dir = base_dir / "venv"
    
    if venv_dir.exists():
        print("⚠️  Ambiente virtual já existe")
        return True
    
    print("📦 Criando ambiente virtual...")
    try:
        subprocess.run([sys.executable, "-m", "venv", "venv"], 
                      cwd=base_dir, check=True)
        print("✅ Ambiente virtual criado")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao criar ambiente virtual: {e}")
        return False


def get_activation_command():
    """Retorna o comando de ativação do ambiente virtual."""
    if platform.system() == "Windows":
        return "venv\\Scripts\\activate"
    else:
        return "source venv/bin/activate"


def get_pip_path():
    """Retorna o caminho do pip no ambiente virtual."""
    base_dir = Path(__file__).parent
    if platform.system() == "Windows":
        return base_dir / "venv" / "Scripts" / "pip"
    else:
        return base_dir / "venv" / "bin" / "pip"


def install_requirements():
    """Instala as dependências no ambiente virtual."""
    base_dir = Path(__file__).parent
    requirements_file = base_dir / "requirements.txt"
    pip_path = get_pip_path()
    
    if not requirements_file.exists():
        print(f"❌ Arquivo requirements.txt não encontrado")
        return False
    
    if not pip_path.exists():
        print(f"❌ Pip não encontrado no ambiente virtual")
        return False
    
    print("📋 Instalando dependências...")
    try:
        # Atualizar pip
        subprocess.run([str(pip_path), "install", "--upgrade", "pip"], 
                      check=True, capture_output=True)
        
        # Instalar requirements
        result = subprocess.run([str(pip_path), "install", "-r", str(requirements_file)], 
                               capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Dependências instaladas com sucesso")
            return True
        else:
            print("❌ Erro ao instalar dependências:")
            print(result.stderr)
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro durante instalação: {e}")
        return False


def main():
    """Função principal."""
    print("🚀 Configuração do Ambiente Virtual")
    print("=" * 40)
    
    # Verificar Python
    if not check_python_version():
        return False
    
    # Criar ambiente virtual
    if not create_virtual_environment():
        return False
    
    # Instalar dependências
    if not install_requirements():
        return False
    
    # Sucesso
    print("\n" + "=" * 40)
    print("🎉 Ambiente configurado com sucesso!")
    print("\n📝 Próximos passos:")
    print(f"1. Ativar o ambiente: {get_activation_command()}")
    print("2. Verificar instalação: python src/setup.py")
    print("3. Testar scraper: python src/run_scraper.py --test")
    
    if platform.system() == "Windows":
        print("\n💡 Dica Windows:")
        print("   Se houver erro de política de execução, execute:")
        print("   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser")
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
