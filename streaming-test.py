import os
import time
import litellm
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set API keys
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["ANTHROPIC_API_KEY"] = os.getenv("ANTHROPIC_API_KEY")

# Define models to test
models = [
    "openai/gpt-4o",
    "anthropic/claude-3-5-sonnet-latest"
]

# User message for streaming test
user_message = "Write a short poem about artificial intelligence."

# Function to test streaming
def test_streaming(model):
    """Test streaming for a given model"""
    print(f"\n=== Testing Streaming for {model} ===")
    
    # User message for streaming test
    user_message = "Write a short poem about artificial intelligence."
    
    try:
        # Measure time manually
        start_time = time.time()
        
        print(f"Streaming response:")
        
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
        
        end_time = time.time()
        
        print("\n")
        print(f"Time taken: {end_time - start_time:.2f} seconds")
        print("Test passed successfully!")
        
    except Exception as e:
        print(f"Error testing {model}: {str(e)}")

# Run test for each model
if __name__ == "__main__":
    for model in models:
        test_streaming(model)