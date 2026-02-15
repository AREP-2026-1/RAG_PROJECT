"""
Simple example demonstrating how to use the RAG system.
"""

from src.rag_system import RAGSystem


def main():
    """Run a simple example of the RAG system."""
    
    print("Initializing RAG System...")
    print("-" * 60)
    
    # Create a RAG system instance
    rag = RAGSystem(data_dir="data", persist_directory="chroma_db")
    
    # Initialize the system (this will load documents and create the vector store)
    rag.initialize()
    
    # Example questions to demonstrate the system
    print("\n" + "=" * 60)
    print("EXAMPLE QUESTIONS")
    print("=" * 60)
    
    # Question 1: About RAG
    print("\n1. Asking about RAG concept:")
    rag.ask("What is RAG and what are its main components?")
    
    # Question 2: About LangChain
    print("\n2. Asking about LangChain:")
    rag.ask("What is LangChain Expression Language (LCEL)?")
    
    # Question 3: About Python
    print("\n3. Asking about Python best practices:")
    rag.ask("What are some Python security best practices?")
    
    print("\n" + "=" * 60)
    print("Example completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
