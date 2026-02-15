# Installation Guide

This guide will walk you through setting up the RAG Project on your local machine.

## Prerequisites

Before you begin, ensure you have the following installed:

1. **Python 3.8 or higher**

   ```bash
   python --version
   # or
   python3 --version
   ```

2. **pip** (Python package manager)

   ```bash
   pip --version
   # or
   pip3 --version
   ```

3. **Git**

   ```bash
   git --version
   ```

4. **OpenAI API Account**
   - Sign up at <https://platform.openai.com/>
   - Generate an API key from your account dashboard

## Step-by-Step Installation

### Step 1: Clone the Repository

```bash
# Clone the repository
git clone https://github.com/AREP-2026-1/RAG_PROJECT.git

# Navigate to the project directory
cd RAG_PROJECT
```

### Step 2: Create a Virtual Environment (Recommended)

Creating a virtual environment isolates your project dependencies from other Python projects.

#### On Windows

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate
```

#### On macOS/Linux

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt indicating the virtual environment is active.

### Step 3: Install Dependencies

With your virtual environment activated, install the required packages:

```bash
pip install -r requirements.txt
```

This will install:

- langchain (core framework)
- langchain-community (community integrations)
- langchain-openai (OpenAI integration)
- chromadb (vector database)
- pypdf (PDF processing)
- python-dotenv (environment variable management)

**Note**: Installation may take a few minutes depending on your internet connection.

### Step 4: Set Up Environment Variables

1. Copy the example environment file:

```bash
# On Windows
copy .env.example .env

# On macOS/Linux
cp .env.example .env
```

1. Open the `.env` file in a text editor:

```bash
# Using nano (Linux/macOS)
nano .env

# Using notepad (Windows)
notepad .env

# Or use any text editor like VS Code, Sublime, etc.
code .env
```

1. Add your OpenAI API key:

```
OPENAI_API_KEY=sk-your-actual-api-key-here
```

1. Save and close the file.

**Important Security Notes:**

- Never commit your `.env` file to version control
- Never share your API key publicly
- The `.env` file is already in `.gitignore`

### Step 5: Verify Installation

Run the validation test to ensure everything is set up correctly:

```bash
python test_project.py
```

You should see output indicating all tests passed:

```
🎉 All tests PASSED! The project is ready.
```

### Step 6: Run the Example

Try running the example script:

```bash
python example.py
```

This will:

1. Initialize the RAG system
2. Load and process documents
3. Create the vector database
4. Ask several example questions
5. Display answers with source attribution

### Step 7: Run Interactive Mode

For interactive question-answering:

```bash
python -m src.rag_system
```

Type your questions and get answers in real-time. Type `quit` to exit.

## Troubleshooting

### Issue: "No module named 'langchain'"

**Solution**: Make sure you activated the virtual environment and installed dependencies:

```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Issue: "OpenAI API key not found"

**Solution**:

1. Ensure you created the `.env` file
2. Verify your API key is correct and starts with "sk-"
3. Check there are no extra spaces in the `.env` file

### Issue: "Permission denied" errors

**Solution**:

- On Linux/macOS, you may need to use `python3` and `pip3` instead
- Ensure you have write permissions in the project directory

### Issue: SSL Certificate errors

**Solution**:

```bash
pip install --upgrade certifi
```

### Issue: Package installation fails

**Solution**:

```bash
# Upgrade pip first
pip install --upgrade pip

# Then try installing requirements again
pip install -r requirements.txt
```

### Issue: ChromaDB errors on Windows

**Solution**:

- Install Microsoft C++ Build Tools
- Or use WSL (Windows Subsystem for Linux)

## Verifying Your Installation

After installation, verify that you can import key modules:

```bash
python -c "from src.rag_system import RAGSystem; print('✓ RAGSystem imported successfully')"
```

## Updating the Project

To update to the latest version:

```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install --upgrade -r requirements.txt
```

## Deactivating the Virtual Environment

When you're done working on the project:

```bash
deactivate
```

## Uninstalling

To remove the project:

1. Deactivate the virtual environment:

```bash
deactivate
```

1. Delete the project directory:

```bash
# Navigate to parent directory
cd ..

# Remove project directory
rm -rf RAG_PROJECT  # Linux/macOS
# or
rmdir /s RAG_PROJECT  # Windows
```

## Next Steps

After successful installation:

1. Read the [README.md](README.md) for usage instructions
2. Check [ARCHITECTURE.md](ARCHITECTURE.md) to understand the system design
3. Explore the sample documents in the `data/` directory
4. Add your own documents to the `data/` directory
5. Experiment with different questions in interactive mode

## Getting Help

If you encounter issues:

1. Check this installation guide
2. Review the troubleshooting section
3. Ensure all prerequisites are met
4. Verify your Python and pip versions
5. Check that your OpenAI API key is valid and has available credits

## System Requirements

- **Operating System**: Windows 10+, macOS 10.14+, or Linux
- **Python**: 3.8 or higher (3.9+ recommended)
- **RAM**: At least 4GB (8GB+ recommended)
- **Disk Space**: At least 500MB for dependencies
- **Internet**: Required for OpenAI API calls

## Optional Tools

For a better development experience:

- **VS Code**: Recommended IDE with Python extension
- **iPython**: Interactive Python shell
- **Jupyter Notebook**: For experimental development

Install with:

```bash
pip install ipython jupyter
```

---

**Congratulations!** You've successfully installed the RAG Project. You're now ready to start asking questions and exploring the capabilities of Retrieval-Augmented Generation.
