import os
import sys
import tempfile
sys.path.append('../../')
from gemini_utils import call_gemini_chat
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders.sitemap import SitemapLoader
from langchain_community.vectorstores import SKLearnVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langsmith import traceable
from typing import List
import nest_asyncio

MODEL_NAME = "gemini-1.5-flash"
MODEL_PROVIDER = "google"
APP_VERSION = 1.0
RAG_SYSTEM_PROMPT = """Você é um assistente para tarefas de perguntas e respostas.
Use as seguintes partes do contexto recuperado para responder à pergunta mais recente na conversa.
Se você não souber a resposta, apenas diga que não sabe.
Use no máximo três frases e mantenha a resposta concisa.
"""


def get_vector_db_retriever():
    persist_path = os.path.join(tempfile.gettempdir(), "union.parquet")
    embd = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    # Se o armazenamento vetorial existir, então carregá-lo
    if os.path.exists(persist_path):
        vectorstore = SKLearnVectorStore(
            embedding=embd,
            persist_path=persist_path,
            serializer="parquet"
        )
        return vectorstore.as_retriever(lambda_mult=0)

    # Caso contrário, indexar documentos LangSmith e criar novo armazenamento vetorial
    ls_docs_sitemap_loader = SitemapLoader(web_path="https://docs.smith.langchain.com/sitemap.xml", continue_on_failure=True)
    ls_docs = ls_docs_sitemap_loader.load()

    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=500, chunk_overlap=0
    )
    doc_splits = text_splitter.split_documents(ls_docs)

    vectorstore = SKLearnVectorStore.from_documents(
        documents=doc_splits,
        embedding=embd,
        persist_path=persist_path,
        serializer="parquet"
    )
    vectorstore.persist()
    return vectorstore.as_retriever(lambda_mult=0)

nest_asyncio.apply()
retriever = get_vector_db_retriever()

"""
retrieve_documents
- Retorna documentos buscados de um armazenamento vetorial baseado na pergunta do usuário
"""
@traceable(run_type="chain")
def retrieve_documents(question: str):
    return retriever.invoke(question)

"""
generate_response
- Chama `call_gemini` para gerar uma resposta do modelo após formatar entradas
"""
@traceable(run_type="chain")
def generate_response(question: str, documents):
    formatted_docs = "\n\n".join(doc.page_content for doc in documents)
    messages = [
        {
            "role": "system",
            "content": RAG_SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": f"Contexto: {formatted_docs} \n\n Pergunta: {question}"
        }
    ]
    return call_gemini(messages)

"""
call_gemini
- Returns the chat completion output from Google Gemini
"""
@traceable(
    run_type="llm",
    metadata={
        "ls_provider": MODEL_PROVIDER,
        "ls_model_name": MODEL_NAME
    }
)
def call_gemini(messages: List[dict]) -> str:
    return call_gemini_chat(MODEL_NAME, messages)

"""
langsmith_rag
- Calls `retrieve_documents` to fetch documents
- Calls `generate_response` to generate a response based on the fetched documents
- Returns the model response
"""
@traceable(run_type="chain")
def langsmith_rag(question: str):
    documents = retrieve_documents(question)
    response = generate_response(question, documents)
    return response
