"""
RAG System Implementation using LangChain

This module implements a Retrieval-Augmented Generation system that:
1. Loads and processes documents from the data directory
2. Creates embeddings and stores them in a vector database
3. Enables question-answering using retrieved context
"""

import os
from typing import List
from dotenv import load_dotenv

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.schema import Document


class RAGSystem:
    """
    A Retrieval-Augmented Generation system that combines document retrieval
    with language model generation to answer questions based on a knowledge base.
    """
    
    def __init__(self, data_dir: str = "data", persist_directory: str = "chroma_db"):
        """
        Initialize the RAG system.
        
        Args:
            data_dir: Directory containing documents to index
            persist_directory: Directory to persist the vector database. If the directory
                             already exists, the vector store will be loaded from it.
                             If it doesn't exist, it will be created during initialization.
        """
        load_dotenv()
        
        # Check if OpenAI API key is set
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError(
                "OpenAI API key not found. Please set OPENAI_API_KEY in your .env file"
            )
        
        self.data_dir = data_dir
        self.persist_directory = persist_directory
        self.vectorstore = None
        self.qa_chain = None
        
        # Initialize embeddings model
        self.embeddings = OpenAIEmbeddings()
        
        # Initialize LLM
        self.llm = ChatOpenAI(
            model_name="gpt-3.5-turbo",
            temperature=0.0
        )
    
    def load_documents(self) -> List[Document]:
        """
        Load documents from the data directory.
        
        Returns:
            List of loaded Document objects
        """
        print(f"Loading documents from {self.data_dir}...")
        
        loader = DirectoryLoader(
            self.data_dir,
            glob="**/*.txt",
            loader_cls=TextLoader
        )
        
        documents = loader.load()
        print(f"Loaded {len(documents)} documents")
        
        return documents
    
    def split_documents(self, documents: List[Document]) -> List[Document]:
        """
        Split documents into smaller chunks for better retrieval.
        
        Args:
            documents: List of Document objects to split
            
        Returns:
            List of Document chunks
        """
        print("Splitting documents into chunks...")
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        
        chunks = text_splitter.split_documents(documents)
        print(f"Created {len(chunks)} document chunks")
        
        return chunks
    
    def create_vectorstore(self, documents: List[Document]):
        """
        Create a vector store from documents.
        
        Args:
            documents: List of Document objects to store
        """
        print("Creating vector store...")
        
        self.vectorstore = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            persist_directory=self.persist_directory
        )
        
        print(f"Vector store created and persisted to {self.persist_directory}")
    
    def load_vectorstore(self):
        """
        Load an existing vector store from disk.
        """
        print(f"Loading vector store from {self.persist_directory}...")
        
        self.vectorstore = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings
        )
        
        print("Vector store loaded successfully")
    
    def setup_qa_chain(self):
        """
        Set up the question-answering chain with custom prompt.
        """
        if not self.vectorstore:
            raise ValueError("Vector store not initialized. Call create_vectorstore() first.")
        
        # Create a custom prompt template
        prompt_template = """You are a helpful assistant that answers questions based on the provided context.
Use the following pieces of context to answer the question at the end.
If you don't know the answer based on the context, just say that you don't know, don't try to make up an answer.
Always provide a clear and concise answer.

Context:
{context}

Question: {question}

Answer:"""
        
        PROMPT = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )
        
        # Create the retrieval QA chain
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever(
                search_kwargs={"k": 3}  # Retrieve top 3 most relevant chunks
            ),
            return_source_documents=True,
            chain_type_kwargs={"prompt": PROMPT}
        )
        
        print("QA chain set up successfully")
    
    def initialize(self, force_reload: bool = False):
        """
        Initialize the RAG system by loading or creating the vector store.
        
        Args:
            force_reload: If True, reload documents even if vector store exists
        """
        # Check if vector store already exists
        if os.path.exists(self.persist_directory) and not force_reload:
            print("Existing vector store found. Loading...")
            self.load_vectorstore()
        else:
            print("Creating new vector store...")
            documents = self.load_documents()
            chunks = self.split_documents(documents)
            self.create_vectorstore(chunks)
        
        self.setup_qa_chain()
        print("\nRAG system initialized and ready to answer questions!\n")
    
    def ask(self, question: str) -> dict:
        """
        Ask a question and get an answer from the RAG system.
        
        Args:
            question: The question to ask
            
        Returns:
            Dictionary containing the answer and source documents
        """
        if not self.qa_chain:
            raise ValueError("QA chain not initialized. Call initialize() first.")
        
        print(f"\nQuestion: {question}")
        print("-" * 80)
        
        result = self.qa_chain.invoke({"query": question})
        
        answer = result["result"]
        source_docs = result["source_documents"]
        
        print(f"Answer: {answer}\n")
        
        if source_docs:
            print("Sources:")
            for i, doc in enumerate(source_docs, 1):
                source = doc.metadata.get("source", "Unknown")
                print(f"  {i}. {source}")
        
        print("-" * 80)
        
        return {
            "question": question,
            "answer": answer,
            "sources": [doc.metadata.get("source", "Unknown") for doc in source_docs]
        }
    
    def similarity_search(self, query: str, k: int = 3) -> List[Document]:
        """
        Perform similarity search to find relevant documents.
        
        Args:
            query: The search query
            k: Number of documents to return
            
        Returns:
            List of relevant Document objects
        """
        if not self.vectorstore:
            raise ValueError("Vector store not initialized. Call initialize() first.")
        
        return self.vectorstore.similarity_search(query, k=k)


def main():
    """
    Main function to demonstrate the RAG system.
    """
    print("=" * 80)
    print("RAG System - Retrieval-Augmented Generation with LangChain")
    print("=" * 80)
    print()
    
    # Initialize the RAG system
    rag = RAGSystem(data_dir="data", persist_directory="chroma_db")
    rag.initialize()
    
    # Example questions
    questions = [
        "What is RAG and how does it work?",
        "What are the benefits of using RAG?",
        "What are the best practices for Python programming?",
        "What is LangChain and what are its key components?",
    ]
    
    # Ask questions
    for question in questions:
        rag.ask(question)
        print()
    
    # Interactive mode
    print("\n" + "=" * 80)
    print("Interactive Mode - Enter your questions (type 'quit' to exit)")
    print("=" * 80)
    print()
    
    while True:
        question = input("Your question: ").strip()
        
        if question.lower() in ["quit", "exit", "q"]:
            print("\nGoodbye!")
            break
        
        if not question:
            continue
        
        try:
            rag.ask(question)
        except Exception as e:
            print(f"Error: {e}")
        
        print()


if __name__ == "__main__":
    main()
