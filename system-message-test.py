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

# System message test
system_message = "You are a pirate. Always respond like a pirate, saying 'Arr' and using pirate slang."
user_message = "What's the weather like today?"

# Test each model
for model in models:
    print(f"\n\n----- Testing {model} with system message -----")
    try:
        response = litellm.completion(
            model=model,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ]
        )
        
        # Extract and print response
        response_message = response.choices[0].message.content
        print(f"Response from {model}: {response_message}")
        print(f"Response time: {response.response_ms/1000:.2f} seconds")
        
    except Exception as e:
        print(f"Error with {model}: {e}")
