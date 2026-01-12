# Projeto de Ingestão e Busca Semântica

Este projeto realiza a leitura de um PDF, salva vetores no PostgreSQL e permite perguntas via chat.

## Instalação

1.  Crie um ambiente virtual:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

2.  Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

3.  Configure as variáveis de ambiente:
    -   Copie `.env.example` para `.env`: `cp .env.example .env`
    -   Edite `.env` e adicione sua `OPENAI_API_KEY` ou `GOOGLE_API_KEY`.

4.  Suba o Banco de Dados (Docker):
    ```bash
    docker compose up -d
    ```

## Como Executar

Execute o menu principal para realizar a ingestão e depois iniciar o chat:

```bash
python main.py
```

Opções:
1.  **Ingestão**: Carrega o PDF no banco de dados.
2.  **Chat**: Faz perguntas sobre o conteúdo.
3.  **Sair**: Encerra o programa.