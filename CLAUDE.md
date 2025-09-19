# CLAUDE.md

Este arquivo fornece orientação para o Claude Code (claude.ai/code) ao trabalhar com código neste repositório.

## Visão Geral do Projeto

Este repositório contém materiais educacionais para a LangSmith Academy - um curso que ensina os fundamentos do LangSmith incluindo observabilidade, engenharia de prompts, avaliações, mecanismos de feedback e monitoramento de produção. O projeto consiste principalmente de notebooks Jupyter organizados em módulos educacionais com aplicações Python acompanhantes.

## Configuração do Ambiente

**Variáveis de Ambiente Necessárias (use arquivo .env baseado no .env.example):**

- `GOOGLE_API_KEY` - Necessária para modelos Google Gemini usados nos exemplos
- `LANGCHAIN_API_KEY` - Necessária para rastreamento e recursos do LangSmith
- `LANGCHAIN_TRACING_V2="true"` - Habilita rastreamento do LangSmith
- `LANGCHAIN_PROJECT="langsmith-academy"` - Nome do projeto para LangSmith

**Para LangSmith Auto-hospedado:**

- `LANGSMITH_ENDPOINT="<sua-url-auto-hospedada>/api/v1"

**Configuração do Ambiente Python:**

```bash
python3 -m venv intro-to-ls
source intro-to-ls/bin/activate
pip install -r requirements.txt
```

## Arquitetura e Estrutura de Módulos

O curso está organizado em 6 módulos (0-5), cada um contendo:

- **Notebooks Jupyter** (.ipynb) - Materiais de aprendizado interativo
- **Aplicações Python** (app.py) - Aplicações independentes demonstrando conceitos
- **Funções Utilitárias** (utils.py) - Funcionalidade compartilhada

### Detalhamento dos Módulos

- **Módulo 0**: Aplicação RAG - Implementação básica de RAG usando documentos LangSmith
- **Módulo 1**: Fundamentos de Rastreamento - Fundamentos de rastreamento LangSmith, threads de conversação
- **Módulo 2**: Avaliações - Experimentos, avaliadores, comparações pareadas, upload de dataset
- **Módulo 3**: Engenharia de Prompts - Ciclo de vida, experimentos playground, hub de prompts
- **Módulo 4**: Feedback - Publicação e coleta de feedback do usuário
- **Módulo 5**: Monitoramento de Produção - Avaliação online, filtragem

## Tecnologias Principais

- **LangChain** - Framework para aplicações LLM
- **LangSmith** - Plataforma de observabilidade e avaliação
- **Google Gemini** - Provedor LLM principal (gemini-1.5-flash)
- **SKLearnVectorStore** - Armazenamento vetorial para RAG
- **Jupyter** - Ambiente de desenvolvimento interativo

## Comandos Comuns de Desenvolvimento

**Executar Notebooks Jupyter:**

```bash
jupyter notebook
# Navegue para notebooks/module_X/ e abra arquivos .ipynb
```

**Executar Aplicações Independentes:**

```bash
cd notebooks/module_X/
python app.py
```

**Instalar Dependências:**

```bash
pip install -r requirements.txt
```

## Padrão de Aplicação RAG

Todas as implementações RAG seguem este padrão:

1. **Recuperação de Documentos** - `retrieve_documents()` com `@traceable(run_type="chain")`
2. **Geração de Resposta** - `generate_response()` com `@traceable(run_type="chain")`
3. **Chamadas LLM** - `call_gemini()` com `@traceable(run_type="llm")`
4. **Função Principal** - `langsmith_rag()` orquestra o fluxo

O sistema RAG indexa documentação LangSmith do sitemap.xml e usa RecursiveCharacterTextSplitter com chunks de 500 tokens.

## Integração Google Gemini

O projeto usa a API Google Gemini através de:
- **Embeddings**: `GoogleGenerativeAIEmbeddings(model="models/embedding-001")`
- **Modelos de Chat**: `gemini-1.5-flash` (principal) e `gemini-1.5-pro` (avançado)
- **Funções Utilitárias**: `gemini_utils.py` fornece helpers de conversão para formato OpenAI→Gemini
- **Formato de Mensagem**: Converte formato de chat OpenAI para estrutura role+parts do Gemini

## Integração LangSmith

Todas as funções são decoradas com `@traceable` para observabilidade:

- `run_type="chain"` para funções de orquestração
- `run_type="llm"` para chamadas diretas de LLM
- Metadata inclui provedor ("google") e informações do modelo ("gemini-1.5-flash")

## Trabalhando com a Base de Código

- Notebooks contêm tanto conteúdo educacional quanto código executável
- Cada módulo se baseia em conceitos anteriores
- Arquivos utils contêm funcionalidade reutilizável entre módulos
- Todos os exemplos usam LangSmith para rastreamento e avaliação
- Bancos de dados vetoriais são armazenados em cache no diretório temp como arquivos .parquet
- Modelos Google Gemini acessados via funções helper `gemini_utils.py`
- Conversão de mensagens tratada automaticamente entre formatos OpenAI e Gemini
