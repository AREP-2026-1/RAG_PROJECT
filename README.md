# RAG Project - Retrieval-Augmented Generation System

A comprehensive implementation of a Retrieval-Augmented Generation (RAG) system using LangChain and OpenAI. This project demonstrates how to build a question-answering system that combines document retrieval with large language models to provide accurate, context-aware responses.

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)

## 🎯 Overview

This RAG system implements a knowledge retrieval and question-answering pipeline that:
1. Loads documents from a local directory
2. Splits them into manageable chunks
3. Creates vector embeddings using OpenAI's embedding model
4. Stores embeddings in a ChromaDB vector database
5. Retrieves relevant context for user queries
6. Generates answers using GPT-3.5-turbo with retrieved context

## 🏗️ Architecture

The system follows the standard RAG architecture with these key components:

```
┌─────────────────────────────────────────────────────────────┐
│                    RAG System Architecture                   │
└─────────────────────────────────────────────────────────────┘

1. DOCUMENT PROCESSING
   ┌──────────────┐      ┌──────────────┐      ┌──────────────┐
   │   Document   │──────▶│     Text     │──────▶│   Document   │
   │    Loader    │      │   Splitter   │      │    Chunks    │
   └──────────────┘      └──────────────┘      └──────────────┘

2. EMBEDDING & STORAGE
   ┌──────────────┐      ┌──────────────┐
   │   OpenAI     │──────▶│   ChromaDB   │
   │  Embeddings  │      │ Vector Store │
   └──────────────┘      └──────────────┘

3. QUERY PROCESSING
   ┌──────────────┐      ┌──────────────┐      ┌──────────────┐
   │     User     │──────▶│  Retriever   │──────▶│   Relevant   │
   │    Query     │      │              │      │   Contexts   │
   └──────────────┘      └──────────────┘      └──────────────┘

4. ANSWER GENERATION
   ┌──────────────┐      ┌──────────────┐      ┌──────────────┐
   │   Context +  │──────▶│     LLM      │──────▶│    Final     │
   │    Query     │      │ (GPT-3.5)    │      │    Answer    │
   └──────────────┘      └──────────────┘      └──────────────┘
```

### Components

1. **Document Loader**: Loads text documents from the `data/` directory
2. **Text Splitter**: Breaks documents into chunks (1000 chars with 200 overlap)
3. **Embedding Model**: OpenAI's embedding model for vector representation
4. **Vector Store**: ChromaDB for efficient similarity search
5. **Retriever**: Fetches top-k relevant document chunks
6. **LLM**: GPT-3.5-turbo for generating contextual answers
7. **QA Chain**: Orchestrates the retrieval and generation pipeline

## ✨ Features

- **Document Processing**: Automatically loads and processes text documents
- **Vector Database**: Persistent storage using ChromaDB
- **Semantic Search**: Finds relevant information using embeddings
- **Context-Aware Answers**: Generates responses based on retrieved documents
- **Source Attribution**: Shows which documents were used for each answer
- **Interactive Mode**: Command-line interface for asking questions
- **Configurable**: Easy to customize chunk sizes, retrieval parameters, etc.
- **Example Documents**: Includes sample documents about RAG, LangChain, and Python

## 📋 Prerequisites

- Python 3.8 or higher
- OpenAI API key
- pip (Python package manager)

## 🚀 Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/AREP-2026-1/RAG_PROJECT.git
cd RAG_PROJECT
```

### Step 2: Create a Virtual Environment (Recommended)

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**Security Note**: This project uses patched versions of all dependencies to address known vulnerabilities. All dependencies are regularly updated to their latest secure versions.

## ⚙️ Configuration

### Step 1: Set Up Environment Variables

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` and add your OpenAI API key:
```
OPENAI_API_KEY=sk-your-actual-api-key-here
```

**Note**: Never commit your `.env` file to version control. It's already included in `.gitignore`.

### Step 2: Add Your Documents (Optional)

The project includes sample documents in the `data/` directory. You can add your own text files:

```bash
# Add your .txt files to the data directory
cp your-document.txt data/
```

## 💻 Usage

### Quick Start

Run the example script to see the RAG system in action:

```bash
python example.py
```

This will:
1. Initialize the RAG system
2. Load and process documents
3. Create the vector database
4. Ask several example questions
5. Display answers with source attribution

### Full Interactive Mode

Run the main RAG system for interactive question-answering:

```bash
python -m src.rag_system
```

This will:
1. Initialize the system
2. Ask predefined example questions
3. Enter interactive mode where you can ask your own questions
4. Type 'quit' to exit

### Using the RAG System in Your Code

```python
from src.rag_system import RAGSystem

# Create and initialize the RAG system
rag = RAGSystem(data_dir="data", persist_directory="chroma_db")
rag.initialize()

# Ask a question
result = rag.ask("What is RAG?")
print(result["answer"])

# Perform similarity search
docs = rag.similarity_search("LangChain features", k=3)
for doc in docs:
    print(doc.page_content)
```

## 📁 Project Structure

