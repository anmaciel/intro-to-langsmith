"""
Utilitários para integração da API Google Gemini
Fornece funções auxiliares para converter formato OpenAI para formato Gemini
"""
import os
import google.generativeai as genai
from typing import List, Dict, Any

def configure_gemini():
    """Configura API Gemini com chave API do ambiente"""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("Variável de ambiente GOOGLE_API_KEY é necessária")
    genai.configure(api_key=api_key)

def convert_openai_messages_to_gemini(messages: List[Dict[str, str]]) -> List[Dict[str, Any]]:
    """
    Converte formato de mensagens de chat OpenAI para formato Gemini

    Formato OpenAI: [{"role": "user", "content": "Olá"}]
    Formato Gemini: [{"role": "user", "parts": ["Olá"]}]
    """
    gemini_messages = []

    for message in messages:
        role = message.get("role")
        content = message.get("content", "")

        # Mapeia roles OpenAI para roles Gemini
        if role == "system":
            # Gemini não tem role system, adiciona como mensagem user
            gemini_messages.append({
                "role": "user",
                "parts": [f"Instrução do sistema: {content}"]
            })
        elif role == "assistant":
            gemini_messages.append({
                "role": "model",
                "parts": [content]
            })
        elif role == "user":
            gemini_messages.append({
                "role": "user",
                "parts": [content]
            })

    return gemini_messages

def create_gemini_client(model_name: str = "gemini-1.5-flash"):
    """Cria e retorna um cliente modelo Gemini"""
    configure_gemini()
    return genai.GenerativeModel(model_name)

def call_gemini_chat(
    model_name: str,
    messages: List[Dict[str, str]],
    temperature: float = 0.0
) -> str:
    """
    Chama API Gemini com mensagens estilo OpenAI
    Retorna o conteúdo de texto da resposta
    """
    # Configura Gemini se ainda não configurado
    configure_gemini()

    # Cria modelo
    model = genai.GenerativeModel(
        model_name,
        generation_config=genai.types.GenerationConfig(
            temperature=temperature
        )
    )

    # Converte mensagens
    gemini_messages = convert_openai_messages_to_gemini(messages)

    # Trata mensagem única vs múltiplas mensagens
    if len(gemini_messages) == 1:
        # Mensagem única - usa generate_content
        response = model.generate_content(gemini_messages[0]["parts"][0])
        return response.text
    else:
        # Múltiplas mensagens - usa chat
        # Para tratamento de mensagem system, usaremos a primeira mensagem user como contexto
        if gemini_messages and "Instrução do sistema:" in gemini_messages[0]["parts"][0]:
            # Extrai instrução do sistema e combina com mensagem do usuário
            system_msg = gemini_messages[0]["parts"][0]
            if len(gemini_messages) > 1:
                user_msg = gemini_messages[1]["parts"][0]
                combined_prompt = f"{system_msg}\n\nUser: {user_msg}"
                response = model.generate_content(combined_prompt)
                return response.text

        # Para mensagens estilo conversa, usa generate_content com texto combinado
        combined_text = ""
        for msg in gemini_messages:
            role_label = "Assistente" if msg["role"] == "model" else "Usuário"
            combined_text += f"{role_label}: {msg['parts'][0]}\n\n"

        response = model.generate_content(combined_text)
        return response.text

# Mapeamento de nomes de modelos
OPENAI_TO_GEMINI_MODELS = {
    "gpt-4o-mini": "gemini-1.5-flash",
    "gpt-4o": "gemini-1.5-pro",
    "gpt-3.5-turbo": "gemini-1.5-flash",
    "gpt-4": "gemini-1.5-pro"
}

def get_gemini_model_name(openai_model: str) -> str:
    """Converte nome do modelo OpenAI para modelo Gemini equivalente"""
    return OPENAI_TO_GEMINI_MODELS.get(openai_model, "gemini-1.5-flash")