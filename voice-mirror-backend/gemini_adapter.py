from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages.base import BaseMessage

MODEL = "gemini-1.5-flash"

class GeminiAdapter:
    def __init__(self, api_key: str):
        self.chat_google_generative_ai = ChatGoogleGenerativeAI(model=MODEL, api_key=api_key)

    def chat(self, username: str, message: str) -> BaseMessage:
        prompt = f"Pretend you are a person texting someone back. The message you are responding to is: {message}. What would you text back?"
        response = self.chat_google_generative_ai.invoke(prompt)
        print(response)
        return response