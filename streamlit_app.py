"""
NumPy RAG Assistant - Streamlit Web Interface
A modern web UI for the NumPy RAG chatbot with source citations and search
"""

import streamlit as st
import sys
from pathlib import Path
import time

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

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #4B8BBE;
        text-align: center;
        margin-bottom: 0;
    }
    .sub-header {
        text-align: center;
        color: #646464;
        margin-top: 0;
    }
    .stChatMessage {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 10px;
        margin: 5px 0;
    }
    .source-box {
        background-color: #e8f4f8;
        border-left: 4px solid #4B8BBE;
        padding: 10px;
        margin: 10px 0;
        border-radius: 5px;
    }
    .example-query {
        background-color: #f0f2f6;
        padding: 8px 12px;
        border-radius: 5px;
        margin: 5px;
        cursor: pointer;
        display: inline-block;
    }
    .stat-box {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
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
            return True
    except Exception as e:
        st.error(f"❌ Failed to initialize assistant: {e}")
        st.info("""
        **Troubleshooting:**
        1. Make sure Ollama is running: `ollama serve`
        2. Verify vector database exists: `ls numpy_vectordb/`
        3. Check models are installed: `ollama list`
        4. Rebuild database if needed: `python build_vector_db_stable.py`
        """)
        return False

def display_sources(docs):
    """Display source documents in a nice format"""
    if not docs:
        return
    
    st.markdown("### 📚 Retrieved Sources")
    for i, doc in enumerate(docs, 1):
        with st.expander(f"📄 Source {i}: {doc.metadata.get('title', 'NumPy Documentation')}"):
            st.markdown(f"**URL:** [{doc.metadata.get('source', 'N/A')}]({doc.metadata.get('source', '#')})")
            st.markdown("**Content:**")
            st.text(doc.page_content[:500] + "..." if len(doc.page_content) > 500 else doc.page_content)

def format_response(response, docs=None):
    """Format the response with optional sources"""
    st.markdown(response)
    
    if st.session_state.show_sources and docs:
        st.divider()
        display_sources(docs)

# Sidebar
with st.sidebar:
    st.image("https://numpy.org/images/logo.svg", width=200)
    st.title("⚙️ Settings")
    
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
        "📊 Documents to Retrieve",
        min_value=1,
        max_value=10,
        value=5,
        help="Number of relevant documents to retrieve"
    )
    st.session_state.top_k = top_k
    
    # Show sources toggle
    st.session_state.show_sources = st.checkbox(
        "📚 Show Sources",
        value=st.session_state.show_sources,
        help="Display retrieved documentation sources"
    )
    
    st.divider()
    
    # Initialize/Reinitialize button
    if st.button("🔄 (Re)Initialize Assistant", use_container_width=True):
        st.session_state.initialized = False
        st.session_state.assistant = None
        initialize_assistant()
        st.rerun()
    
    # Clear conversation button
    if st.button("🧹 Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        if st.session_state.assistant:
            st.session_state.assistant.clear_history()
        st.rerun()
    
    st.divider()
    
    # Statistics
    if st.session_state.assistant:
        st.markdown("### 📈 Statistics")
        try:
            count = st.session_state.assistant.vectordb._collection.count()
            st.metric("Document Chunks", count)
            st.metric("Messages", len(st.session_state.messages))
        except:
            pass
    
    st.divider()
    
    # Info
    st.markdown("""
    ### ℹ️ About
    This RAG assistant uses official NumPy documentation to provide accurate, sourced answers.
    
    **Features:**
    - 🎯 Grounded in official docs
    - 📚 Source citations
    - 💬 Conversation memory
    - 🔍 Semantic search
    """)
    
    st.markdown("---")
    st.markdown("Made with ❤️ using [Streamlit](https://streamlit.io)")

# Main content
st.markdown('<p class="main-header">🐍 NumPy RAG Assistant</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Powered by Official NumPy Documentation</p>', unsafe_allow_html=True)

# Initialize assistant if not done
if not st.session_state.initialized:
    if not initialize_assistant():
        st.stop()

# Example queries
st.markdown("### 💡 Example Queries")
col1, col2, col3 = st.columns(3)

example_queries = [
    "How do I create a 2D array?",
    "What is NumPy broadcasting?",
    "Explain np.einsum with examples",
    "How to optimize NumPy code?",
    "What's the difference between view and copy?",
    "Matrix multiplication methods"
]

for idx, query in enumerate(example_queries):
    col = [col1, col2, col3][idx % 3]
    with col:
        if st.button(query, key=f"example_{idx}", use_container_width=True):
            # Add to messages and process
            st.session_state.messages.append({"role": "user", "content": query})
            st.rerun()

st.divider()

# Chat interface
st.markdown("### 💬 Chat")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        # Display sources if available
        if message["role"] == "assistant" and "sources" in message:
            display_sources(message["sources"])

# Chat input
if prompt := st.chat_input("Ask me anything about NumPy..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        try:
            # Get response with streaming effect
            message_placeholder.markdown("🤔 Thinking...")
            
            # Retrieve documents
            docs = st.session_state.assistant.retriever.invoke(prompt)
            
            # Generate response
            response = st.session_state.assistant.chat(prompt, show_sources=False)
            
            # Display response with typing effect
            full_response = ""
            for chunk in response.split():
                full_response += chunk + " "
                message_placeholder.markdown(full_response + "▌")
                time.sleep(0.02)
            
            message_placeholder.markdown(response)
            
            # Display sources if enabled
            if st.session_state.show_sources and docs:
                display_sources(docs)
            
            # Add to messages
            message_data = {
                "role": "assistant",
                "content": response
            }
            if st.session_state.show_sources and docs:
                message_data["sources"] = docs
            
            st.session_state.messages.append(message_data)
            
        except Exception as e:
            error_msg = f"❌ Error: {str(e)}"
            message_placeholder.error(error_msg)
            st.session_state.messages.append({
                "role": "assistant",
                "content": error_msg
            })

# Footer
st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    **🚀 Quick Tips:**
    - Be specific in your questions
    - Enable "Show Sources" for citations
    - Adjust temperature for creativity
    """)

with col2:
    st.markdown("""
    **🔧 Troubleshooting:**
    - Make sure Ollama is running
    - Check vector database exists
    - Reinitialize if needed
    """)

with col3:
    st.markdown("""
    **📚 Resources:**
    - [NumPy Docs](https://numpy.org/doc)
    - [Project GitHub](#)
    - [Report Issue](#)
    """)
