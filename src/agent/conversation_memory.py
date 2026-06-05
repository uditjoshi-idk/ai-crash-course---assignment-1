from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage


class ConversationMemory:
    r"""
        This class is responsible for storing the conversation history between the user and the assistant.
        Uses LangChain's InMemoryChatMessageHistory internally.
    """

    def __init__(self):
        self.history = InMemoryChatMessageHistory()
        self.last_products = []

    @property
    def messages(self):
        """Backward-compatible property: returns list of dicts with 'role' and 'content' keys."""
        result = []
        for msg in self.history.messages:
            if isinstance(msg, HumanMessage):
                result.append({"role": "user", "content": msg.content})
            elif isinstance(msg, AIMessage):
                result.append({"role": "assistant", "content": msg.content})
        return result

    @property
    def langchain_messages(self):
        """Returns native LangChain message objects."""
        return self.history.messages

    def add_user_message(self, text):
        self.history.add_user_message(text)

    def add_assistant_message(self, text):
        self.history.add_ai_message(text)

    def set_products(self, products):
        self.last_products = products