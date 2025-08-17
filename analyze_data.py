import matplotlib
matplotlib.use('Agg')  

import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from datetime import datetime
import os

def load_data(filename="repositories_data.json"):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
            print(f"Carregados dados de {len(data)} repositórios.")
            return data
    except Exception as e:
        print(f"Erro ao carregar arquivo de dados: {str(e)}")
        return []

def analyze_repository_age(data):
    """RQ 01. Sistemas populares são maduros/antigos?"""
    ages = [repo["age_days"] for repo in data]
    ages_years = [age / 365 for age in ages]
    
    plt.figure(figsize=(10, 6))
    plt.hist(ages_years, bins=20, color='skyblue', edgecolor='black')
    plt.xlabel('Idade do Repositório (anos)')
    plt.ylabel('Número de Repositórios')
    plt.title('Distribuição da Idade dos Repositórios Populares')
    plt.grid(axis='y', alpha=0.75)
    plt.tight_layout()
    
    os.makedirs("resultados", exist_ok=True)
    plt.savefig('resultados/rq01_repository_age.png')
    plt.close() 
    
    avg_age = sum(ages) / len(ages)
    median_age = sorted(ages)[len(ages) // 2]
    
    print(f"RQ 01: Sistemas populares são maduros/antigos?")
    print(f"Idade média dos repositórios: {avg_age / 365:.2f} anos ({avg_age:.0f} dias)")
    print(f"Mediana da idade: {median_age / 365:.2f} anos ({median_age:.0f} dias)")
    print()

def analyze_external_contributions(data):
    """RQ 02. Sistemas populares recebem muita contribuição externa?"""
    prs = [repo["merged_pull_requests"] for repo in data]
    
    plt.figure(figsize=(10, 6))
    plt.hist(prs, bins=20, color='green', edgecolor='black')
    plt.xlabel('Número de Pull Requests Aceitas')
    plt.ylabel('Número de Repositórios')
    plt.title('Distribuição de Pull Requests Aceitas em Repositórios Populares')
    plt.grid(axis='y', alpha=0.75)
    plt.tight_layout()
    plt.savefig('resultados/rq02_pull_requests.png')
    plt.close()
    
    avg_prs = sum(prs) / len(prs)
    median_prs = sorted(prs)[len(prs) // 2]
    
    print(f"RQ 02: Sistemas populares recebem muita contribuição externa?")
    print(f"Média de pull requests aceitas: {avg_prs:.0f}")
    print(f"Mediana de pull requests aceitas: {median_prs:.0f}")
    print()

def analyze_releases(data):
    """RQ 03. Sistemas populares lançam releases com frequência?"""
    releases = [repo["releases_count"] for repo in data]
    
    plt.figure(figsize=(10, 6))
    plt.hist(releases, bins=20, color='orange', edgecolor='black')
    plt.xlabel('Número de Releases')
    plt.ylabel('Número de Repositórios')
    plt.title('Distribuição do Número de Releases em Repositórios Populares')
    plt.grid(axis='y', alpha=0.75)
    plt.tight_layout()
    plt.savefig('resultados/rq03_releases.png')
    plt.close()
    
    avg_releases = sum(releases) / len(releases)
    median_releases = sorted(releases)[len(releases) // 2]
    
    print(f"RQ 03: Sistemas populares lançam releases com frequência?")
    print(f"Média de releases: {avg_releases:.2f}")
    print(f"Mediana de releases: {median_releases:.0f}")
    print()

def analyze_update_frequency(data):
    """RQ 04. Sistemas populares são atualizados com frequência?"""
    days_since_update = [repo["days_since_last_update"] for repo in data]
    
    plt.figure(figsize=(10, 6))
    plt.hist(days_since_update, bins=20, color='red', edgecolor='black')
    plt.xlabel('Dias desde a última atualização')
    plt.ylabel('Número de Repositórios')
    plt.title('Tempo desde a Última Atualização em Repositórios Populares')
    plt.grid(axis='y', alpha=0.75)
    plt.tight_layout()
    plt.savefig('resultados/rq04_last_update.png')
    plt.close()
    
    avg_days = sum(days_since_update) / len(days_since_update)
    median_days = sorted(days_since_update)[len(days_since_update) // 2]
    
    print(f"RQ 04: Sistemas populares são atualizados com frequência?")
    print(f"Média de dias desde a última atualização: {avg_days:.2f}")
    print(f"Mediana de dias desde a última atualização: {median_days:.0f}")
    print()

def analyze_languages(data):
    """RQ 05. Sistemas populares são escritos nas linguagens mais populares?"""
    languages = [repo["language"] for repo in data]
    language_counts = {}
    
    for lang in languages:
        if lang in language_counts:
            language_counts[lang] += 1
        else:
            language_counts[lang] = 1
    
    sorted_langs = sorted(language_counts.items(), key=lambda x: x[1], reverse=True)
    top_languages = sorted_langs[:10]
    
    labels = [lang for lang, count in top_languages]
    counts = [count for lang, count in top_languages]
    
    plt.figure(figsize=(12, 8))
    plt.bar(labels, counts, color='purple')
    plt.xlabel('Linguagem de Programação')
    plt.ylabel('Número de Repositórios')
    plt.title('Top 10 Linguagens em Repositórios Populares')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('resultados/rq05_languages.png')
    plt.close()
    
    print(f"RQ 05: Sistemas populares são escritos nas linguagens mais populares?")
    print("Top 10 linguagens mais utilizadas:")
    for i, (lang, count) in enumerate(top_languages, 1):
        print(f"{i}. {lang}: {count} repositórios ({count/len(data)*100:.1f}%)")
    print()

def analyze_closed_issues(data):
    """RQ 06. Sistemas populares possuem um alto percentual de issues fechadas?"""
    ratios = [repo["issues_closed_ratio"] for repo in data]
    ratios_percent = [ratio * 100 for ratio in ratios]
    
    plt.figure(figsize=(10, 6))
    plt.hist(ratios_percent, bins=20, color='blue', edgecolor='black')
    plt.xlabel('Percentual de Issues Fechadas (%)')
    plt.ylabel('Número de Repositórios')
    plt.title('Distribuição do Percentual de Issues Fechadas em Repositórios Populares')
    plt.grid(axis='y', alpha=0.75)
    plt.tight_layout()
    plt.savefig('resultados/rq06_closed_issues.png')
    plt.close()
    
    avg_ratio = sum(ratios) / len(ratios)
    median_ratio = sorted(ratios)[len(ratios) // 2]
    
    print(f"RQ 06: Sistemas populares possuem um alto percentual de issues fechadas?")
    print(f"Média do percentual de issues fechadas: {avg_ratio*100:.2f}%")
    print(f"Mediana do percentual de issues fechadas: {median_ratio*100:.2f}%")
    print()

def save_summary(data, filename="resultados/sumario_resultados.txt"):
    """Salva um resumo dos resultados em um arquivo de texto"""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write("RESUMO DA ANÁLISE DE REPOSITÓRIOS POPULARES DO GITHUB\n")
        f.write("====================================================\n\n")
        
        # RQ 01: Idade
        ages = [repo["age_days"] for repo in data]
        avg_age = sum(ages) / len(ages)
        median_age = sorted(ages)[len(ages) // 2]
        f.write("RQ 01: Sistemas populares são maduros/antigos?\n")
        f.write(f"- Idade média dos repositórios: {avg_age / 365:.2f} anos ({avg_age:.0f} dias)\n")
        f.write(f"- Mediana da idade: {median_age / 365:.2f} anos ({median_age:.0f} dias)\n\n")
        
        # RQ 02: PRs
        prs = [repo["merged_pull_requests"] for repo in data]
        avg_prs = sum(prs) / len(prs)
        median_prs = sorted(prs)[len(prs) // 2]
        f.write("RQ 02: Sistemas populares recebem muita contribuição externa?\n")
        f.write(f"- Média de pull requests aceitas: {avg_prs:.0f}\n")
        f.write(f"- Mediana de pull requests aceitas: {median_prs:.0f}\n\n")
        
        # RQ 03: Releases
        releases = [repo["releases_count"] for repo in data]
        avg_releases = sum(releases) / len(releases)
        median_releases = sorted(releases)[len(releases) // 2]
        f.write("RQ 03: Sistemas populares lançam releases com frequência?\n")
        f.write(f"- Média de releases: {avg_releases:.2f}\n")
        f.write(f"- Mediana de releases: {median_releases:.0f}\n\n")
        
        # RQ 04: Atualizações
        days_since_update = [repo["days_since_last_update"] for repo in data]
        avg_days = sum(days_since_update) / len(days_since_update)
        median_days = sorted(days_since_update)[len(days_since_update) // 2]
        f.write("RQ 04: Sistemas populares são atualizados com frequência?\n")
        f.write(f"- Média de dias desde a última atualização: {avg_days:.2f}\n")
        f.write(f"- Mediana de dias desde a última atualização: {median_days:.0f}\n\n")
        
        # RQ 05: Linguagens
        languages = [repo["language"] for repo in data]
        language_counts = {}
        for lang in languages:
            language_counts[lang] = language_counts.get(lang, 0) + 1
        sorted_langs = sorted(language_counts.items(), key=lambda x: x[1], reverse=True)
        top_languages = sorted_langs[:10]
        
        f.write("RQ 05: Sistemas populares são escritos nas linguagens mais populares?\n")
        for i, (lang, count) in enumerate(top_languages, 1):
            f.write(f"- {i}. {lang}: {count} repositórios ({count/len(data)*100:.1f}%)\n")
        f.write("\n")
        
        # RQ 06: Issues fechadas
        ratios = [repo["issues_closed_ratio"] for repo in data]
        avg_ratio = sum(ratios) / len(ratios)
        median_ratio = sorted(ratios)[len(ratios) // 2]
        f.write("RQ 06: Sistemas populares possuem um alto percentual de issues fechadas?\n")
        f.write(f"- Média do percentual de issues fechadas: {avg_ratio*100:.2f}%\n")
        f.write(f"- Mediana do percentual de issues fechadas: {median_ratio*100:.2f}%\n")
    
    print(f"Resumo dos resultados salvos em {filename}")

def main():
    data = load_data()
    
    if not data:
        print("Não foi possível carregar os dados. Verifique se o arquivo repositories_data.json existe.")
        return
    
    try:
        analyze_repository_age(data)
        analyze_external_contributions(data)
        analyze_releases(data)
        analyze_update_frequency(data)
        analyze_languages(data)
        analyze_closed_issues(data)
        
        save_summary(data)
        
        print("Análise concluída! Os gráficos foram salvos na pasta 'resultados'.")
    except Exception as e:
        print(f"Erro durante a análise: {str(e)}")

if __name__ == "__main__":
    main()