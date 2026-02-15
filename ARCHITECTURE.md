# RAG System Architecture Diagram

## System Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                         RAG SYSTEM WORKFLOW                          │
└─────────────────────────────────────────────────────────────────────┘

INITIALIZATION PHASE:
──────────────────────

  ┌───────────────┐
  │  Text Files   │ (.txt documents in data/ directory)
  │  (.txt, .pdf) │
  └───────┬───────┘
          │
          ▼
  ┌───────────────────┐
  │ Document Loader   │ (Load all documents)
  │  DirectoryLoader  │
  └─────────┬─────────┘
            │
            ▼
  ┌───────────────────────┐
  │   Text Splitter       │ (Break into chunks)
  │  - Chunk size: 1000   │
  │  - Overlap: 200       │
  └──────────┬────────────┘
             │
             ▼
  ┌──────────────────────────┐
  │   OpenAI Embeddings      │ (Convert to vectors)
  │  text-embedding-ada-002  │
  └────────────┬─────────────┘
               │
               ▼
  ┌──────────────────────────┐
  │   ChromaDB Storage       │ (Persistent vector DB)
  │   Vector Database        │
  └──────────────────────────┘


QUERY PHASE:
────────────

  ┌───────────────┐
  │  User Query   │ "What is RAG?"
  └───────┬───────┘
          │
          ▼
  ┌──────────────────────┐
  │  Query Embedding     │ (Convert query to vector)
  │  OpenAI Embeddings   │
  └──────────┬───────────┘
             │
             ▼
  ┌──────────────────────────┐
  │  Similarity Search       │ (Find relevant chunks)
  │  ChromaDB Retrieval      │
  │  Top k=3 results         │
  └────────────┬─────────────┘
               │
               ▼
  ┌──────────────────────────┐
  │  Retrieved Context       │ (Relevant document chunks)
  └────────────┬─────────────┘
               │
               ▼
  ┌──────────────────────────┐
  │  Prompt Construction     │ (Context + Question)
  │  Custom Prompt Template  │
  └────────────┬─────────────┘
               │
               ▼
  ┌──────────────────────────┐
  │  LLM Generation          │ (Generate answer)
  │  GPT-3.5-turbo           │
  │  Temperature: 0.0        │
  └────────────┬─────────────┘
               │
               ▼
  ┌──────────────────────────┐
  │  Final Answer            │ (With source attribution)
  │  + Source Documents      │
  └──────────────────────────┘
```

## Component Details

### 1. Document Loader (DirectoryLoader)
- **Purpose**: Load documents from file system
- **Supported formats**: .txt files (extensible to .pdf, .docx, etc.)
- **Output**: List of Document objects with content and metadata

### 2. Text Splitter (RecursiveCharacterTextSplitter)
- **Purpose**: Break large documents into manageable chunks
- **Chunk Size**: 1000 characters
- **Overlap**: 200 characters (maintains context across boundaries)
- **Strategy**: Recursive splitting by paragraphs, sentences, then characters

### 3. Embeddings (OpenAIEmbeddings)
- **Model**: text-embedding-ada-002
- **Purpose**: Convert text into numerical vectors (embeddings)
- **Dimensions**: 1536-dimensional vectors
- **Use**: Both document chunks and queries are embedded

### 4. Vector Store (ChromaDB)
- **Purpose**: Store and search embeddings efficiently
- **Type**: Persistent vector database
- **Search Method**: Cosine similarity
- **Retrieval**: Top-k most similar documents

### 5. Retriever
- **Purpose**: Fetch relevant documents for a query
- **Strategy**: Similarity search
- **Parameter k**: Number of documents to retrieve (default: 3)

### 6. LLM (ChatOpenAI)
- **Model**: gpt-3.5-turbo
- **Temperature**: 0.0 (deterministic output)
- **Purpose**: Generate natural language answers
- **Input**: Query + Retrieved context
- **Output**: Contextual answer

### 7. QA Chain (RetrievalQA)
- **Purpose**: Orchestrate the entire RAG pipeline
- **Chain Type**: "stuff" (pass all context at once)
- **Components**: Retriever + LLM + Prompt Template
- **Returns**: Answer + Source documents

## Data Flow Example

```
User Input: "What are the benefits of RAG?"
     │
     ├─► Embedding Model
     │      └─► [0.123, -0.456, 0.789, ...] (1536 dimensions)
     │
     ├─► Vector Search (ChromaDB)
     │      └─► Find top 3 similar chunks:
     │           1. data/rag_overview.txt (similarity: 0.92)
     │           2. data/rag_overview.txt (similarity: 0.88)
     │           3. data/langchain_overview.txt (similarity: 0.76)
     │
     ├─► Prompt Construction
     │      Context: [Retrieved chunks]
     │      Question: "What are the benefits of RAG?"
     │
     ├─► LLM Generation (GPT-3.5)
     │      └─► "RAG provides several benefits including..."
     │
     └─► Output
           Answer: "RAG provides several benefits including..."
           Sources: ["data/rag_overview.txt"]
```

## Key Design Decisions

1. **Chunk Size (1000 chars)**: Balance between context preservation and precision
2. **Chunk Overlap (200 chars)**: Prevents loss of context at boundaries
3. **Top-k Retrieval (3 docs)**: Provides sufficient context without overwhelming LLM
4. **Temperature (0.0)**: Ensures consistent, factual responses
5. **Chain Type (stuff)**: Simple approach for moderate context sizes
6. **Persistent Storage**: ChromaDB persists to disk for faster subsequent loads

## Scalability Considerations

- **Small Scale** (< 1000 docs): Current implementation works well
- **Medium Scale** (1000-10000 docs): Consider batch processing for embeddings
- **Large Scale** (> 10000 docs): Consider:
  - Pinecone or Weaviate for distributed vector search
  - Map-reduce chain type for large contexts
  - Async processing for embeddings
  - Caching frequently asked questions

## Alternative Configurations

### Different Chain Types:
- **map_reduce**: Process chunks separately, then combine
- **refine**: Iteratively refine answer with each chunk
- **map_rerank**: Score each chunk's relevance, use best

### Different Retrievers:
- **SelfQueryRetriever**: Auto-generate metadata filters
- **MultiQueryRetriever**: Generate multiple query variants
- **ContextualCompressionRetriever**: Compress retrieved docs

### Different Vector Stores:
- **FAISS**: Fast CPU-based similarity search
- **Pinecone**: Managed cloud vector database
- **Weaviate**: GraphQL vector search
- **Qdrant**: Production-ready vector engine
