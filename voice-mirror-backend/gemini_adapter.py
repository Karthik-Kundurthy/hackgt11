from langchain_google_genai import ChatGoogleGenerativeAI, HarmCategory, HarmBlockThreshold
from langchain_core.messages.base import BaseMessage
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from typing import Optional

MODEL = "gemini-1.5-flash"
SAFETY_SETTINGS = {
    HarmCategory.HARM_CATEGORY_UNSPECIFIED: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_DEROGATORY: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_TOXICITY: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_VIOLENCE: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_SEXUAL: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_MEDICAL: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_DANGEROUS: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE
}

def create_initial_prompt(username: str, persona: str) -> HumanMessage:
    prompt = f"Pretend you are a person named {persona} replying to texts from {username}. All messages from now on will be texts sent to {persona} and you should respond as {persona} texting back. You should reply with only the exact text to send back and nothing else. Never reveal that you are a chatbot or AI. Always send a text to be responded back to {username}, not any other context or information to me. I will provide you with context from past conversations on how {persona} texts. You should use the context to match they're vibe, tone, and personality. Text like a human would with personality, typos, less punctuation, informally, and with acronyms. Keep it short, nothing too extra."
    return HumanMessage(prompt)

def create_prompt(username: str, persona: str, message: str, context: Optional[str]) -> HumanMessage:
    context = context if context else "(No sample conversation is available)"
    prompt = f"Here is some sample context on how {persona} texts: {context}. You are {persona} texting back to {username}. Here is an incoming message from {username}, reply how {persona} might respond to it: {message}"
    return HumanMessage(prompt)


class GeminiAdapter:
    def __init__(self, api_key: str):
        workflow = StateGraph(state_schema=MessagesState)
        workflow.add_edge(START, "model")
        workflow.add_node("model", self._call_model)
        memory = MemorySaver()
    
        self.gemini_llm = ChatGoogleGenerativeAI(
            model=MODEL, 
            api_key=api_key, 
            safety_settings=SAFETY_SETTINGS
        )
        self.existing_thread_ids = set()
        self.app = workflow.compile(checkpointer=memory)

    def _call_model(self, state: MessagesState):
        response = self.gemini_llm.invoke(state["messages"])
        return {"messages": response}
    
    def _initialize_conversation(self, username: str, persona: str, config: dict):
        print("Prompt:", create_initial_prompt(username, persona))
        self.app.invoke({"messages": [create_initial_prompt(username, persona)]}, config)

    def chat(self, username: str, persona: str, message: str, thread_id: str, context: str) -> BaseMessage:
        config = config = {"configurable": {"thread_id": thread_id}}

        if thread_id not in self.existing_thread_ids:
            self._initialize_conversation(username, persona, config)
            self.existing_thread_ids.add(thread_id)

        if not context:
            context = "(No sample conversation is available)"

        print("prompt:", create_prompt(username, persona, message, context))
        input_messages = [create_prompt(username, persona, message, context)]
        output = self.app.invoke({"messages": input_messages}, config)
        ai_message: AIMessage = output["messages"][-1]

        print("Thread ID:", thread_id)
        print("Context:", context)
        print("User Message:", message)
        print("AI Message:", ai_message)

        return ai_message.content