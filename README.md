# Laboratório 1 de Experimentação de Software

Este projeto implementa consultas à API GraphQL do GitHub para coletar informações de **100 repositórios** e responder a diferentes **Questões de Pesquisa (RQs)** relacionadas a métricas de popularidade, maturidade e atividade dos sistemas.

---

## 🚀 Objetivo

O objetivo deste laboratório é automatizar a coleta e análise de dados de repositórios no GitHub, utilizando a API GraphQL, de modo a responder às seguintes **questões de pesquisa**:

### Questões de Pesquisa (RQs)

- **RQ01:** Sistemas populares são maduros/antigos?  
  *Métrica:* idade do repositório (calculada a partir da data de criação).  

- **RQ02:** Sistemas populares recebem muita contribuição externa?  
  *Métrica:* total de *pull requests* aceitas.  

- **RQ03:** Sistemas populares lançam releases com frequência?  
  *Métrica:* total de releases.  

- **RQ04:** Sistemas populares são atualizados com frequência?  
  *Métrica:* tempo até a última atualização (calculado a partir da data da última atualização).  

- **RQ05:** Sistemas populares são escritos nas linguagens mais populares?  
  *Métrica:* linguagem primária de cada repositório.  

- **RQ06:** Sistemas populares possuem um alto percentual de issues fechadas?  
  *Métrica:* razão entre número de issues fechadas pelo total de issues.  

---

## ⚙️ Como Executar

2. **Ativar o ambiente**
   ```bash
   # Windows
   venv\Scripts\activate

   # Linux/Mac
   source venv/bin/activate
   ```

3. **Instalar dependências**
   ```bash
   pip install -r requirements.txt
   ```

4. **Executar o projeto**  
   É necessário fornecer um **GitHub Personal Access Token** para acessar a API GraphQL.  

   > O token pode ser gerado em: [Configurações do GitHub → Developer settings → Personal access tokens → Tokens (classic)](https://github.com/settings/tokens)  
   > É recomendado selecionar ao menos a permissão `repo` para acesso completo às informações públicas de repositórios.

   Exemplo de execução:
   ```bash
   GITHUB_TOKEN=<seu_token> python run_analysis.py
   ```

---

## 📊 Saída Esperada

Após a execução, o programa gera métricas que permitem responder às **Questões de Pesquisa (RQs)**, incluindo:

- 📅 **Idade do repositório** (RQ01)  
- 🔀 **Número de pull requests aceitas** (RQ02)  
- 🏷️ **Total de releases** (RQ03)  
- ⏳ **Tempo até a última atualização** (RQ04)  
- 💻 **Linguagem primária do repositório** (RQ05)  
- ✅ **Percentual de issues fechadas** (RQ06)  

Esses resultados podem ser exibidos no console ou exportados para arquivos de análise, dependendo da implementação feita nos scripts.

---

## 👨‍💻 Autores

- [Luís Felipe Teixeira Dias Brescia](https://luisbrescia.tech)
- [Victor Reis Carlota](https://carlotavictor.vercel.app)
