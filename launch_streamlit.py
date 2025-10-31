#!/usr/bin/env python3
"""
Streamlit App Launcher for NumPy RAG Assistant
Checks prerequisites and launches the web interface
"""

import subprocess
import sys
import os

def check_ollama():
    """Check if Ollama is running"""
    try:
        import httpx
        response = httpx.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("✅ Ollama is running")
            return True
        else:
            print("⚠️  Ollama responded but with unexpected status")
            return False
    except:
        print("❌ Ollama is not running")
        print("\n🔧 Start Ollama in another terminal:")
        print("   ollama serve")
        return False

def check_vector_db():
    """Check if vector database exists"""
    if os.path.exists("./numpy_vectordb"):
        print("✅ Vector database found")
        return True
    else:
        print("❌ Vector database not found")
        print("\n🔧 Build the database first:")
        print("   python build_vector_db_stable.py")
        return False

def check_models():
    """Check if required Ollama models are installed"""
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        models = result.stdout.lower()
        
        has_mistral = "mistral" in models
        has_nomic = "nomic-embed-text" in models
        
        if has_mistral and has_nomic:
            print("✅ Required models installed")
            return True
        else:
            print("❌ Missing required models")
            if not has_mistral:
                print("   Missing: mistral")
                print("   Install: ollama pull mistral")
            if not has_nomic:
                print("   Missing: nomic-embed-text")
                print("   Install: ollama pull nomic-embed-text")
            return False
            
    except Exception as e:
        print(f"⚠️  Could not check models: {e}")
        return True  # Don't block if check fails

def check_streamlit():
    """Check if Streamlit is installed"""
    try:
        import streamlit
        print("✅ Streamlit installed")
        return True
    except ImportError:
        print("❌ Streamlit not installed")
        print("\n🔧 Install Streamlit:")
        print("   pip install streamlit")
        return False

def main():
    print("="*60)
    print("🐍 NumPy RAG Assistant - Streamlit Launcher")
    print("="*60)
    
    # Check prerequisites
    print("\n📋 Checking prerequisites...")
    print("-"*60)
    
    checks = [
        ("Streamlit", check_streamlit()),
        ("Ollama", check_ollama()),
        ("Vector Database", check_vector_db()),
        ("Ollama Models", check_models())
    ]
    
    all_passed = all(check[1] for check in checks)
    
    print("-"*60)
    
    if not all_passed:
        print("\n❌ Some prerequisites failed")
        print("Please fix the issues above before launching")
        return 1
    
    print("\n✅ All prerequisites met!")
    print("\n🚀 Launching Streamlit app...")
    print("-"*60)
    
    # Choose which app to launch
    print("\nWhich version do you want to launch?")
    print("1. Standard (streamlit_app.py)")
    print("2. Advanced (streamlit_app_advanced.py) - Recommended")
    
    choice = input("\nEnter choice [2]: ").strip() or "2"
    
    if choice == "1":
        app_file = "streamlit_app.py"
    else:
        app_file = "streamlit_app_advanced.py"
    
    if not os.path.exists(app_file):
        print(f"\n❌ {app_file} not found")
        return 1
    
    print(f"\n🌐 Starting {app_file}...")
    print("\n💡 The app will open in your default browser")
    print("📍 URL: http://localhost:8501")
    print("\n⚠️  Press Ctrl+C to stop the server\n")
    print("="*60)
    
    # Launch Streamlit
    try:
        subprocess.run(
            ["streamlit", "run", app_file],
            check=True
        )
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down...")
    except subprocess.CalledProcessError:
        print("\n❌ Failed to launch Streamlit")
        return 1
    
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n👋 Cancelled by user")
        sys.exit(0)