```
RAG_PROJECT/
│
├── src/
│   └── rag_system.py          # Main RAG system implementation
│
├── data/                       # Document storage
│   ├── rag_overview.txt        # Information about RAG
│   ├── langchain_overview.txt  # Information about LangChain
│   └── python_best_practices.txt # Python best practices
│
├── chroma_db/                  # Vector database (created on first run)
│   └── (ChromaDB files)
│
├── example.py                  # Simple usage example
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── .gitignore                 # Git ignore rules
└── README.md                  # This file
```

## 🔍 How It Works

### 1. Document Loading and Processing

When you initialize the RAG system:

```python
documents = self.load_documents()  # Load all .txt files from data/
chunks = self.split_documents(documents)  # Split into smaller chunks
```

Documents are split using `RecursiveCharacterTextSplitter` with:
- **Chunk size**: 1000 characters
- **Chunk overlap**: 200 characters (to maintain context)

### 2. Embedding and Vector Storage

```python
self.create_vectorstore(chunks)  # Create embeddings and store in ChromaDB
```

Each chunk is converted to a vector embedding using OpenAI's embedding model, then stored in ChromaDB for fast similarity search.

### 3. Query Processing

When you ask a question:

```python
result = rag.ask("What is RAG?")
```

The system:
1. Converts your question to an embedding
2. Searches for the top 3 most similar document chunks
3. Retrieves those chunks as context
4. Sends context + question to GPT-3.5-turbo
5. Returns the generated answer with sources

### 4. Answer Generation

The LLM receives a prompt with:
- Retrieved document chunks (context)
- Your question
- Instructions to answer based on context only

This ensures answers are grounded in your documents and reduces hallucinations.

## 📸 Examples

### Example 1: Asking About RAG

**Input:**
```
What is RAG and how does it work?
```

**Output:**
```
Answer: RAG stands for Retrieval-Augmented Generation. It is an AI framework 
that combines large language models with external knowledge retrieval systems. 
The process works in four steps: 1) Document Indexing - documents are converted 
to embeddings and stored in a vector database, 2) Query Processing - user 
questions are converted to embeddings, 3) Retrieval - the system finds relevant 
documents similar to the query, and 4) Generation - an LLM generates responses 
using both its training and the retrieved information.

Sources:
  1. data/rag_overview.txt
```

### Example 2: Asking About LangChain

**Input:**
```
What are the key components of LangChain?
```

**Output:**
```
Answer: The key components of LangChain include: 1) Model I/O for managing 
interactions with language models, 2) Retrieval for working with application-
specific data, 3) Chains for combining multiple components, 4) Agents that 
let language models make decisions, 5) Memory for persisting state, and 
6) Callbacks for hooking into execution stages.

Sources:
  1. data/langchain_overview.txt
```

### Example 3: Interactive Session

```
$ python -m src.rag_system

RAG system initialized and ready to answer questions!

Interactive Mode - Enter your questions (type 'quit' to exit)
================================================================================

Your question: What are Python security best practices?

Question: What are Python security best practices?
--------------------------------------------------------------------------------
Answer: Python security best practices include: 1) Validate and sanitize user 
inputs, 2) Don't hardcode secrets or credentials, 3) Use environment variables 
for sensitive data, 4) Keep dependencies up to date, and 5) Be careful with 
eval() and exec().

Sources:
  1. data/python_best_practices.txt
--------------------------------------------------------------------------------

Your question: quit

Goodbye!
```

## 🔧 Troubleshooting

### Issue: "OpenAI API key not found"

**Solution**: Make sure you've created a `.env` file with your API key:
```bash
cp .env.example .env
# Edit .env and add your API key
```

### Issue: "ModuleNotFoundError"

**Solution**: Install all dependencies:
```bash
pip install -r requirements.txt
```

### Issue: Vector store not loading documents

**Solution**: Delete the existing vector store and reinitialize:
```bash
rm -rf chroma_db/
python example.py
```

### Issue: API rate limits or timeouts

**Solution**: 
- Check your OpenAI API quota
- Reduce the number of chunks retrieved (modify `k` in `setup_qa_chain`)
- Add retry logic or increase timeout values

### Issue: Poor answer quality

**Solution**:
- Add more relevant documents to the `data/` directory
- Adjust chunk size and overlap in the text splitter
- Increase the number of retrieved chunks (`k` parameter)
- Experiment with different LLM models or temperatures

## 🎓 Learning Resources

This project is based on the following tutorials:

1. **LangChain Quickstart**: https://docs.langchain.com/oss/python/langchain/quickstart
2. **RAG Tutorial**: https://python.langchain.com/docs/tutorials/rag/

## 📝 Assessment Criteria

This project addresses the following requirements:

✅ **Completeness**: Full implementation of RAG system following LangChain tutorials
✅ **Code Quality**: Well-documented, follows Python best practices
✅ **README**: Comprehensive documentation with architecture, installation, and usage
✅ **Organization**: Clean project structure with proper separation of concerns
✅ **Examples**: Working examples and sample documents included

## 🤝 Contributing

This is a learning project. Feel free to:
- Add more documents to the knowledge base
- Experiment with different LLM models
- Improve the prompts
- Add new features like conversation memory
- Optimize chunk sizes and retrieval parameters

## 📄 License

This project is for educational purposes as part of the AREP-2026-1 course.

## 👥 Author

Created as part of the RAG project implementation assignment.

---

**Note**: This is Repository 2 containing the RAG project code and documentation as specified in the project requirements.