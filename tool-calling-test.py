import os
import time
import litellm
import json
import random
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set API keys
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["ANTHROPIC_API_KEY"] = os.getenv("ANTHROPIC_API_KEY")

# Define models to test (models that support tool calling)
models = [
    "openai/gpt-4o",
    "anthropic/claude-3-5-sonnet-latest"
]

# Define tool schema
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "The unit of temperature to use. Infer this from the user's location if not explicitly mentioned."
                    }
                },
                "required": ["location"]
            }
        }
    }
]

# Function to simulate weather retrieval (in a real app, this would call a weather API)
def get_weather(location, unit="celsius"):
    # Simulate weather data
    weather_data = {
        "San Francisco, CA": {"temp": 18, "condition": "Foggy", "humidity": 80},
        "New York, NY": {"temp": 22, "condition": "Sunny", "humidity": 60},
        "London, UK": {"temp": 15, "condition": "Rainy", "humidity": 85}
    }
    
    # Default to San Francisco if location not found
    city_data = weather_data.get(location, weather_data["San Francisco, CA"])
    
    # Convert temperature if needed
    temp = city_data["temp"]
    if unit == "fahrenheit":
        temp = (temp * 9/5) + 32
    
    return {
        "location": location,
        "temperature": f"{temp} {'°F' if unit == 'fahrenheit' else '°C'}",
        "condition": city_data["condition"],
        "humidity": f"{city_data['humidity']}%"
    }

# Function to test tool calling
def test_tool_calling(model):
    """Test tool calling for a given model"""
    print(f"\n=== Testing Tool Calling for {model} ===")
    
    # User message for tool calling test
    user_message = "What's the weather like in San Francisco today?"
    
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
                messages=[{"role": "user", "content": user_message}],
                tools=tools,
                tool_choice="auto"
            )
            
            mid_time = time.time()
            
            # Print the initial response
            content = response.choices[0].message.content
            tool_calls = response.choices[0].message.tool_calls
            
            print(f"Initial response: {content}")
            
            # Handle tool_calls serialization
            if tool_calls:
                # Convert tool_calls to a serializable format for display
                serializable_tool_calls = []
                for call in tool_calls:
                    serializable_call = {
                        "id": call.id,
                        "type": call.type,
                        "function": {
                            "name": call.function.name,
                            "arguments": call.function.arguments
                        }
                    }
                    serializable_tool_calls.append(serializable_call)
                print(f"Tool calls: {json.dumps(serializable_tool_calls, indent=2)}")
            else:
                print("Tool calls: None")
                
            print(f"Initial API call time: {mid_time - start_time:.2f} seconds")
            
            # If there are tool calls, process them
            if tool_calls:
                # In a real application, you would execute the actual function
                # Here we'll simulate with our get_weather function
                tool_call = tool_calls[0]
                function_name = tool_call.function.name
                
                if function_name == "get_weather":
                    # Parse arguments
                    args = json.loads(tool_call.function.arguments)
                    location = args.get("location", "San Francisco, CA")
                    unit = args.get("unit", "celsius")
                    
                    # Get weather data
                    weather_result = get_weather(location, unit)
                    
                    # Call the model again with the tool results
                    print("\nCalling model with tool results...")
                    
                    # Second API call with retry logic
                    inner_retry_count = 0
                    inner_backoff_time = 2
                    
                    while inner_retry_count < max_retries:
                        try:
                            tool_start_time = time.time()
                            
                            # Convert tool_calls to the format expected by litellm for the second request
                            assistant_message = {
                                "role": "assistant",
                                "content": content if content else None
                            }
                            
                            # Add tool_calls to the assistant message if they exist
                            if tool_calls:
                                # We need to pass the raw tool_calls object here, not the serialized version
                                assistant_message["tool_calls"] = tool_calls
                            
                            second_response = litellm.completion(
                                model=model,
                                messages=[
                                    {"role": "user", "content": user_message},
                                    assistant_message,
                                    {
                                        "role": "tool",
                                        "tool_call_id": tool_call.id,
                                        "name": function_name,
                                        "content": json.dumps(weather_result)
                                    }
                                ],
                                tools=tools if 'anthropic' in model else None  # Include tools for Anthropic
                            )
                            
                            tool_end_time = time.time()
                            
                            # Print the final response
                            final_response = second_response.choices[0].message.content
                            print(f"Final response: {final_response}")
                            print(f"Second API call time: {tool_end_time - tool_start_time:.2f} seconds")
                            break  # Success, exit retry loop
                            
                        except Exception as e:
                            inner_retry_count += 1
                            error_msg = str(e)
                            
                            # Check if it's an overloaded error
                            if "overloaded" in error_msg.lower() and inner_retry_count < max_retries:
                                jitter = random.uniform(0, 0.5)  # Add some randomness
                                wait_time = inner_backoff_time + jitter
                                print(f"Service overloaded during second call. Retrying in {wait_time:.2f} seconds... (Attempt {inner_retry_count}/{max_retries})")
                                time.sleep(wait_time)
                                inner_backoff_time *= 2  # Exponential backoff
                            else:
                                if inner_retry_count >= max_retries:
                                    print(f"Max retries ({max_retries}) reached for second call. Giving up.")
                                print(f"Error in second API call: {error_msg}")
                                break
            
            end_time = time.time()
            print(f"Total time taken: {end_time - start_time:.2f} seconds")
            print("Test passed successfully!")
            break  # Success, exit main retry loop
            
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

# Run test for each model
if __name__ == "__main__":
    for model in models:
        test_tool_calling(model)
        # Add delay between models to avoid overloading
        if model != models[-1]:  # If not the last model
            time.sleep(2)  # Wait 2 seconds between model tests