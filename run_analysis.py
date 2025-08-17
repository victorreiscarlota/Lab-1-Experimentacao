#!/usr/bin/env python
import os
import sys
import subprocess

def check_environment():
    """Verifica se o ambiente virtual existe e está ativado"""
    if not os.path.exists("venv"):
        print("Ambiente virtual não encontrado. Criando...")
        try:
            if sys.platform == "win32":
                subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
            else:
                subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        except subprocess.CalledProcessError:
            print("Erro ao criar ambiente virtual.")
            return False
    
    # Verificar se estamos em um ambiente virtual
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("Ambiente virtual não está ativado.")
        print("\nPor favor, ative o ambiente virtual antes de executar este script:")
        if sys.platform == "win32":
            print("    venv\\Scripts\\activate")
        else:
            print("    source venv/bin/activate")
        return False
    
    return True

def install_requirements():
    """Instala os pacotes necessários do requirements.txt"""
    print("Instalando dependências...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        return True
    except subprocess.CalledProcessError:
        print("Erro ao instalar dependências.")
        return False

def check_token():
    """Verifica se o token do GitHub está configurado"""
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("\nToken do GitHub não configurado!")
        print("Por favor, defina a variável de ambiente GITHUB_TOKEN antes de executar o script.")
        if sys.platform == "win32":
            print("    set GITHUB_TOKEN=seu_token_aqui")
        else:
            print("    export GITHUB_TOKEN=seu_token_aqui")
        return False
    return True

def run_data_collection():
    """Executa o script de coleta de dados"""
    print("\nIniciando coleta de dados...")
    try:
        subprocess.run([sys.executable, "github_repos_data.py"], check=True)
        return True
    except subprocess.CalledProcessError:
        print("Erro durante a coleta de dados.")
        return False

def run_data_analysis():
    """Executa o script de análise de dados"""
    print("\nIniciando análise dos dados...")
    try:
        subprocess.run([sys.executable, "analyze_data.py"], check=True)
        return True
    except subprocess.CalledProcessError:
        print("Erro durante a análise dos dados.")
        return False

def main():
    """Função principal que orquestra o processo completo"""
    print("=== Laboratório 1 - Experimentação: Características de Repositórios Populares ===\n")
    
    # Verificar e configurar ambiente
    if not check_environment():
        return
    
    # Instalar dependências
    if not install_requirements():
        return
    
    # Verificar token do GitHub
    if not check_token():
        return
    
    # Menu de opções
    print("\nO que você deseja fazer?")
    print("1. Executar coleta de dados")
    print("2. Executar análise de dados")
    print("3. Executar coleta e análise de dados")
    print("4. Sair")
    
    choice = input("Escolha uma opção (1-4): ")
    
    if choice == '1':
        run_data_collection()
    elif choice == '2':
        run_data_analysis()
    elif choice == '3':
        if run_data_collection():
            run_data_analysis()
    elif choice == '4':
        print("Saindo...")
    else:
        print("Opção inválida!")

if __name__ == "__main__":
    main()