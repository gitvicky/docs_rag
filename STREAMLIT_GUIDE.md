# Streamlit Web Interface Guide

## 🌐 Overview

The NumPy RAG Assistant now includes a modern web interface built with Streamlit, providing an intuitive, feature-rich alternative to the command-line interface.

## ✨ Features

### Two Versions Available

#### 1. Standard Version (`streamlit_app.py`)
- Clean, simple interface
- Essential chat functionality
- Source citation display
- Basic configuration options
- Good for: Quick deployment, simple use cases

#### 2. Advanced Version (`streamlit_app_advanced.py`) ⭐ **Recommended**
- Multi-tab interface (Chat, Search, Analytics, About)
- Enhanced visual design
- Conversation export to JSON
- Usage analytics dashboard
- Direct documentation search
- Copy-to-clipboard features
- Good for: Full-featured experience, learning, production use

## 🚀 Quick Start

### Method 1: Using the Launcher (Easiest)

```bash
python launch_streamlit.py
```

The launcher will:
1. Check if Streamlit is installed
2. Verify Ollama is running
3. Confirm vector database exists
4. Check required models are installed
5. Let you choose standard or advanced version
6. Launch the app in your browser

### Method 2: Direct Launch

```bash
# Advanced version (recommended)
streamlit run streamlit_app_advanced.py

# Standard version
streamlit run streamlit_app.py

# Custom port
streamlit run streamlit_app_advanced.py --server.port 8502

# Disable CORS (if needed)
streamlit run streamlit_app_advanced.py --server.enableCORS false
```

## 📋 Prerequisites

Before launching:

### 1. Install Streamlit
```bash
pip install streamlit

# Or install all Streamlit dependencies
pip install -r requirements_streamlit.txt
```

### 2. Ensure Ollama is Running
```bash
# In a separate terminal
ollama serve
```

### 3. Verify Vector Database
```bash
# Check if it exists
ls -la numpy_vectordb/

# If not, build it
python build_vector_db_stable.py
```

### 4. Check Models
```bash
ollama list

# Should show:
# - mistral (or mixtral)
# - nomic-embed-text
```

## 🎨 Interface Tour

### Advanced Version Layout

```
┌─────────────────────────────────────────────────────────┐
│  🐍 NumPy RAG Assistant                                 │
│  AI-Powered NumPy Documentation Search & Chat           │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  [💬 Chat] [🔍 Search] [📊 Analytics] [ℹ️ About]       │
│                                                          │
│  Current Tab Content Area                               │
│  - Chat interface with examples                         │
│  - Search with results                                  │
│  - Analytics dashboard                                  │
│  - About & system info                                  │
│                                                          │
└─────────────────────────────────────────────────────────┘

Sidebar:
┌─────────────────┐
│ ⚙️ Configuration │
│                 │
│ Model: [...]    │
│ Temp: [slider]  │
│ Top K: [slider] │
│ [x] Show Sources│
│                 │
│ [Reload] [Clear]│
│ [Export]        │
│                 │
│ 📈 Statistics   │
│ 📚 Quick Links  │
└─────────────────┘
```

### Tab Descriptions

#### 💬 Chat Tab

**Features:**
- Example query buttons organized by category:
  - 🔰 Basics
  - ⚡ Performance  
  - 🧮 Operations
- Chat message history
- Real-time responses
- Optional source citations
- Typing indicator

**How to Use:**
1. Click an example query OR type your own
2. Wait for response (3-6 seconds)
3. Enable "Show Sources" in sidebar for citations
4. Continue conversation with follow-ups

#### 🔍 Search Tab

**Features:**
- Direct documentation search
- Adjustable result count (1-20)
- Expandable result cards
- Full content display
- "Ask about this" buttons

**How to Use:**
1. Enter search query (e.g., "broadcasting")
2. Set number of results
3. Click "Search"
4. Expand results to see full content
5. Click "Ask about this" to start chat about specific doc

#### 📊 Analytics Tab

**Features:**
- Document count
- Message count
- Question count
- Conversation breakdown chart
- Recent query history

**What You'll See:**
- Visual metrics cards
- Bar chart of user vs assistant messages
- Last 5 queries
- Real-time updates

#### ℹ️ About Tab

**Features:**
- Feature list
- Architecture overview
- Quick start guide
- Resource links
- System information display

**Information Shown:**
- Current model
- Temperature setting
- Top K value
- System status

### Sidebar Controls

#### ⚙️ Configuration

**Model Selection:**
```
Dropdown with options:
- mistral (default, 7B)
- mixtral (larger, more capable)
- llama2 (alternative)
- codellama (code-focused)
```

**Temperature Slider:**
```
Range: 0.0 - 1.0
Default: 0.3
- Lower (0.1-0.3): More focused, deterministic
- Higher (0.7-0.9): More creative, varied
```

**Documents to Retrieve:**
```
Range: 1 - 10
Default: 5
- Lower (1-3): Faster, less context
- Higher (7-10): Slower, more context
```

**Show Sources Toggle:**
```
[x] Show Sources
- ON: Display retrieved docs with each answer
- OFF: Show only the answer
```

#### Action Buttons

**Reload:**
- Reinitializes the assistant
- Useful after changing models
- Resets connection

**Clear:**
- Clears conversation history
- Resets assistant memory
- Starts fresh

**Export:**
- Downloads conversation as JSON
- Includes all messages and settings
- Timestamped filename
- Only visible when messages exist

