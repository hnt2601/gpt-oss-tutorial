"""
Example: Function Calling

This example demonstrates how to extend the model's capabilities
by allowing it to call custom functions.

Key Concepts:
- Defining function tools with JSON Schema parameters
- Function call workflow (request -> call -> response)
- Multi-step conversations with function results
- Reasoning summaries
"""

import json
import requests
from pprint import pprint
from src.client import create_client, get_default_model


def get_weather(latitude: float, longitude: float) -> float:
    """
    Get current temperature for provided coordinates.
    
    Args:
        latitude: Latitude coordinate
        longitude: Longitude coordinate
        
    Returns:
        Current temperature in Celsius
    """
    response = requests.get(
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}&longitude={longitude}"
        f"&current=temperature_2m,wind_speed_10m"
        f"&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"
    )
    data = response.json()
    return data['current']['temperature_2m']


def simple_function_calling():
    """
    Example: Basic function calling workflow
    
    Demonstrates the complete cycle:
    1. Model decides to call a function
    2. We execute the function
    3. Model uses the result to generate final response
    """
    client = create_client()
    
    print("=" * 60)
    print("Example: Simple Function Calling")
    print("=" * 60)
    
    # Define the function tool
    tools = [{
        "type": "function",
        "name": "get_weather",
        "description": "Get current temperature for provided coordinates in celsius.",
        "parameters": {
            "type": "object",
            "properties": {
                "latitude": {"type": "number"},
                "longitude": {"type": "number"}
            },
            "required": ["latitude", "longitude"],
            "additionalProperties": False
        },
        "strict": True
    }]
    
    # Initial request
    context = [{"role": "user", "content": "What's the weather like in Paris today?"}]
    
    print("\nUser:", context[0]["content"])
    print("\n📞 Step 1: Model decides to call function...")
    
    response = client.responses.create(
        model=get_default_model(),
        input=context,
        tools=tools,
        store=False,
        include=["reasoning.encrypted_content"]
    )
    
    print("\nResponse output structure:")
    for i, item in enumerate(response.output):
        print(f"  [{i}] Type: {item.type}")
    
    # Get the function call (typically at index 1, after reasoning)
    tool_call = response.output[1]
    print(f"\n🔧 Function to call: {tool_call.name}")
    print(f"   Arguments: {tool_call.arguments}")
    
    # Parse arguments and execute function
    args = json.loads(tool_call.arguments)
    result = get_weather(args["latitude"], args["longitude"])
    
    print(f"\n✅ Function result: {result}°C")
    
    # Add function call and result to context
    context += response.output
    context.append({
        "type": "function_call_output",
        "call_id": tool_call.call_id,
        "output": str(result)
    })
    
    print("\n📞 Step 2: Model generates final response...")
    
    # Get final response
    response_2 = client.responses.create(
        model=get_default_model(),
        input=context,
        tools=tools,
        store=False,
        include=["reasoning.encrypted_content"]
    )
    
    print("\n💬 Final Answer:")
    print(response_2.output_text)
    
    print("\n" + "=" * 60)
    return response_2


def function_with_reasoning_summary():
    """
    Example: Function calling with reasoning summary
    
    Shows how to access the model's reasoning process
    """
    client = create_client()
    
    print("\n" + "=" * 60)
    print("Example: Function Calling with Reasoning Summary")
    print("=" * 60)
    
    response = client.responses.create(
        model=get_default_model(),
        input="What are the main differences between photosynthesis and cellular respiration?",
        reasoning={"summary": "auto"},
    )
    
    print("\nQuery:", "Photosynthesis vs Cellular Respiration")
    
    # Extract reasoning summary
    first_item = response.output[0]
    if hasattr(first_item, 'summary') and first_item.summary:
        summary_text = first_item.summary[0].text
        print("\n🧠 Reasoning Summary:")
        print(summary_text)
    
    print("\n💬 Final Answer:")
    print(response.output_text)
    
    print("\n" + "=" * 60)
    return response


def get_stock_price(symbol: str) -> dict:
    """Mock function to get stock price"""
    # In real scenario, this would call a stock API
    mock_data = {
        "AAPL": {"price": 178.25, "change": +2.5},
        "GOOGL": {"price": 141.50, "change": -1.2},
        "MSFT": {"price": 378.90, "change": +3.8},
    }
    return mock_data.get(symbol, {"price": 0, "change": 0})


def multiple_function_calls():
    """
    Example: Multiple function calls in sequence
    
    Demonstrates how to handle multiple tool uses
    """
    client = create_client()
    
    print("\n" + "=" * 60)
    print("Example: Multiple Function Calls")
    print("=" * 60)
    
    tools = [{
        "type": "function",
        "name": "get_stock_price",
        "description": "Get current stock price and change for a given symbol",
        "parameters": {
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "Stock ticker symbol (e.g., AAPL, GOOGL)"
                }
            },
            "required": ["symbol"],
            "additionalProperties": False
        },
        "strict": True
    }]
    
    context = [{
        "role": "user", 
        "content": "Compare the stock prices of Apple and Microsoft. Which one is performing better today?"
    }]
    
    print("\nUser:", context[0]["content"])
    
    # Model will likely need multiple function calls
    max_iterations = 5
    iteration = 0
    
    while iteration < max_iterations:
        iteration += 1
        print(f"\n🔄 Iteration {iteration}")
        
        response = client.responses.create(
            model=get_default_model(),
            input=context,
            tools=tools,
        )
        
        # Check if there are function calls
        has_function_call = any(
            item.type == "function_call" 
            for item in response.output
        )
        
        if not has_function_call:
            print("✅ No more function calls needed")
            print("\n💬 Final Answer:")
            print(response.output_text)
            break
        
        # Process all function calls
        context += response.output
        
        for item in response.output:
            if item.type == "function_call":
                args = json.loads(item.arguments)
                print(f"   📞 Calling: {item.name}({args})")
                
                result = get_stock_price(args["symbol"])
                print(f"   ✅ Result: ${result['price']} (${result['change']:+.2f})")
                
                context.append({
                    "type": "function_call_output",
                    "call_id": item.call_id,
                    "output": json.dumps(result)
                })
    
    print("\n" + "=" * 60)
    return response


def main():
    """Run all function calling examples"""
    print("\n🚀 GPT-OSS Function Calling Examples")
    print("=" * 60)
    
    # Example 1: Simple function call
    simple_function_calling()
    
    # Example 2: Reasoning summary
    function_with_reasoning_summary()
    
    # Example 3: Multiple calls
    multiple_function_calls()
    
    print("\n✅ All function calling examples completed!")


if __name__ == "__main__":
    main()

