import os
import time
import base64
import litellm
import random
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set API keys
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["ANTHROPIC_API_KEY"] = os.getenv("ANTHROPIC_API_KEY")

# Define models to test (models with vision capabilities)
models = [
    "openai/gpt-4o",
    "anthropic/claude-3-5-sonnet-latest"
]

# Function to encode image to base64
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Function to test image input
def test_image_input(model):
    """Test image input for a given model"""
    print(f"\n=== Testing Image Input for {model} ===")
    
    # Path to image
    image_path = "docs/ai2.jpg"  # Update with your image path
    
    try:
        # Encode the image
        base64_image = encode_image(image_path)
        
        # Create the message with the image
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "What's in this image? Describe it in detail."},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ]
        
        # Retry logic with exponential backoff
        max_retries = 5
        retry_count = 0
        backoff_time = 2  # Start with 2 seconds
        
        while retry_count < max_retries:
            try:
                # Measure time manually
                start_time = time.time()
                
                response = litellm.completion(
                    model=model,
                    messages=messages
                )
                
                end_time = time.time()
                
                # Extract and print response
                response_message = response.choices[0].message.content
                print(f"Response:\n{response_message}")
                print(f"Time taken: {end_time - start_time:.2f} seconds")
                print("Test passed successfully!")
                break  # Exit loop on success
                
            except Exception as e:
                retry_count += 1
                error_msg = str(e)
                
                # Check if it's an overloaded error
                if "overloaded" in error_msg.lower() and retry_count < max_retries:
                    jitter = random.uniform(0, 0.5)  # Add some randomness
                    wait_time = backoff_time + jitter
                    print(f"Service overloaded. Retrying in {wait_time:.2f} seconds... (Attempt {retry_count}/{max_retries})")
                    time.sleep(wait_time)
                    backoff_time *= 2  # Exponential backoff
                else:
                    if retry_count >= max_retries:
                        print(f"Max retries ({max_retries}) reached. Giving up.")
                    print(f"Error testing {model}: {error_msg}")
                    break
        
    except FileNotFoundError:
        print(f"Image file not found: {image_path}")
        print("Please update the image path to a valid image file")
    except Exception as e:
        print(f"Error testing {model}: {str(e)}")

# Run test for each model
if __name__ == "__main__":
    for model in models:
        test_image_input(model)
        # Add delay between models to avoid overloading
        if model != models[-1]:  # If not the last model
            time.sleep(2)  # Wait 2 seconds between model tests
