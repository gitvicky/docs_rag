#!/usr/bin/env python3
"""
Quick Setup Script for NumPy RAG Assistant
Automates the entire setup process
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(cmd, description):
    """Run a command and handle errors"""
    print(f"\n{'='*60}")
    print(f"🔄 {description}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        print(e.stderr)
        return False

def check_ollama():
    """Check if Ollama is installed and running"""
    print("\n🔍 Checking Ollama installation...")
    
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            timeout=5
        )
        print("✅ Ollama is installed and running")
        return True
    except FileNotFoundError:
        print("❌ Ollama not found. Please install from https://ollama.ai")
        return False
    except subprocess.TimeoutExpired:
        print("⚠️  Ollama might not be running. Try: ollama serve")
        return False
    except Exception as e:
        print(f"❌ Error checking Ollama: {e}")
        return False

def check_model(model_name):
    """Check if a model is available"""
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True
        )
        return model_name in result.stdout
    except:
        return False

def pull_model(model_name):
    """Pull an Ollama model"""
    if check_model(model_name):
        print(f"✅ Model '{model_name}' already available")
        return True
    
    print(f"📥 Pulling model: {model_name}")
    print("This may take a few minutes...")
    
    return run_command(
        f"ollama pull {model_name}",
        f"Downloading {model_name}"
    )

def install_packages():
    """Install required Python packages"""
    packages = [
        "langchain",
        "langchain-core", 
        "langchain-community",
        "langchain-ollama",
        "langchain-text-splitters",
        "chromadb",
        "beautifulsoup4",
        "requests"
    ]
    
    print("\n📦 Installing Python packages...")
    
    cmd = f"{sys.executable} -m pip install --break-system-packages " + " ".join(packages)
    
    return run_command(cmd, "Installing dependencies")

def scrape_docs():
    """Scrape NumPy documentation"""
    if os.path.exists("numpy_docs.json"):
        response = input("\n📄 numpy_docs.json already exists. Re-scrape? (y/n): ")
        if response.lower() != 'y':
            print("Skipping documentation scraping")
            return True
    
    return run_command(
        f"{sys.executable} scrape_numpy_docs.py",
        "Scraping NumPy documentation"
    )

def build_vectordb():
    """Build vector database"""
    if os.path.exists("numpy_vectordb"):
        response = input("\n🗄️  Vector database already exists. Rebuild? (y/n): ")
        if response.lower() != 'y':
            print("Skipping vector database creation")
            return True
    
    return run_command(
        f"{sys.executable} build_vector_db.py",
        "Building vector database (this may take 5-10 minutes)"
    )

def main():
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║     NumPy RAG Assistant - Quick Setup Script              ║
    ║                                                            ║
    ║  This script will:                                         ║
    ║  1. Check Ollama installation                             ║
    ║  2. Pull required models (mistral, nomic-embed-text)      ║
    ║  3. Install Python packages                               ║
    ║  4. Scrape NumPy documentation                            ║
    ║  5. Build vector database                                 ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    response = input("Continue with setup? (y/n): ")
    if response.lower() != 'y':
        print("Setup cancelled")
        return
    
    # Step 1: Check Ollama
    if not check_ollama():
        print("\n⚠️  Please install Ollama and try again")
        print("Visit: https://ollama.ai")
        return
    
    # Step 2: Pull models
    print("\n" + "="*60)
    print("📥 Checking/Pulling Required Models")
    print("="*60)
    
    if not pull_model("mistral"):
        print("\n⚠️  Failed to pull Mistral model")
        return
    
    if not pull_model("nomic-embed-text"):
        print("\n⚠️  Failed to pull nomic-embed-text model")
        return
    
    # Step 3: Install packages
    if not install_packages():
        print("\n⚠️  Failed to install Python packages")
        return
    
    # Step 4: Scrape docs
    if not scrape_docs():
        print("\n⚠️  Failed to scrape documentation")
        return
    
    # Step 5: Build vector database
    if not build_vectordb():
        print("\n⚠️  Failed to build vector database")
        return
    
    # Success!
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                  ✅ Setup Complete!                        ║
    ╚═══════════════════════════════════════════════════════════╝
    
    🚀 You can now run the assistant:
    
        python numpy_rag_assistant.py
    
    📚 For more information, see RAG_README.md
    
    Happy coding with NumPy! 🐍
    """)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSetup cancelled by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
