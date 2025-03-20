import os
import litellm
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set API keys
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["ANTHROPIC_API_KEY"] = os.getenv("ANTHROPIC_API_KEY")
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

# Define models to test
models = [
    "gpt-4o-mini",
    "gemini-1.5-flash", 
    "claude-3-5-sonnet"
]

# User message for streaming test
user_message = "Write a short poem about artificial intelligence."

# Function to handle streaming
def handle_stream(model):
    print(f"\n----- Streaming test for {model} -----")
    try:
        response = litellm.completion(
            model=model,
            messages=[{"role": "user", "content": user_message}],
            stream=True,
            max_tokens=50  # Limit to 50 tokens for quick testing
        )
        
        # Process streaming response
        for chunk in response:
            if hasattr(chunk, 'choices') and len(chunk.choices) > 0:
                if hasattr(chunk.choices[0], 'delta') and hasattr(chunk.choices[0].delta, 'content'):
                    content = chunk.choices[0].delta.content
                    if content:
                        print(content, end="", flush=True)
        
        print("\n")  # Add newline after streaming finishes
        
    except Exception as e:
        print(f"Error with {model}: {e}")

# Test streaming for each model
for model in models:
    handle_stream(model)
