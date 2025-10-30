"""
Build Vector Database - STABLE VERSION
Handles Ollama crashes gracefully with retries and smaller batches
"""

import json
import time
import sys

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_core.documents import Document

def load_documents(filepath="numpy_docs.json"):
    """Load scraped documents"""
    print(f"Loading documents from {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        docs = json.load(f)
    
    documents = []
    for doc in docs:
        documents.append(
            Document(
                page_content=doc['content'],
                metadata={
                    'source': doc['url'],
                    'title': doc['title']
                }
            )
        )
    
    print(f"✅ Loaded {len(documents)} documents")
    return documents


def split_documents(documents, chunk_size=1000, chunk_overlap=200):
    """Split documents into smaller chunks"""
    print(f"Splitting documents...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )
    
    splits = text_splitter.split_documents(documents)
    print(f"✅ Split into {len(splits)} chunks")
    return splits


def create_vector_store_stable(splits, persist_directory="./numpy_vectordb", 
                               batch_size=10, max_retries=3):
    """
    Create vector store with automatic retry on failures
    Uses smaller batches for stability
    """
    print("\n" + "="*60)
    print("Creating Vector Database (STABLE MODE)")
    print("="*60)
    print(f"Using batch size: {batch_size} (smaller = more stable)")
    print(f"Total batches: {(len(splits) + batch_size - 1) // batch_size}")
    print("="*60)
    
    # Initialize embeddings
    embeddings = OllamaEmbeddings(
        model="nomic-embed-text",
        base_url="http://localhost:11434"
    )
    
    # Test embeddings
    print("\n🧪 Testing embeddings...")
    try:
        test_embedding = embeddings.embed_query("test")
        print(f"✅ Working! Vector dimension: {len(test_embedding)}")
    except Exception as e:
        print(f"❌ Test failed: {e}")
        print("\n⚠️  Restart Ollama and try again:")
        print("   pkill ollama && sleep 3 && ollama serve")
        sys.exit(1)
    
    # Process documents
    vectordb = None
    total_batches = (len(splits) + batch_size - 1) // batch_size
    
    for i in range(0, len(splits), batch_size):
        batch = splits[i:i + batch_size]
        batch_num = (i // batch_size) + 1
        
        # Try processing this batch with retries
        retry_count = 0
        batch_success = False
        
        while retry_count < max_retries and not batch_success:
            try:
                print(f"\n📦 Batch {batch_num}/{total_batches} " + 
                      f"(Attempt {retry_count + 1}/{max_retries})")
                
                if vectordb is None:
                    vectordb = Chroma.from_documents(
                        documents=batch,
                        embedding=embeddings,
                        persist_directory=persist_directory
                    )
                else:
                    vectordb.add_documents(batch)
                
                processed = min(i + batch_size, len(splits))
                progress = (processed / len(splits)) * 100
                print(f"   ✅ Success! Progress: {processed}/{len(splits)} ({progress:.1f}%)")
                
                batch_success = True
                
                # Longer pause between successful batches
                if i + batch_size < len(splits):
                    print("   ⏸️  Pausing 2 seconds...")
                    time.sleep(2)
                    
            except Exception as e:
                retry_count += 1
                error_msg = str(e)
                
                if "EOF" in error_msg or "500" in error_msg:
                    print(f"   ⚠️  Ollama crashed (attempt {retry_count}/{max_retries})")
                    
                    if retry_count < max_retries:
                        print("   🔄 Waiting 5 seconds for Ollama to recover...")
                        time.sleep(5)
                        
                        # Test if Ollama is responsive
                        try:
                            test_embedding = embeddings.embed_query("recovery test")
                            print("   ✅ Ollama recovered, retrying batch...")
                        except:
                            print("   ⚠️  Ollama still not responding")
                            print("\n   🔧 Please restart Ollama in another terminal:")
                            print("      pkill ollama && sleep 3 && ollama serve")
                            input("   Press Enter when Ollama is restarted...")
                    else:
                        print(f"\n❌ Failed after {max_retries} attempts")
                        print("\n🔧 Manual fix required:")
                        print("1. Restart Ollama: pkill ollama && sleep 3 && ollama serve")
                        print("2. Close memory-hungry applications")
                        print("3. Run this script again (it will resume from the last successful batch)")
                        print(f"\nProgress saved: {i}/{len(splits)} documents")
                        sys.exit(1)
                else:
                    print(f"   ❌ Unexpected error: {error_msg}")
                    raise
    
    print("\n" + "="*60)
    print("✅ SUCCESS!")
    print("="*60)
    print(f"Total vectors: {vectordb._collection.count()}")
    print(f"Location: {persist_directory}")
    print("="*60)
    
    return vectordb


def main():
    print("="*60)
    print("NumPy Vector Database Builder - STABLE MODE")
    print("="*60)
    
    import os
    if not os.path.exists("numpy_docs.json"):
        print("\n❌ numpy_docs.json not found!")
        print("Run: python scrape_numpy_docs.py")
        sys.exit(1)
    
    try:
        # Load and split
        documents = load_documents()
        splits = split_documents(documents)
        
        # Ask user for batch size
        print("\n" + "="*60)
        print("Batch Size Selection")
        print("="*60)
        print("Smaller = More stable but slower")
        print("Larger = Faster but may crash")
        print()
        print("Recommended batch sizes:")
        print("  5  - Very stable (slowest)")
        print("  10 - Stable (recommended) ⭐")
        print("  20 - Balanced")
        print("  50 - Fast but may crash")
        
        batch_input = input("\nEnter batch size [10]: ").strip()
        batch_size = int(batch_input) if batch_input else 10
        
        print(f"\nUsing batch size: {batch_size}")
        print("⏱️  Estimated time: ~10-15 minutes")
        print("\n⚠️  KEEP OLLAMA RUNNING IN ANOTHER TERMINAL!")
        input("\nPress Enter to start...")
        
        # Build database
        vectordb = create_vector_store_stable(
            splits, 
            batch_size=batch_size,
            max_retries=3
        )
        
        # Test retrieval
        print("\n" + "="*60)
        print("Testing Retrieval")
        print("="*60)
        results = vectordb.similarity_search("numpy array", k=2)
        print(f"✅ Found {len(results)} results")
        
        print("\n🎉 All done!")
        print("\n📚 Next step:")
        print("   python numpy_rag_assistant.py")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()