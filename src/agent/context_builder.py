class ContextBuilder:
    r"""
        This class is responsible to build context for the llm to use in order to answer the user query.
    """

    def build(self, results):

        context = []
        documents = results["documents"][0]
        metadata = results["metadatas"][0]

        for doc, meta in zip(documents, metadata):
            context.append(
                f"""
                Product Name: {meta.get("name")}
                Description:
                {doc}
                """
            )

        return "\n".join(context)