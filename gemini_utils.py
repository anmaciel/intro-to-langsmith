"""
Utilities for Google Gemini API integration
Provides helper functions to convert OpenAI format to Gemini format
"""
import os
import google.generativeai as genai
from typing import List, Dict, Any

def configure_gemini():
    """Configure Gemini API with API key from environment"""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable is required")
    genai.configure(api_key=api_key)

def convert_openai_messages_to_gemini(messages: List[Dict[str, str]]) -> List[Dict[str, Any]]:
    """
    Convert OpenAI chat messages format to Gemini format

    OpenAI format: [{"role": "user", "content": "Hello"}]
    Gemini format: [{"role": "user", "parts": ["Hello"]}]
    """
    gemini_messages = []

    for message in messages:
        role = message.get("role")
        content = message.get("content", "")

        # Map OpenAI roles to Gemini roles
        if role == "system":
            # Gemini doesn't have system role, prepend as user message
            gemini_messages.append({
                "role": "user",
                "parts": [f"System instruction: {content}"]
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
    """Create and return a Gemini model client"""
    configure_gemini()
    return genai.GenerativeModel(model_name)

def call_gemini_chat(
    model_name: str,
    messages: List[Dict[str, str]],
    temperature: float = 0.0
) -> str:
    """
    Call Gemini API with OpenAI-style messages
    Returns the response text content
    """
    # Configure Gemini if not already configured
    configure_gemini()

    # Create model
    model = genai.GenerativeModel(
        model_name,
        generation_config=genai.types.GenerationConfig(
            temperature=temperature
        )
    )

    # Convert messages
    gemini_messages = convert_openai_messages_to_gemini(messages)

    # Handle single vs multiple messages
    if len(gemini_messages) == 1:
        # Single message - use generate_content
        response = model.generate_content(gemini_messages[0]["parts"][0])
        return response.text
    else:
        # Multiple messages - use chat
        # For system message handling, we'll use the first user message as context
        if gemini_messages and "System instruction:" in gemini_messages[0]["parts"][0]:
            # Extract system instruction and combine with user message
            system_msg = gemini_messages[0]["parts"][0]
            if len(gemini_messages) > 1:
                user_msg = gemini_messages[1]["parts"][0]
                combined_prompt = f"{system_msg}\n\nUser: {user_msg}"
                response = model.generate_content(combined_prompt)
                return response.text

        # For conversation-style messages, use generate_content with combined text
        combined_text = ""
        for msg in gemini_messages:
            role_label = "Assistant" if msg["role"] == "model" else "User"
            combined_text += f"{role_label}: {msg['parts'][0]}\n\n"

        response = model.generate_content(combined_text)
        return response.text

# Model name mappings
OPENAI_TO_GEMINI_MODELS = {
    "gpt-4o-mini": "gemini-1.5-flash",
    "gpt-4o": "gemini-1.5-pro",
    "gpt-3.5-turbo": "gemini-1.5-flash",
    "gpt-4": "gemini-1.5-pro"
}

def get_gemini_model_name(openai_model: str) -> str:
    """Convert OpenAI model name to equivalent Gemini model"""
    return OPENAI_TO_GEMINI_MODELS.get(openai_model, "gemini-1.5-flash")