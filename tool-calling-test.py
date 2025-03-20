import os
import litellm
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set API keys
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["ANTHROPIC_API_KEY"] = os.getenv("ANTHROPIC_API_KEY")
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

# Define models to test (models that support tool calling)
models = [
    "gpt-4o",
    "gemini-1.5-pro", 
    "claude-3-5-sonnet"
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

# User message for tool calling test
user_message = "What's the weather like in San Francisco today?"

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

# Test each model
for model in models:
    print(f"\n\n----- Testing {model} with tool calling -----")
    try:
        response = litellm.completion(
            model=model,
            messages=[{"role": "user", "content": user_message}],
            tools=tools,
            tool_choice="auto"
        )
        
        # Print the initial response
        content = response.choices[0].message.content
        tool_calls = response.choices[0].message.tool_calls
        
        print(f"Initial response: {content}")
        print(f"Tool calls: {json.dumps(tool_calls, indent=2) if tool_calls else 'None'}")
        
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
                second_response = litellm.completion(
                    model=model,
                    messages=[
                        {"role": "user", "content": user_message},
                        {
                            "role": "assistant",
                            "tool_calls": tool_calls
                        },
                        {
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "name": function_name,
                            "content": json.dumps(weather_result)
                        }
                    ]
                )
                
                # Print the final response
                final_response = second_response.choices[0].message.content
                print(f"Final response: {final_response}")
        
        print(f"Response time: {response.response_ms/1000:.2f} seconds")
        
    except Exception as e:
        print(f"Error with {model}: {e}")
