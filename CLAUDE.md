# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository contains educational materials for LangSmith Academy - a course teaching LangSmith fundamentals including observability, prompt engineering, evaluations, feedback mechanisms, and production monitoring. The project consists primarily of Jupyter notebooks organized into educational modules with accompanying Python applications.

## Environment Setup

**Required Environment Variables (use .env file based on .env.example):**

- `GOOGLE_API_KEY` - Required for Google Gemini models used in examples
- `LANGCHAIN_API_KEY` - Required for LangSmith tracing and features
- `LANGCHAIN_TRACING_V2="true"` - Enables LangSmith tracing
- `LANGCHAIN_PROJECT="langsmith-academy"` - Project name for LangSmith

**For Self-Hosted LangSmith:**

- `LANGSMITH_ENDPOINT="<your-self-hosted-url>/api/v1"`

**Python Environment Setup:**

```bash
python3 -m venv intro-to-ls
source intro-to-ls/bin/activate
pip install -r requirements.txt
```

## Architecture and Module Structure

The course is organized into 6 modules (0-5), each containing:

- **Jupyter Notebooks** (.ipynb) - Interactive learning materials
- **Python Applications** (app.py) - Standalone applications demonstrating concepts
- **Utility Functions** (utils.py) - Shared functionality

### Module Breakdown

- **Module 0**: RAG Application - Basic RAG implementation using LangSmith docs
- **Module 1**: Tracing Basics - LangSmith tracing fundamentals, conversation threads
- **Module 2**: Evaluations - Experiments, evaluators, pairwise comparisons, dataset upload
- **Module 3**: Prompt Engineering - Lifecycle, playground experiments, prompt hub
- **Module 4**: Feedback - Publishing and collecting user feedback
- **Module 5**: Production Monitoring - Online evaluation, filtering

## Key Technologies

- **LangChain** - Framework for LLM applications
- **LangSmith** - Observability and evaluation platform
- **Google Gemini** - Primary LLM provider (gemini-1.5-flash)
- **SKLearnVectorStore** - Vector storage for RAG
- **Jupyter** - Interactive development environment

## Common Development Commands

**Run Jupyter Notebooks:**

```bash
jupyter notebook
# Navigate to notebooks/module_X/ and open .ipynb files
```

**Run Standalone Applications:**

```bash
cd notebooks/module_X/
python app.py
```

**Install Dependencies:**

```bash
pip install -r requirements.txt
```

## RAG Application Pattern

All RAG implementations follow this pattern:

1. **Document Retrieval** - `retrieve_documents()` with `@traceable(run_type="chain")`
2. **Response Generation** - `generate_response()` with `@traceable(run_type="chain")`
3. **LLM Calls** - `call_gemini()` with `@traceable(run_type="llm")`
4. **Main Function** - `langsmith_rag()` orchestrates the flow

The RAG system indexes LangSmith documentation from sitemap.xml and uses RecursiveCharacterTextSplitter with 500-token chunks.

## Google Gemini Integration

The project uses Google Gemini API through:
- **Embeddings**: `GoogleGenerativeAIEmbeddings(model="models/embedding-001")`
- **Chat Models**: `gemini-1.5-flash` (primary) and `gemini-1.5-pro` (advanced)
- **Utility Functions**: `gemini_utils.py` provides conversion helpers for OpenAI→Gemini format
- **Message Format**: Converts OpenAI chat format to Gemini's role+parts structure

## LangSmith Integration

All functions are decorated with `@traceable` for observability:

- `run_type="chain"` for orchestration functions
- `run_type="llm"` for direct LLM calls
- Metadata includes provider ("google") and model information ("gemini-1.5-flash")

## Working with the Codebase

- Notebooks contain both educational content and runnable code
- Each module builds on previous concepts
- Utils files contain reusable functionality across modules
- All examples use LangSmith for tracing and evaluation
- Vector databases are cached in temp directory as .parquet files
- Google Gemini models accessed via `gemini_utils.py` helper functions
- Message conversion handled automatically between OpenAI and Gemini formats
