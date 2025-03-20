import os
import time
import litellm
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set API keys
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["ANTHROPIC_API_KEY"] = os.getenv("ANTHROPIC_API_KEY")

# Define models to test (focused on long context models)
models = [
    "openai/gpt-4o",
    "anthropic/claude-3-5-sonnet-latest"
]

# Function to load long text file
def load_long_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    
    # Duplicate the text to make it longer (optional)
    # Uncomment the next line if you need even longer context
    # text = text * 2  
    
    return text

# Function to test long context
def test_long_context(model):
    """Test long context handling for a given model"""
    print(f"\n=== Testing Long Context for {model} ===")
    
    # Path to your long text file
    long_text_path = "docs/llm.txt"  # Update this path to your file
    
    try:
        # Load the long text
        long_text = load_long_text(long_text_path)
        text_length = len(long_text)
        approx_tokens = len(long_text) // 4
        
        print(f"Loaded text with {text_length} characters (approximately {approx_tokens} tokens)")
        
        # User prompt with the long text
        user_message = f"""
        Please provide a 3-bullet summary of the following text:
        
        {long_text}
        """
        
        # Measure time manually
        start_time = time.time()
        
        try:
            response = litellm.completion(
                model=model,
                messages=[{"role": "user", "content": user_message}],
                max_tokens=500  # Limit response length
            )
            
            end_time = time.time()
            
            # Extract and print response
            response_message = response.choices[0].message.content
            print(f"Response:\n{response_message}")
            print(f"Time taken: {end_time - start_time:.2f} seconds")
            print("Test passed successfully!")
            
        except Exception as e:
            end_time = time.time()
            print(f"API Error: {str(e)}")
            print(f"Time taken before error: {end_time - start_time:.2f} seconds")
            print("This could indicate a context length error or other API limitation")
            
    except FileNotFoundError:
        print(f"File not found: {long_text_path}")
        print("Please update the file path or create a sample long text file")
    except Exception as e:
        print(f"Error loading text: {str(e)}")

# Run test for each model
if __name__ == "__main__":
    for model in models:
        test_long_context(model)