import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from .prompts import prompt


class GroqLLM:
    r"""
    Wrapper class around the Groq API using LangChain's ChatGroq.
    Integrates with ConversationMemory to supply multi-turn chat history.
    """
    def __init__(self, memory=None, model_name="llama-3.3-70b-versatile", api_key=None):
        load_dotenv()
        self.api_key = api_key or os.environ.get("GROQ_API_KEY")
        if self.api_key:
            self.api_key = self.api_key.strip()
        self.model_name = os.environ.get("GROQ_MODEL_NAME", model_name)
        self.memory = memory

        if not self.api_key:
            print("[Warning] GROQ_API_KEY not found in environment or .env file.")

        self.chat_model = ChatGroq(
            model=self.model_name,
            api_key=self.api_key,
            temperature=0.3,
        )

    def generate(self, system_prompt: str, user_query: str, context: str) -> str:
        r"""
        Generate response using LangChain ChatGroq.
        """
        if not self.api_key:
            raise ValueError("GROQ_API_KEY is not set. Please set it in .env file.")

        messages = []

        if not user_query and not context:
            intent = prompt("intent_classification", user_query)
            messages.append(SystemMessage(content=intent))
            messages.append(HumanMessage(content=system_prompt))
        else:
            messages.append(SystemMessage(content=system_prompt))

            if context:
                messages.append(SystemMessage(content=f"Product Search Context:\n{context}"))

            if self.memory and self.memory.messages:
                for msg in self.memory.langchain_messages:
                    messages.append(msg)
            else:
                messages.append(HumanMessage(content=user_query))

        try:
            response = self.chat_model.invoke(messages)
            raw_text = response.content.strip()

            if not user_query and not context:
                raw_text_upper = raw_text.upper()
                allowed = {"SEARCH", "COMPARE", "RECOMMEND", "DETAILS", "OUT_OF_SCOPE"}
                for word in raw_text_upper.split():
                    cleaned_word = "".join(c for c in word if c.isalnum() or c == "_")
                    if cleaned_word in allowed:
                        return cleaned_word
                first_word = "".join(c for c in raw_text_upper.split()[0] if c.isalnum() or c == "_") if raw_text_upper.split() else ""
                return first_word or "OUT_OF_SCOPE"

            return raw_text
        except Exception as e:
            raise RuntimeError(f"Failed to communicate with Groq API: {e}")
