# Introdução ao LangSmith

Bem-vindo à Introdução ao LangSmith!

## Introdução

Neste curso, vamos percorrer os fundamentos do LangSmith - explorando observabilidade, engenharia de prompts, avaliações, mecanismos de feedback e monitoramento de produção. Dê uma olhada nas instruções de configuração abaixo para acompanhar qualquer um dos nossos exemplos de notebook.

---

## Configuração

Siga estas instruções para ter certeza de que você tem todos os recursos necessários para este curso!

### Inscrever-se no LangSmith

* [Inscreva-se](https://smith.langchain.com/)
* Navegue até a página de Configurações e gere uma chave de API no LangSmith.
* Crie um arquivo .env que imita o .env.example fornecido. Defina `LANGCHAIN_API_KEY` no arquivo .env.

### Configurar chave da API do Google

* Se você não tem uma chave da API do Google, pode [se inscrever aqui](https://aistudio.google.com/app/apikey).
* Defina `GOOGLE_API_KEY` no arquivo .env.

### Criar ambiente e instalar dependências

```bash
cd intro-to-langsmith
python3 -m venv intro-to-ls
source intro-to-ls/bin/activate
pip install -r requirements.txt
```

### LangSmith Auto-hospedado

Nota: Se você está usando uma versão auto-hospedada do LangSmith, precisará definir esta variável de ambiente além das outras - veja este [guia](https://docs.smith.langchain.com/self_hosting/usage) para mais informações

```txt
LANGSMITH_ENDPOINT = "<sua-url-auto-hospedada>/api/v1"
```
