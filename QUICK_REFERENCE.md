# Quick Reference Guide

## 🚀 Quick Start (30 seconds)

```bash
# Clone and setup
git clone https://github.com/AREP-2026-1/RAG_PROJECT.git
cd RAG_PROJECT
python -m venv venv && source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configure
cp .env.example .env
# Edit .env and add: OPENAI_API_KEY=sk-your-key-here

# Run
python example.py
```

## 📋 Common Commands

```bash
# Test installation
python test_project.py

# Run example
python example.py

# Interactive mode
python -m src.rag_system

# Syntax check
python -m py_compile src/rag_system.py

# Start fresh (delete vector DB)
rm -rf chroma_db/
```

## 💻 Basic Usage in Code

```python
from src.rag_system import RAGSystem

# Initialize
rag = RAGSystem(data_dir="data", persist_directory="chroma_db")
rag.initialize()

# Ask a question
result = rag.ask("What is RAG?")
print(result["answer"])
print(result["sources"])

# Search for similar documents
docs = rag.similarity_search("LangChain", k=3)
```

## 📁 Project Structure

```
RAG_PROJECT/
├── src/
│   ├── __init__.py          # Package initialization
│   └── rag_system.py        # Main RAG implementation (400+ lines)
├── data/                     # Knowledge base documents
│   ├── rag_overview.txt
│   ├── langchain_overview.txt
│   └── python_best_practices.txt
├── chroma_db/               # Vector database (auto-created)
├── example.py               # Quick start example
├── test_project.py          # Validation tests
├── requirements.txt         # Dependencies
├── .env.example             # Environment template
├── README.md                # Main documentation
├── INSTALLATION.md          # Installation guide
├── ARCHITECTURE.md          # Architecture details
└── PROJECT_SUMMARY.md       # Project summary
```

## 🔑 Key Classes and Methods

### RAGSystem Class

```python
# Initialization
__init__(data_dir, persist_directory)

# Document processing
load_documents()              # Load .txt files
split_documents(docs)         # Chunk documents

# Vector store
create_vectorstore(docs)      # Create new DB
load_vectorstore()            # Load existing DB

# Query
initialize(force_reload)      # Setup system
ask(question)                 # Ask and get answer
similarity_search(query, k)   # Find similar docs
```

## ⚙️ Configuration Options

### Text Splitting

```python
chunk_size=1000       # Characters per chunk
chunk_overlap=200     # Overlap between chunks
```

### Retrieval

```python
k=3                   # Number of documents to retrieve
```

### LLM

```python
model_name="gpt-3.5-turbo"
temperature=0.0       # Deterministic output
```

## 🐛 Troubleshooting Quick Fixes

| Problem | Solution |
|---------|----------|
| ModuleNotFoundError | `pip install -r requirements.txt` |
| API key not found | Check `.env` file exists and has correct key |
| Vector DB errors | Delete `chroma_db/` folder and reinitialize |
| Permission errors | Use `python3` and `pip3` on Linux/macOS |
| SSL errors | `pip install --upgrade certifi` |

## 📊 Example Output

```
Question: What is RAG?
────────────────────────────────────────────────────────────────────────────────
Answer: RAG stands for Retrieval-Augmented Generation. It is an AI framework 
that combines large language models with external knowledge retrieval systems...

Sources:
  1. data/rag_overview.txt
────────────────────────────────────────────────────────────────────────────────
```

## 🎯 Key Features

✅ Automatic document loading  
✅ Persistent vector storage  
✅ Semantic search  
✅ Source attribution  
✅ Interactive mode  
✅ Custom prompts  
✅ Error handling  
✅ Well-documented  

## 📚 Documentation Files

- **README.md**: Complete guide (300+ lines)
- **INSTALLATION.md**: Step-by-step setup
- **ARCHITECTURE.md**: System design details
- **PROJECT_SUMMARY.md**: Implementation summary
- **QUICK_REFERENCE.md**: This file

## 🔗 Important Links

- **LangChain Docs**: <https://python.langchain.com/docs/>
- **RAG Tutorial**: <https://python.langchain.com/docs/tutorials/rag/>
- **OpenAI Platform**: <https://platform.openai.com/>
- **ChromaDB Docs**: <https://docs.trychroma.com/>

## 💡 Tips

1. **First Time**: Run `example.py` to see how it works
2. **Development**: Keep virtual environment activated
3. **Testing**: Use `test_project.py` before submitting
4. **Debugging**: Check `.env` file if API errors occur
5. **Performance**: Vector DB is created once and reused
6. **Adding Docs**: Just drop .txt files in `data/` folder
7. **Reset**: Delete `chroma_db/` to rebuild index

## 🎓 Learning Path

1. Read **README.md** - Understand the project
2. Check **ARCHITECTURE.md** - Learn how it works
3. Run **example.py** - See it in action
4. Read **src/rag_system.py** - Study the code
5. Try **interactive mode** - Experiment with queries
6. Modify **data/** files - Test with your documents

## 🔢 By the Numbers

- **Setup Time**: < 5 minutes
- **First Run**: ~30 seconds (creates vector DB)
- **Subsequent Runs**: < 5 seconds (loads existing DB)
- **Lines of Code**: ~400
- **Test Coverage**: 6/6 tests passing
- **Dependencies**: 6 packages
- **Documentation**: 500+ lines

---

**Need Help?** Check README.md for detailed information or INSTALLATION.md for setup issues.
