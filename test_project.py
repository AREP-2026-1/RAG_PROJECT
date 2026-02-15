"""
Test script to validate the RAG project structure and code quality.
This tests the project without requiring an OpenAI API key.
"""

import os
import sys
import ast


def test_project_structure():
    """Test that all required files and directories exist."""
    print("Testing project structure...")
    
    required_files = [
        "README.md",
        "requirements.txt",
        ".env.example",
        ".gitignore",
        "example.py",
        "src/__init__.py",
        "src/rag_system.py",
    ]
    
    required_dirs = [
        "src",
        "data",
    ]
    
    required_data_files = [
        "data/rag_overview.txt",
        "data/langchain_overview.txt",
        "data/python_best_practices.txt",
    ]
    
    all_required = required_files + required_dirs + required_data_files
    missing = []
    
    for item in all_required:
        if not os.path.exists(item):
            missing.append(item)
            print(f"  ✗ Missing: {item}")
        else:
            print(f"  ✓ Found: {item}")
    
    if missing:
        print(f"\n❌ Project structure test FAILED - Missing {len(missing)} items")
        return False
    else:
        print("\n✓ Project structure test PASSED")
        return True


def test_python_syntax():
    """Test that all Python files have valid syntax."""
    print("\nTesting Python syntax...")
    
    python_files = [
        "src/__init__.py",
        "src/rag_system.py",
        "example.py",
    ]
    
    errors = []
    
    for file_path in python_files:
        try:
            with open(file_path, 'r') as f:
                code = f.read()
            ast.parse(code)
            print(f"  ✓ {file_path} - Syntax OK")
        except SyntaxError as e:
            print(f"  ✗ {file_path} - Syntax Error: {e}")
            errors.append(file_path)
    
    if errors:
        print(f"\n❌ Syntax test FAILED - {len(errors)} file(s) with errors")
        return False
    else:
        print("\n✓ Syntax test PASSED")
        return True


def test_rag_class_structure():
    """Test that the RAGSystem class has all required methods."""
    print("\nTesting RAGSystem class structure...")
    
    with open("src/rag_system.py", 'r') as f:
        code = f.read()
    
    tree = ast.parse(code)
    
    # Find the RAGSystem class
    rag_class = None
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == "RAGSystem":
            rag_class = node
            break
    
    if not rag_class:
        print("  ✗ RAGSystem class not found")
        print("\n❌ Class structure test FAILED")
        return False
    
    print(f"  ✓ Found RAGSystem class")
    
    # Check for required methods
    required_methods = [
        "__init__",
        "load_documents",
        "split_documents",
        "create_vectorstore",
        "load_vectorstore",
        "setup_qa_chain",
        "initialize",
        "ask",
        "similarity_search",
    ]
    
    found_methods = [node.name for node in rag_class.body if isinstance(node, ast.FunctionDef)]
    
    missing_methods = []
    for method in required_methods:
        if method in found_methods:
            print(f"  ✓ Method: {method}")
        else:
            print(f"  ✗ Missing method: {method}")
            missing_methods.append(method)
    
    if missing_methods:
        print(f"\n❌ Class structure test FAILED - Missing {len(missing_methods)} method(s)")
        return False
    else:
        print("\n✓ Class structure test PASSED")
        return True


def test_documentation():
    """Test that files have proper documentation."""
    print("\nTesting documentation...")
    
    # Test README
    with open("README.md", 'r') as f:
        readme_content = f.read()
    
    required_sections = [
        "Overview",
        "Architecture",
        "Installation",
        "Usage",
        "Project Structure",
    ]
    
    missing_sections = []
    for section in required_sections:
        if section.lower() in readme_content.lower():
            print(f"  ✓ README has {section} section")
        else:
            print(f"  ✗ README missing {section} section")
            missing_sections.append(section)
    
    # Test that Python files have docstrings
    python_files = ["src/rag_system.py", "example.py"]
    
    for file_path in python_files:
        with open(file_path, 'r') as f:
            code = f.read()
        tree = ast.parse(code)
        
        if ast.get_docstring(tree):
            print(f"  ✓ {file_path} has module docstring")
        else:
            print(f"  ✗ {file_path} missing module docstring")
            missing_sections.append(f"{file_path} docstring")
    
    if missing_sections:
        print(f"\n❌ Documentation test FAILED - Missing {len(missing_sections)} section(s)")
        return False
    else:
        print("\n✓ Documentation test PASSED")
        return True


def test_requirements():
    """Test that requirements.txt has necessary dependencies."""
    print("\nTesting requirements.txt...")
    
    with open("requirements.txt", 'r') as f:
        requirements = f.read()
    
    required_packages = [
        "langchain",
        "chromadb",
        "pypdf",
        "python-dotenv",
        "langchain-openai",
        "langchain-community",
    ]
    
    missing_packages = []
    for package in required_packages:
        if package in requirements:
            print(f"  ✓ {package}")
        else:
            print(f"  ✗ Missing: {package}")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n❌ Requirements test FAILED - Missing {len(missing_packages)} package(s)")
        return False
    else:
        print("\n✓ Requirements test PASSED")
        return True


def test_data_files():
    """Test that data files contain content."""
    print("\nTesting data files...")
    
    data_files = [
        "data/rag_overview.txt",
        "data/langchain_overview.txt",
        "data/python_best_practices.txt",
    ]
    
    empty_files = []
    for file_path in data_files:
        with open(file_path, 'r') as f:
            content = f.read().strip()
        
        if len(content) > 100:  # Should have substantial content
            print(f"  ✓ {file_path} ({len(content)} chars)")
        else:
            print(f"  ✗ {file_path} is too short or empty")
            empty_files.append(file_path)
    
    if empty_files:
        print(f"\n❌ Data files test FAILED - {len(empty_files)} file(s) with issues")
        return False
    else:
        print("\n✓ Data files test PASSED")
        return True


def main():
    """Run all tests."""
    print("=" * 70)
    print("RAG PROJECT - VALIDATION TESTS")
    print("=" * 70)
    print()
    
    tests = [
        ("Project Structure", test_project_structure),
        ("Python Syntax", test_python_syntax),
        ("RAG Class Structure", test_rag_class_structure),
        ("Documentation", test_documentation),
        ("Requirements", test_requirements),
        ("Data Files", test_data_files),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ {test_name} test FAILED with exception: {e}")
            results.append((test_name, False))
        print()
    
    # Print summary
    print("=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status} - {test_name}")
    
    print()
    print(f"Total: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests PASSED! The project is ready.")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) FAILED. Please review the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
