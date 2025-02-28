import time
from langchain_community.chat_models import ChatOllama  # Ollama model import
from langchain.schema import HumanMessage, SystemMessage

# ---------- OLLAMA Model Initialization ----------
llm = ChatOllama(model="mistral")  # Using a local Mistral model via Ollama

# ---------- OPENAI Alternative (Commented Out) ----------
# If you want to use OpenAI instead of Ollama, follow these changes:
# from langchain_openai import ChatOpenAI  # Import OpenAI model
# from dotenv import load_dotenv
# import os

# load_dotenv()  # Load API key from .env file
# llm = ChatOpenAI(
#     model_name="gpt-4",  # Specify "gpt-3.5-turbo" or "gpt-4" based on need
#     openai_api_key=os.getenv("OPENAI_API_KEY")  # Load API key from environment
# )


def query_mistral(prompt, role="supportive coach"):
    """Send a prompt to the local Mistral model via Ollama with role-based context."""

    system_prompt = f"""You are a {role} helping the user improve their verbal communication.
    - Provide feedback on their tone, clarity, and grammar.
    - Suggest improvements to make their message clearer and more effective.
    - Keep responses constructive, supportive, and encouraging.
    - If the user asks a general question, provide relevant information.
    """

    messages = [
        SystemMessage(content=system_prompt),  # Setting AI's behavior
        HumanMessage(content=prompt)  # User input
    ]

    try:
        response = llm.invoke(messages)  # Invoke the Ollama model
        return response.content.strip()

    except Exception as e:
        return f"⚠️ Error: {str(e)}"


# Example usage:
# response = query_mistral("How can I improve my presentation skills?")
# print(response)

# ---------- Differences Between Ollama and OpenAI ----------
# 1. **Ollama** runs locally, no internet or API key required.
# 2. **OpenAI** requires an API key and internet access.
# 3. **Performance**: OpenAI models (GPT-4) are more powerful, but Ollama provides privacy and cost-free usage.
# 4. **Initialization**: Replace `ChatOllama` with `ChatOpenAI` and load API keys for OpenAI usage.
