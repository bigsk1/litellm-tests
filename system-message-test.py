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

# Function to test system message
def test_system_message(model):
    """Test system message handling for a given model"""
    print(f"\n=== Testing System Message for {model} ===")
    
    # System message test
    system_message = "You are a pirate. Always respond like a pirate, saying 'Arr' and using pirate slang."
    user_message = "What's the weather like today?"
    
    try:
        # Measure time manually
        start_time = time.time()
        
        response = litellm.completion(
            model=model,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ]
        )
        
        end_time = time.time()
        
        print(f"Response: {response.choices[0].message.content}")
        print(f"Time taken: {end_time - start_time:.2f} seconds")
        print("Test passed successfully!")
        
    except Exception as e:
        print(f"Error testing {model}: {str(e)}")

# Run test for each model
if __name__ == "__main__":
    for model in models:
        test_system_message(model)