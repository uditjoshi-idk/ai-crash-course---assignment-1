from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from .intent_classifier import IntentClassifier
from .context_builder import ContextBuilder
from .domain_restriction import is_correct


class ProductAgent:
    def __init__(self, retriever, llm, memory):
        self.retriever = retriever
        self.llm = llm
        self.memory = memory

        self.intent_classifier = IntentClassifier(llm)
        self.context_builder = ContextBuilder()

        # Build the LCEL response chain:
        self._response_chain = (
            ChatPromptTemplate.from_messages([
                ("system", "{system_prompt}"),
                ("system", "Product Search Context:\n{context}"),
                ("human", "{user_query}"),
            ])
            | self.llm.chat_model
            | StrOutputParser()
        )

    def chat(self, user_query):
        intent = self.intent_classifier.classify(user_query)
        if not is_correct(user_query, intent=intent):
            return "Sorry, I can only answer questions related to products."
        if self.memory:
            self.memory.add_user_message(user_query)
        results = self.retriever.retrieve(user_query)
        context = self.context_builder.build(results)

        from .prompts import prompt
        response = self._response_chain.invoke({
            "system_prompt": prompt("system"),
            "user_query": user_query,
            "context": context,
        })

        if self.memory:
            self.memory.add_assistant_message(response)
        return response