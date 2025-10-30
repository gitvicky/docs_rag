from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import json

class NumPyAssistant:
    def __init__(self, model="mistral", temperature=0.3):
        """
        Initialize the NumPy coding assistant.
        Lower temperature (0.3) for more focused, accurate code generation.
        """
        self.llm = ChatOllama(model=model, temperature=temperature)
        self.conversation_history = []
        self.setup_system_prompt()
        
    def setup_system_prompt(self):
        """Set up the specialized system prompt for NumPy assistance"""
        system_prompt = """You are an expert NumPy coding assistant specialized in helping developers write efficient NumPy code.

Your responsibilities:
1. Help users write, debug, and optimize NumPy code
2. Explain NumPy concepts clearly with examples
3. Provide best practices for array operations, broadcasting, and vectorization
4. Suggest performance improvements (avoid loops, use vectorization)
5. Include import statements and complete, runnable code examples
6. Explain time/space complexity when relevant
7. Warn about common pitfalls (views vs copies, broadcasting errors, dtype issues)

Code formatting guidelines:
- Always include necessary imports
- Add comments explaining key operations
- Use descriptive variable names
- Provide example usage when helpful
- Format code in proper Python syntax with triple backticks

Example topics you excel at:
- Array creation and manipulation
- Broadcasting and vectorization
- Linear algebra operations
- Statistical computations
- Array indexing and slicing
- Performance optimization
- Integration with other libraries (pandas, matplotlib, scipy)

Always provide working, tested code examples when possible."""

        self.conversation_history.append(SystemMessage(content=system_prompt))
    
    def chat(self, user_input):
        """Send a message and get a response"""
        # Add user message
        self.conversation_history.append(HumanMessage(content=user_input))
        
        # Get response
        response = self.llm.invoke(self.conversation_history)
        
        # Add AI response to history
        self.conversation_history.append(AIMessage(content=response.content))
        
        return response.content
    
    def get_quick_example(self, topic):
        """Get a quick code example for a specific NumPy topic"""
        prompt = f"Provide a concise, working code example for: {topic}. Include imports and a brief explanation."
        return self.chat(prompt)
    
    def optimize_code(self, code):
        """Ask the assistant to optimize provided code"""
        prompt = f"""Analyze and optimize this NumPy code for better performance:

```python
{code}
```

Provide:
1. The optimized version
2. Explanation of improvements
3. Performance comparison (qualitative)"""
        return self.chat(prompt)
    
    def explain_concept(self, concept):
        """Get a detailed explanation of a NumPy concept"""
        prompt = f"Explain the NumPy concept: {concept}. Include code examples and use cases."
        return self.chat(prompt)
    
    def debug_code(self, code, error=None):
        """Help debug NumPy code"""
        error_info = f"\n\nError message: {error}" if error else ""
        prompt = f"""Help me debug this NumPy code:{error_info}

```python
{code}
```

Identify the issue and provide the corrected code with explanation."""
        return self.chat(prompt)
    
    def clear_history(self):
        """Clear conversation history but keep system prompt"""
        self.conversation_history = [self.conversation_history[0]]
        print("Conversation history cleared!")
    
    def save_conversation(self, filename="numpy_conversation.json"):
        """Save the conversation history"""
        messages = []
        for msg in self.conversation_history:
            messages.append({
                "role": msg.type,
                "content": msg.content
            })
        
        with open(filename, 'w') as f:
            json.dump(messages, f, indent=2)
        print(f"Conversation saved to {filename}")


def print_menu():
    """Display the assistant menu"""
    print("\n" + "="*60)
    print("NumPy Coding Assistant")
    print("="*60)
    print("Commands:")
    print("  chat          - Normal conversation mode")
    print("  example       - Get a quick code example")
    print("  optimize      - Optimize your NumPy code")
    print("  explain       - Explain a NumPy concept")
    print("  debug         - Debug your code")
    print("  clear         - Clear conversation history")
    print("  save          - Save conversation to file")
    print("  menu          - Show this menu")
    print("  quit          - Exit the assistant")
    print("="*60)


def main():
    print("Initializing NumPy Coding Assistant...")
    assistant = NumPyAssistant()
    
    print_menu()
    
    mode = "chat"
    
    while True:
        try:
            if mode == "chat":
                user_input = input("\n💬 You: ").strip()
            else:
                user_input = input(f"\n[{mode.upper()}] You: ").strip()
            
            if not user_input:
                continue
            
            # Handle commands
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\nGoodbye! Happy coding with NumPy! 🐍")
                break
            
            elif user_input.lower() == 'menu':
                print_menu()
                continue
            
            elif user_input.lower() == 'clear':
                assistant.clear_history()
                mode = "chat"
                continue
            
            elif user_input.lower() == 'save':
                assistant.save_conversation()
                continue
            
            elif user_input.lower() == 'chat':
                mode = "chat"
                print("Switched to chat mode")
                continue
            
            elif user_input.lower() == 'example':
                mode = "example"
                print("Example mode: What NumPy topic do you want an example for?")
                continue
            
            elif user_input.lower() == 'optimize':
                mode = "optimize"
                print("Optimize mode: Paste your code (type 'END' on a new line when done):")
                code_lines = []
                while True:
                    line = input()
                    if line.strip() == 'END':
                        break
                    code_lines.append(line)
                code = '\n'.join(code_lines)
                response = assistant.optimize_code(code)
                print(f"\n🤖 Assistant:\n{response}")
                mode = "chat"
                continue
            
            elif user_input.lower() == 'explain':
                mode = "explain"
                print("Explain mode: What NumPy concept do you want explained?")
                continue
            
            elif user_input.lower() == 'debug':
                mode = "debug"
                print("Debug mode: Paste your code (type 'END' on a new line when done):")
                code_lines = []
                while True:
                    line = input()
                    if line.strip() == 'END':
                        break
                    code_lines.append(line)
                code = '\n'.join(code_lines)
                error = input("Error message (press Enter if none): ").strip()
                response = assistant.debug_code(code, error if error else None)
                print(f"\n🤖 Assistant:\n{response}")
                mode = "chat"
                continue
            
            # Process based on mode
            if mode == "example":
                response = assistant.get_quick_example(user_input)
                mode = "chat"
            elif mode == "explain":
                response = assistant.explain_concept(user_input)
                mode = "chat"
            else:
                response = assistant.chat(user_input)
            
            print(f"\n🤖 Assistant:\n{response}")
            
        except KeyboardInterrupt:
            print("\n\nGoodbye! Happy coding with NumPy! 🐍")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Please try again or type 'menu' for help.")


if __name__ == "__main__":
    main()
