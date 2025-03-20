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
    "gpt-4o-mini", 
    "claude-3-5-sonnet-latest"
]

# Function to test basic completion
def test_basic_completion(model):
    """Test basic completion for a given model"""
    print(f"\n=== Testing Basic Completion for {model} ===")
    
    try:
        # Measure time manually
        start_time = time.time()
        
        response = litellm.completion(
            model=model,
            messages=[{
                "role": "user",
                "content": "What is the capital of France? Answer in one word."
            }]
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
        test_basic_completion(model)