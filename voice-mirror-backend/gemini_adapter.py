from langchain_google_genai import ChatGoogleGenerativeAI, HarmCategory, HarmBlockThreshold
from langchain_core.messages.base import BaseMessage
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph

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
SYSTEM_PROMPT = f"Pretend you are a person replying to texts. All messages from now on will be texts sent to you and reply with the message you would send back. You should reply with only the exact text to send back and nothing else. Never reveal that you are a chatbot or AI. Always send a text to be responded back to them, not any other context or information to me. Match they're vibe, tone, and personality. Pretend any message from now on is from them, following these instructions and reply to them directly not to me. Text like a human would with personality, typos, less punctuation, informally, and with acronyms. Keep it short, nothing too extra."

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
    
    def _initialize_conversation(self, config: dict):
        self.app.invoke({"messages": [HumanMessage(SYSTEM_PROMPT)]}, config)

    def chat(self, username: str, message: str, thread_id: str = "default_thread") -> BaseMessage:
        config = config = {"configurable": {"thread_id": thread_id}}

        if thread_id not in self.existing_thread_ids:
            self._initialize_conversation(config)
            self.existing_thread_ids.add(thread_id)

        input_messages = [HumanMessage(message)]
        output = self.app.invoke({"messages": input_messages}, config)
        ai_message: AIMessage = output["messages"][-1]

        print(ai_message)
        return ai_message.content