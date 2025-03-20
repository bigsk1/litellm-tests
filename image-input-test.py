import os
import base64
import litellm
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set API keys
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["ANTHROPIC_API_KEY"] = os.getenv("ANTHROPIC_API_KEY")
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

# Define models to test (models with vision capabilities)
models = [
    "gpt-4o",  
    "gemini-1.5-pro",
    "claude-3-opus"
]

# Function to encode image to base64
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Path to image
image_path = "docs/panda.jpg"  # Update with your image path

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
    
    # Test each model
    for model in models:
        print(f"\n\n----- Testing {model} with image input -----")
        try:
            response = litellm.completion(
                model=model,
                messages=messages
            )
            
            # Extract and print response
            response_message = response.choices[0].message.content
            print(f"Response from {model}:\n{response_message}")
            print(f"Response time: {response.response_ms/1000:.2f} seconds")
            
        except Exception as e:
            print(f"Error with {model}: {e}")
    
except FileNotFoundError:
    print(f"Image file not found: {image_path}")
    print("Please update the image path to a valid image file")
except Exception as e:
    print(f"Error encoding image: {e}")
