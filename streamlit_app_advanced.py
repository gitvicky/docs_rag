"""
NumPy RAG Assistant - Advanced Streamlit Web Interface
Enhanced version with tabs, search, code highlighting, and export
"""

import streamlit as st
import json
from datetime import datetime
from pathlib import Path

# Import the RAG assistant
try:
    from numpy_rag_assistant import NumPyRAGAssistant
except ImportError:
    st.error("⚠️ Cannot import numpy_rag_assistant.py. Make sure it's in the same directory!")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="NumPy RAG Assistant",
    page_icon="🐍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #4B8BBE 0%, #306998 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0;
    }
    .sub-header {
        text-align: center;
        color: #646464;
        margin-top: 0;
        font-size: 1.2rem;
    }
    .source-box {
        background-color: #e8f4f8;
        border-left: 4px solid #4B8BBE;
        padding: 15px;
        margin: 10px 0;
        border-radius: 8px;
    }
    .stat-metric {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-size: 1.5rem;
        font-weight: bold;
    }
    .feature-card {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #dee2e6;
        margin: 10px 0;
    }
    .code-block {
        background-color: #1e1e1e;
        color: #d4d4d4;
        padding: 15px;
        border-radius: 8px;
        font-family: 'Courier New', monospace;
        overflow-x: auto;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'assistant' not in st.session_state:
    st.session_state.assistant = None
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'show_sources' not in st.session_state:
    st.session_state.show_sources = False
if 'initialized' not in st.session_state:
    st.session_state.initialized = False
if 'search_results' not in st.session_state:
    st.session_state.search_results = None

def initialize_assistant():
    """Initialize the RAG assistant"""
    try:
        with st.spinner("🔄 Loading NumPy RAG Assistant..."):
            assistant = NumPyRAGAssistant(
                vectordb_path="./numpy_vectordb",
                model=st.session_state.get('model', 'mistral'),
                temperature=st.session_state.get('temperature', 0.3),
                top_k=st.session_state.get('top_k', 5)
            )
            st.session_state.assistant = assistant
            st.session_state.initialized = True
            st.success("✅ Assistant initialized successfully!")
            return True
    except Exception as e:
        st.error(f"❌ Failed to initialize assistant: {e}")
        with st.expander("🔧 Troubleshooting Steps"):
            st.markdown("""
            1. **Start Ollama:** `ollama serve`
            2. **Check Vector Database:** `ls numpy_vectordb/`
            3. **Verify Models:** `ollama list`
            4. **Rebuild Database:** `python build_vector_db_stable.py`
            5. **Check Installation:** `python test_imports.py`
            """)
        return False

def display_sources(docs):
    """Display source documents"""
    if not docs:
        return
    
    st.markdown("### 📚 Retrieved Sources")
    for i, doc in enumerate(docs, 1):
        with st.expander(f"📄 Source {i}: {doc.metadata.get('title', 'NumPy Documentation')}", expanded=i==1):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**🔗 URL:** [{doc.metadata.get('source', 'N/A')}]({doc.metadata.get('source', '#')})")
            with col2:
                if st.button(f"📋 Copy", key=f"copy_source_{i}"):
                    st.toast("Link copied!", icon="✅")
            
            st.markdown("**📝 Content:**")
            st.text_area(
                "Content",
                doc.page_content,
                height=200,
                key=f"source_content_{i}",
                label_visibility="collapsed"
            )

def export_conversation():
    """Export conversation to JSON"""
    export_data = {
        "timestamp": datetime.now().isoformat(),
        "messages": st.session_state.messages,
        "settings": {
            "model": st.session_state.model,
            "temperature": st.session_state.temperature,
            "top_k": st.session_state.top_k
        }
    }
    
    filename = f"numpy_chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    json_str = json.dumps(export_data, indent=2)
    
    st.download_button(
        label="📥 Download Conversation",
        data=json_str,
        file_name=filename,
        mime="application/json"
    )

# Sidebar
with st.sidebar:
    st.image("https://numpy.org/images/logo.svg", width=200)
    st.title("⚙️ Configuration")
    
    # Model selection
    model = st.selectbox(
        "🤖 Model",
        ["mistral", "mixtral", "llama2", "codellama"],
        index=0,
        help="Select the Ollama model to use"
    )
    st.session_state.model = model
    
    # Temperature slider
    temperature = st.slider(
        "🌡️ Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.3,
        step=0.1,
        help="Lower = more focused, Higher = more creative"
    )
    st.session_state.temperature = temperature
    
    # Top K slider
    top_k = st.slider(
        "📊 Retrieved Documents",
        min_value=1,
        max_value=10,
        value=5,
        help="Number of documents to retrieve"
    )
    st.session_state.top_k = top_k
    
    # Show sources toggle
    st.session_state.show_sources = st.checkbox(
        "📚 Show Sources",
        value=st.session_state.show_sources
    )
    
    st.divider()
    
    # Action buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Reload", use_container_width=True):
            st.session_state.initialized = False
            st.session_state.assistant = None
            st.rerun()
    
    with col2:
        if st.button("🧹 Clear", use_container_width=True):
            st.session_state.messages = []
            if st.session_state.assistant:
                st.session_state.assistant.clear_history()
            st.rerun()
    
    if len(st.session_state.messages) > 0:
        export_conversation()
    
    st.divider()
    
    # Statistics
    if st.session_state.assistant:
        st.markdown("### 📈 Statistics")
        try:
            count = st.session_state.assistant.vectordb._collection.count()
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("📚 Docs", count)
            with col2:
                st.metric("💬 Messages", len(st.session_state.messages))
        except:
            pass
    
    st.divider()
    
    # Quick links
    st.markdown("### 🔗 Quick Links")
    st.markdown("""
    - [📖 NumPy Docs](https://numpy.org/doc)
    - [🐙 GitHub](#)
    - [❓ Help](TROUBLESHOOTING.md)
    - [🐛 Report Issue](#)
    """)

# Main content
st.markdown('<p class="main-header">🐍 NumPy RAG Assistant</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">AI-Powered NumPy Documentation Search & Chat</p>', unsafe_allow_html=True)

# Initialize assistant if not done
if not st.session_state.initialized:
    if not initialize_assistant():
        st.stop()

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs(["💬 Chat", "🔍 Search", "📊 Analytics", "ℹ️ About"])

# Tab 1: Chat Interface
with tab1:
    # Example queries
    st.markdown("### 💡 Quick Start Examples")
    
    examples = {
        "🔰 Basics": [
            "How do I create a 2D array?",
            "What are NumPy arrays?",
            "Array vs list differences"
        ],
        "⚡ Performance": [
            "How to optimize NumPy code?",
            "What's the difference between view and copy?",
            "Vectorization best practices"
        ],
        "🧮 Operations": [
            "What is NumPy broadcasting?",
            "Explain np.einsum with examples",
            "Matrix multiplication methods"
        ]
    }
    
    cols = st.columns(3)
    for idx, (category, queries) in enumerate(examples.items()):
        with cols[idx]:
            st.markdown(f"**{category}**")
            for query in queries:
                if st.button(query, key=f"example_{category}_{query}", use_container_width=True):
                    st.session_state.messages.append({"role": "user", "content": query})
                    st.rerun()
    
    st.divider()
    
    # Chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            if message["role"] == "assistant" and "sources" in message:
                display_sources(message["sources"])
    
    # Chat input
    if prompt := st.chat_input("Ask me anything about NumPy..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            try:
                with st.spinner("🤔 Thinking..."):
                    docs = st.session_state.assistant.retriever.invoke(prompt)
                    response = st.session_state.assistant.chat(prompt, show_sources=False)
                
                st.markdown(response)
                
                if st.session_state.show_sources and docs:
                    display_sources(docs)
                
                message_data = {"role": "assistant", "content": response}
                if st.session_state.show_sources and docs:
                    message_data["sources"] = docs
                
                st.session_state.messages.append(message_data)
                
            except Exception as e:
                error_msg = f"❌ Error: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})

# Tab 2: Search Interface
with tab2:
    st.markdown("### 🔍 Search NumPy Documentation")
    st.markdown("Search directly through the indexed documentation")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        search_query = st.text_input("Search query:", placeholder="e.g., broadcasting, matrix multiplication, array slicing")
    with col2:
        search_k = st.number_input("Results:", min_value=1, max_value=20, value=5)
    
    if st.button("🔎 Search", type="primary", use_container_width=True):
        if search_query:
            with st.spinner("Searching..."):
                try:
                    results = st.session_state.assistant.vectordb.similarity_search(search_query, k=search_k)
                    st.session_state.search_results = results
                except Exception as e:
                    st.error(f"Search failed: {e}")
    
    if st.session_state.search_results:
        st.markdown(f"### 📄 Found {len(st.session_state.search_results)} Results")
        
        for i, doc in enumerate(st.session_state.search_results, 1):
            with st.expander(f"Result {i}: {doc.metadata.get('title', 'NumPy Documentation')}", expanded=i==1):
                st.markdown(f"**🔗 Source:** [{doc.metadata.get('source', 'N/A')}]({doc.metadata.get('source', '#')})")
                st.markdown("**📝 Content:**")
                st.text_area("", doc.page_content, height=250, key=f"search_result_{i}", label_visibility="collapsed")
                
                if st.button(f"💬 Ask about this", key=f"ask_about_{i}"):
                    prompt = f"Based on this documentation: {doc.page_content[:200]}... Can you explain this?"
                    st.session_state.messages.append({"role": "user", "content": prompt})
                    st.switch_page("💬 Chat")

# Tab 3: Analytics
with tab3:
    st.markdown("### 📊 Usage Analytics")
    
    if st.session_state.assistant:
        try:
            count = st.session_state.assistant.vectordb._collection.count()
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown('<div class="stat-metric">📚<br>' + str(count) + '<br>Documents</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="stat-metric">💬<br>' + str(len(st.session_state.messages)) + '<br>Messages</div>', unsafe_allow_html=True)
            
            with col3:
                user_messages = len([m for m in st.session_state.messages if m["role"] == "user"])
                st.markdown('<div class="stat-metric">❓<br>' + str(user_messages) + '<br>Questions</div>', unsafe_allow_html=True)
            
            st.divider()
            
            # Message breakdown
            if st.session_state.messages:
                st.markdown("### 💬 Conversation Breakdown")
                
                user_msg = [m for m in st.session_state.messages if m["role"] == "user"]
                asst_msg = [m for m in st.session_state.messages if m["role"] == "assistant"]
                
                chart_data = {
                    "Type": ["User Questions", "Assistant Responses"],
                    "Count": [len(user_msg), len(asst_msg)]
                }
                
                st.bar_chart(chart_data, x="Type", y="Count")
                
                # Recent queries
                st.markdown("### 📝 Recent Queries")
                recent = [m["content"][:100] + "..." for m in user_msg[-5:]]
                for i, query in enumerate(reversed(recent), 1):
                    st.text(f"{i}. {query}")
            
        except Exception as e:
            st.error(f"Could not load analytics: {e}")
    else:
        st.info("Initialize the assistant to view analytics")

# Tab 4: About
with tab4:
    st.markdown("### 🎯 About NumPy RAG Assistant")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### ✨ Features
        
        - **RAG-Powered**: Uses official NumPy documentation
        - **Source Citations**: See where answers come from
        - **Semantic Search**: Find relevant docs instantly
        - **Conversation Memory**: Context-aware responses
        - **Multiple Models**: Choose your preferred LLM
        - **Export**: Save conversations for later
        """)
        
        st.markdown("""
        #### 🏗️ Architecture
        
        - **LangChain**: RAG orchestration
        - **Ollama**: Local LLM hosting
        - **ChromaDB**: Vector database
        - **Streamlit**: Web interface
        - **Mistral**: Default language model
        """)
    
    with col2:
        st.markdown("""
        #### 🚀 Quick Start
        
        1. **Initialize**: Click "Reload" to start
        2. **Ask**: Type your NumPy question
        3. **Learn**: Get accurate, sourced answers
        4. **Search**: Find specific documentation
        5. **Export**: Save your conversation
        """)
        
        st.markdown("""
        #### 📚 Resources
        
        - [NumPy Documentation](https://numpy.org/doc)
        - [GitHub Repository](#)
        - [Report Issues](#)
        - [Contribute](#)
        """)
    
    st.divider()
    
    st.markdown("### ⚙️ System Information")
    
    info_cols = st.columns(4)
    with info_cols[0]:
        st.info(f"**Model**\n\n{st.session_state.model}")
    with info_cols[1]:
        st.info(f"**Temperature**\n\n{st.session_state.temperature}")
    with info_cols[2]:
        st.info(f"**Top K**\n\n{st.session_state.top_k}")
    with info_cols[3]:
        status = "🟢 Active" if st.session_state.initialized else "🔴 Inactive"
        st.info(f"**Status**\n\n{status}")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    Built with ❤️ using Streamlit | Powered by Ollama & LangChain | NumPy Documentation © NumPy Contributors
</div>
""", unsafe_allow_html=True)
