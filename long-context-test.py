import os
import litellm
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set API keys
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["ANTHROPIC_API_KEY"] = os.getenv("ANTHROPIC_API_KEY")
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

# Define models to test (focused on long context models)
models = [
    "gpt-4-turbo",  # 128k context
    "gemini-1.5-pro",  # 1M+ context
    "claude-3-opus"  # 200k context
]

# Function to load long text file
def load_long_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    
    # Duplicate the text to make it longer (optional)
    # Uncomment the next line if you need even longer context
    # text = text * 2  
    
    return text

# Path to your long text file
long_text_path = "docs/transcript.txt"  # Update this path to your file

try:
    # Load the long text
    long_text = load_long_text(long_text_path)
    print(f"Loaded text with {len(long_text)} characters (approximately {len(long_text)/4} tokens)")
    
    # User prompt with the long text
    user_message = f"""
    Please provide a 3-bullet summary of the following text:
    
    {long_text}
    """
    
    # Test each model
    for model in models:
        print(f"\n\n----- Testing {model} with long context -----")
        try:
            response = litellm.completion(
                model=model,
                messages=[{"role": "user", "content": user_message}],
                max_tokens=500  # Limit response length
            )
            
            # Extract and print response
            response_message = response.choices[0].message.content
            print(f"Response from {model}:\n{response_message}")
            print(f"Response time: {response.response_ms/1000:.2f} seconds")
            
        except Exception as e:
            print(f"Error with {model}: {e}")
            print("This could indicate a context length error or other API limitation")
            
except FileNotFoundError:
    print(f"File not found: {long_text_path}")
    print("Please update the file path or create a sample long text file")
