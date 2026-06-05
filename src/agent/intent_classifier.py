from langchain_core.output_parsers import StrOutputParser
from .prompts import INTENT_CLASSIFICATION_TEMPLATE


class IntentClassifier:
    r"""
        This class is responsible for classifying the intent of the user query.
        Uses an LCEL chain (ChatPromptTemplate | ChatGroq | StrOutputParser).
    """

    def __init__(self, llm=None):
        self.llm = llm
        self._chain = None

        if self.llm and hasattr(self.llm, 'chat_model'):
            self._chain = INTENT_CLASSIFICATION_TEMPLATE | self.llm.chat_model | StrOutputParser()

    def classify(self, user_query: str) -> str:
        r"""
        This function takes the user query as input and returns the intent of the query.
        """
        if not self._chain:
            return "SEARCH"

        try:
            response = self._chain.invoke({"user_input": user_query})
            intent = response.strip().split()[0].upper()
            allowed = {"SEARCH", "COMPARE", "RECOMMEND", "DETAILS", "OUT_OF_SCOPE"}
            return intent if intent in allowed else "OUT_OF_SCOPE"
        except Exception:
            return "OUT_OF_SCOPE"