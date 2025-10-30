"""
NumPy RAG Assistant
Chatbot with Retrieval Augmented Generation using NumPy documentation
"""

from langchain_ollama import ChatOllama
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate

class NumPyRAGAssistant:
    def __init__(self, 
                 vectordb_path="./numpy_vectordb",
                 model="mistral",
                 temperature=0.3,
                 top_k=5):
        """
        Initialize RAG assistant
        
        Args:
            vectordb_path: Path to the ChromaDB vector store
            model: Ollama model to use
            temperature: LLM temperature (0.0-1.0)
            top_k: Number of documents to retrieve
        """
        print("Loading NumPy RAG Assistant...")
        
        # Initialize embeddings and vector store
        self.embeddings = OllamaEmbeddings(model="nomic-embed-text")
        self.vectordb = Chroma(
            persist_directory=vectordb_path,
            embedding_function=self.embeddings
        )
        self.retriever = self.vectordb.as_retriever(
            search_kwargs={"k": top_k}
        )
        
        # Initialize LLM
        self.llm = ChatOllama(model=model, temperature=temperature)
        
        # Conversation history
        self.conversation_history = []
        
        # Setup RAG chain
        self.setup_rag_chain()
        
        print(f"✅ Loaded with {self.vectordb._collection.count()} document chunks")
    
    def setup_rag_chain(self):
        """Setup the RAG chain with prompt template"""
        
        # RAG prompt template
        template = """You are an expert NumPy coding assistant with access to the official NumPy documentation.

Use the following documentation context to answer the user's question. If the context doesn't contain relevant information, use your general knowledge but mention that it's not from the documentation.

Documentation Context:
{context}

Previous Conversation:
{history}

Guidelines:
1. Provide accurate, working code examples with proper imports
2. Reference the documentation when applicable
3. Explain concepts clearly with examples
4. Highlight best practices and performance tips
5. Warn about common pitfalls
6. If the documentation doesn't cover the topic, say so and provide your best answer

User Question: {question}

Assistant Response:"""

        self.prompt = ChatPromptTemplate.from_template(template)
    
    def format_docs(self, docs):
        """Format retrieved documents for context"""
        formatted = []
        for i, doc in enumerate(docs, 1):
            source = doc.metadata.get('title', 'NumPy Documentation')
            content = doc.page_content
            formatted.append(f"[Source {i}: {source}]\n{content}")
        
        return "\n\n---\n\n".join(formatted)
    
    def format_history(self):
        """Format conversation history"""
        if not self.conversation_history:
            return "No previous conversation"
        
        history = []
        for msg in self.conversation_history[-6:]:  # Last 3 exchanges
            if isinstance(msg, HumanMessage):
                history.append(f"User: {msg.content}")
            elif isinstance(msg, AIMessage):
                history.append(f"Assistant: {msg.content}")
        
        return "\n".join(history)
    
    def chat(self, question, show_sources=False):
        """
        Chat with the assistant
        
        Args:
            question: User's question
            show_sources: Whether to display source documents
            
        Returns:
            Assistant's response
        """
        # Retrieve relevant documents
        docs = self.retriever.invoke(question)
        
        if show_sources:
            print("\n📚 Retrieved Sources:")
            for i, doc in enumerate(docs, 1):
                print(f"\n{i}. {doc.metadata.get('title', 'NumPy Docs')}")
                print(f"   URL: {doc.metadata.get('source', 'N/A')}")
                print(f"   Preview: {doc.page_content[:150]}...")
            print("\n" + "-" * 60)
        
        # Format context and history
        context = self.format_docs(docs)
        history = self.format_history()
        
        # Generate response using RAG
        response = self.llm.invoke(
            self.prompt.format(
                context=context,
                history=history,
                question=question
            )
        )
        
        # Update conversation history
        self.conversation_history.append(HumanMessage(content=question))
        self.conversation_history.append(AIMessage(content=response.content))
        
        return response.content
    
    def search_docs(self, query, k=5):
        """Search documentation directly"""
        results = self.vectordb.similarity_search(query, k=k)
        
        print(f"\n🔍 Search Results for: '{query}'")
        print("=" * 60)
        
        for i, doc in enumerate(results, 1):
            print(f"\n📄 Result {i}:")
            print(f"Title: {doc.metadata.get('title', 'N/A')}")
            print(f"URL: {doc.metadata.get('source', 'N/A')}")
            print(f"Content:\n{doc.page_content[:300]}...")
            print("-" * 60)
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        print("🧹 Conversation history cleared!")


def print_menu():
    """Display menu"""
    print("\n" + "=" * 60)
    print("NumPy RAG Assistant - Powered by Official Documentation")
    print("=" * 60)
    print("Commands:")
    print("  chat          - Ask questions (default mode)")
    print("  sources       - Show retrieved sources with answer")
    print("  search        - Search documentation directly")
    print("  clear         - Clear conversation history")
    print("  stats         - Show database statistics")
    print("  menu          - Show this menu")
    print("  quit          - Exit")
    print("=" * 60)


def main():
    import os
    
    # Check if vector database exists
    if not os.path.exists("./numpy_vectordb"):
        print("❌ Error: Vector database not found!")
        print("\nPlease run these commands first:")
        print("1. python scrape_numpy_docs.py")
        print("2. python build_vector_db.py")
        print("\nThen run this script again.")
        return
    
    try:
        assistant = NumPyRAGAssistant()
    except Exception as e:
        print(f"❌ Error initializing assistant: {e}")
        print("\nMake sure you have:")
        print("1. Ollama running (ollama serve)")
        print("2. Models pulled: ollama pull mistral && ollama pull nomic-embed-text")
        return
    
    print_menu()
    
    show_sources = False
    
    while True:
        try:
            user_input = input("\n💬 You: ").strip()
            
            if not user_input:
                continue
            
            # Handle commands
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Happy coding with NumPy!")
                break
            
            elif user_input.lower() == 'menu':
                print_menu()
                continue
            
            elif user_input.lower() == 'clear':
                assistant.clear_history()
                continue
            
            elif user_input.lower() == 'sources':
                show_sources = not show_sources
                status = "enabled" if show_sources else "disabled"
                print(f"📚 Source display {status}")
                continue
            
            elif user_input.lower() == 'search':
                query = input("🔍 Search query: ").strip()
                if query:
                    assistant.search_docs(query)
                continue
            
            elif user_input.lower() == 'stats':
                count = assistant.vectordb._collection.count()
                print(f"\n📊 Database Statistics:")
                print(f"Total document chunks: {count}")
                continue
            
            # Normal chat
            response = assistant.chat(user_input, show_sources=show_sources)
            print(f"\n🤖 Assistant:\n{response}")
            
        except KeyboardInterrupt:
            print("\n\n👋 Happy coding with NumPy!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Please try again or type 'menu' for help.")


if __name__ == "__main__":
    main()
