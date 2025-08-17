import requests
import json
import time
import datetime
import os
import sys

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    print("Erro: Token do GitHub não encontrado!")
    print("Defina a variável de ambiente GITHUB_TOKEN antes de executar o script.")
    print("Exemplo no Windows: set GITHUB_TOKEN=seu_token_aqui")
    print("Exemplo no Linux/macOS: export GITHUB_TOKEN=seu_token_aqui")
    sys.exit(1)

HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Content-Type": "application/json",
}
API_ENDPOINT = "https://api.github.com/graphql"

def create_query(cursor=None):
    after_clause = f', after: "{cursor}"' if cursor else ""
    return f"""
    {{
      search(query: "stars:>1000", type: REPOSITORY, first: 25{after_clause}) {{
        pageInfo {{
          hasNextPage
          endCursor
        }}
        nodes {{
          ... on Repository {{
            nameWithOwner
            url
            stargazerCount
            createdAt
            updatedAt
            primaryLanguage {{
              name
            }}
            releases {{
              totalCount
            }}
            pullRequests(states: [MERGED]) {{
              totalCount
            }}
            issues(states: [OPEN, CLOSED]) {{
              totalCount
            }}
            closedIssues: issues(states: [CLOSED]) {{
              totalCount
            }}
          }}
        }}
      }}
    }}
    """

def fetch_repositories(total_count=100, max_retries=3):
    repositories = []
    cursor = None
    
    print(f"Coletando dados de {total_count} repositórios mais populares do GitHub...")
    
    while len(repositories) < total_count:
        query = create_query(cursor)
        
        # Implementar lógica de retry
        retry_count = 0
        success = False
        
        while not success and retry_count < max_retries:
            try:
                response = requests.post(
                    API_ENDPOINT, 
                    headers=HEADERS, 
                    json={"query": query},
                    timeout=30  # Adicionar timeout explícito
                )
                
                if response.status_code == 200:
                    success = True
                else:
                    retry_count += 1
                    print(f"Erro na requisição (tentativa {retry_count}/{max_retries}): {response.status_code}")
                    if retry_count < max_retries:
                        wait_time = 5 * retry_count  # Backoff exponencial
                        print(f"Aguardando {wait_time} segundos antes de tentar novamente...")
                        time.sleep(wait_time)
            except requests.exceptions.RequestException as e:
                retry_count += 1
                print(f"Erro de conexão (tentativa {retry_count}/{max_retries}): {str(e)}")
                if retry_count < max_retries:
                    wait_time = 5 * retry_count
                    print(f"Aguardando {wait_time} segundos antes de tentar novamente...")
                    time.sleep(wait_time)
        
        if not success:
            print("Máximo de tentativas excedido. Finalizando coleta com os dados já obtidos.")
            break
        
        data = response.json()
        
        if "errors" in data:
            print(f"Erro na consulta GraphQL: {data['errors']}")
            break
            
        search_results = data["data"]["search"]
        current_repos = search_results["nodes"]
        repositories.extend(current_repos)
        
        print(f"Coletados {len(repositories)} repositórios até agora.")
        
        page_info = search_results["pageInfo"]
        if not page_info["hasNextPage"] or len(repositories) >= total_count:
            break
            
        cursor = page_info["endCursor"]
        
        # Respeitar limites da API do GitHub
        time.sleep(2)
    
    # Limitar ao número desejado
    return repositories[:total_count]

def process_repositories(repositories):
    today = datetime.datetime.now(datetime.timezone.utc)
    processed_data = []
    
    print(f"Processando dados de {len(repositories)} repositórios...")
    
    for repo in repositories:
        try:
            created_at = datetime.datetime.fromisoformat(repo["createdAt"].replace("Z", "+00:00"))
            updated_at = datetime.datetime.fromisoformat(repo["updatedAt"].replace("Z", "+00:00"))
            
            # Calcula a idade do repositório em dias
            age_days = (today - created_at).days
            
            # Calcula o tempo desde a última atualização em dias
            days_since_update = (today - updated_at).days
            
            # Calcula o percentual de issues fechadas
            total_issues = repo["issues"]["totalCount"]
            closed_issues = repo["closedIssues"]["totalCount"]
            issues_closed_ratio = closed_issues / total_issues if total_issues > 0 else 0
            
            processed_repo = {
                "name": repo["nameWithOwner"],
                "url": repo["url"],
                "stars": repo["stargazerCount"],
                "language": repo["primaryLanguage"]["name"] if repo["primaryLanguage"] else "None",
                "age_days": age_days,
                "days_since_last_update": days_since_update,
                "releases_count": repo["releases"]["totalCount"],
                "merged_pull_requests": repo["pullRequests"]["totalCount"],
                "total_issues": total_issues,
                "closed_issues": closed_issues,
                "issues_closed_ratio": issues_closed_ratio
            }
            
            processed_data.append(processed_repo)
        except Exception as e:
            print(f"Erro ao processar repositório {repo.get('nameWithOwner', 'desconhecido')}: {str(e)}")
    
    return processed_data

def save_to_json(data, filename="repositories_data.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Dados salvos em {filename}")

def save_to_csv(data, filename="repositories_data.csv"):
    if not data:
        print("Nenhum dado para salvar.")
        return
    
    import csv
    
    with open(filename, "w", newline="", encoding="utf-8") as f:
        headers = data[0].keys() if data else []
        writer = csv.DictWriter(f, fieldnames=headers)
        
        writer.writeheader()
        writer.writerows(data)
    
    print(f"Dados salvos em {filename}")

def main():
    repositories = fetch_repositories(100)  
    
    if repositories:
        processed_data = process_repositories(repositories)
        
        if processed_data:
            save_to_json(processed_data)
            save_to_csv(processed_data)
            print(f"Coleta de dados concluída com sucesso! Coletados {len(processed_data)} repositórios.")
        else:
            print("Não foi possível processar os dados dos repositórios.")
    else:
        print("Falha na coleta de dados dos repositórios.")

if __name__ == "__main__":
    main()