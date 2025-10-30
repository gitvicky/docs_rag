from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# Initialize the LLM
llm = ChatOllama(model="mistral", temperature=0.3)

# Create specialized system prompt for NumPy
system_prompt = """You are an expert NumPy coding assistant. You help developers:

1. Write efficient NumPy code with proper vectorization
2. Debug NumPy errors and issues
3. Optimize code to avoid loops and use broadcasting
4. Explain NumPy concepts with clear examples
5. Provide best practices for array operations

Always include:
- Complete, runnable code with imports
- Clear comments explaining operations
- Performance tips when relevant
- Warnings about common pitfalls (views vs copies, broadcasting, dtype issues)

Format all code properly in Python with ```python blocks."""

# Initialize conversation with system prompt
conversation_history = [SystemMessage(content=system_prompt)]

print("="*60)
print("NumPy Coding Assistant (Simple Version)")
print("="*60)
print("Ask me anything about NumPy!")
print("Type 'quit' to exit, 'clear' to reset conversation")
print("="*60)

while True:
    user_input = input("\n💬 You: ").strip()
    
    if not user_input:
        continue
    
    if user_input.lower() in ['quit', 'exit']:
        print("\nHappy coding with NumPy! 🐍")
        break
    
    if user_input.lower() == 'clear':
        conversation_history = [conversation_history[0]]
        print("Conversation cleared!")
        continue
    
    # Add user message
    conversation_history.append(HumanMessage(content=user_input))
    
    # Get response
    try:
        response = llm.invoke(conversation_history)
        conversation_history.append(AIMessage(content=response.content))
        print(f"\n🤖 Assistant:\n{response.content}")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        # Remove the last user message if there was an error
        conversation_history.pop()