#### Statistics Display

Shows real-time:
- 📚 Number of document chunks
- 💬 Total messages sent

## 🎯 Usage Examples

### Example 1: Quick Question

1. Launch app: `python launch_streamlit.py`
2. Click example: "How do I create a 2D array?"
3. Read response
4. Done!

### Example 2: Learning Session with Sources

1. Launch app
2. Enable "Show Sources" in sidebar
3. Ask: "What is NumPy broadcasting?"
4. Read answer and sources
5. Follow up: "Show me a complex broadcasting example"
6. Export conversation for later

### Example 3: Documentation Search

1. Go to 🔍 Search tab
2. Enter: "matrix multiplication"
3. Set results: 10
4. Click Search
5. Browse results
6. Click "Ask about this" on interesting result
7. Switches to Chat tab with context

### Example 4: Optimizing Settings

1. In sidebar, set:
   - Model: mixtral (for better quality)
   - Temperature: 0.1 (for focused answers)
   - Top K: 8 (for more context)
2. Ask technical question
3. Get detailed, accurate answer

## 🔧 Configuration Tips

### For Speed
```
Model: mistral
Temperature: 0.3
Top K: 3
```

### For Quality
```
Model: mixtral
Temperature: 0.1
Top K: 8
```

### For Creativity
```
Model: mistral
Temperature: 0.7
Top K: 5
```

### For Learning
```
Model: mistral
Temperature: 0.3
Top K: 5
Show Sources: ON
```

## 🐛 Troubleshooting

### App Won't Start

**Error: "Vector database not found"**
```bash
python build_vector_db_stable.py
```

**Error: "Connection refused"**
```bash
# Start Ollama in another terminal
ollama serve
```

**Error: "No module named 'streamlit'"**
```bash
pip install streamlit
```

### App Starts But Has Issues

**Slow responses:**
- Reduce Top K to 3
- Use mistral instead of mixtral
- Check system resources

**Sources not showing:**
- Enable "Show Sources" in sidebar
- Reload the assistant

**"Assistant not initialized":**
- Click "Reload" button
- Check Ollama is running
- Verify vector database exists

### Port Conflicts

**Port 8501 already in use:**
```bash
streamlit run streamlit_app_advanced.py --server.port 8502
```

**Check which ports are in use:**
```bash
lsof -i :8501
```

### Browser Issues

**App not opening automatically:**
- Manually go to: http://localhost:8501

**Browser cached old version:**
- Hard refresh: Ctrl+Shift+R (or Cmd+Shift+R on Mac)
- Clear browser cache

## 💡 Pro Tips

### 1. Use Example Queries
- Great starting point
- Learn query patterns
- Discover capabilities

### 2. Enable Sources for Learning
- See where answers come from
- Verify information
- Learn documentation structure

### 3. Export Important Conversations
- Save for reference
- Track learning progress
- Share with others

### 4. Check Analytics
- See what you've asked
- Track usage patterns
- Identify knowledge gaps

### 5. Use Search for Quick Lookups
- Faster than asking
- Browse related topics
- Find specific sections

### 6. Adjust Settings Per Task
- Speed vs quality tradeoff
- Different models for different tasks
- Temperature affects creativity

## 🚀 Advanced Usage

### Running on Different Port
```bash
streamlit run streamlit_app_advanced.py --server.port 8502
```

### Headless Mode (Server)
```bash
streamlit run streamlit_app_advanced.py --server.headless true
```

### Custom Configuration File
```bash
# Create ~/.streamlit/config.toml
[server]
port = 8501
headless = false

[theme]
primaryColor = "#4B8BBE"
backgroundColor = "#FFFFFF"
```

### Embedding in Existing Site
```bash
# Disable CORS for iframes
streamlit run streamlit_app_advanced.py --server.enableCORS false
```

## 📊 Performance Optimization

### For Faster Loading
1. Use smaller model (mistral vs mixtral)
2. Reduce top_k to 3
3. Disable source display initially
4. Clear conversation regularly

### For Better Quality
1. Use larger model (mixtral)
2. Increase top_k to 8-10
3. Lower temperature (0.1-0.2)
4. Always show sources

### For Balanced Use
1. Use mistral
2. Keep top_k at 5
3. Temperature at 0.3
4. Toggle sources as needed

## 🌍 Deployment

### Local Network Access
```bash
streamlit run streamlit_app_advanced.py --server.address 0.0.0.0
# Access from other devices: http://YOUR_IP:8501
```

### Production Deployment
For production use, consider:
- Streamlit Cloud
- Docker container
- Nginx reverse proxy
- Authentication layer

## 📝 Comparison: Web vs CLI

| Feature | Web Interface | CLI |
|---------|---------------|-----|
| Ease of Use | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Visual Appeal | ⭐⭐⭐⭐⭐ | ⭐ |
| Search Function | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Analytics | ⭐⭐⭐⭐⭐ | ❌ |
| Export | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| Resource Use | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Setup | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

## 🎉 Conclusion

The Streamlit web interface provides a modern, user-friendly way to interact with the NumPy RAG Assistant. It's perfect for:

- 🎓 Learning NumPy
- 💼 Professional development
- 🔍 Documentation browsing
- 📊 Tracking progress
- 💾 Saving conversations

**Get Started:**
```bash
python launch_streamlit.py
```

Happy coding! 🐍✨
