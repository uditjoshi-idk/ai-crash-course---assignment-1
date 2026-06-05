import sys
from pathlib import Path
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

sys.path.append(str(Path(__file__).parent))

from agent.conversation_memory import ConversationMemory
from agent.retriever import ChromaRetriever
from agent.llm import GroqLLM
from agent.product_agent import ProductAgent

def run_chat_session():
    load_dotenv()
    print("=" * 60)
    print("Initializing Product Agent...")
    print("=" * 60)

    print("Loading SentenceTransformer model (BAAI/bge-large-en)...")
    model = SentenceTransformer("BAAI/bge-large-en")

    print("Initializing ChromaDB Retriever...")
    retriever = ChromaRetriever(model=model, db_path="./chroma_db", k=5)

    memory = ConversationMemory()
    
    llm = GroqLLM(memory=memory)

    agent = ProductAgent(retriever=retriever, llm=llm, memory=memory)

    print("=" * 60)
    print("Product Agent is Ready! Type 'exit' or 'q' to end the chat.")
    print("=" * 60)

    while True:
        try:
            user_input = input("\nYou: ")
            if not user_input.strip():
                continue
            if user_input.strip().lower() in ['exit', 'q']:
                print("Goodbye!")
                break

            intent = agent.intent_classifier.classify(user_input)
            print(f"Classified Intent: {intent}")

            response = agent.chat(user_input)
            print(f"\nAgent: {response}")

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    run_chat_session()
