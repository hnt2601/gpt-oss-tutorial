"""
Example: Reasoning with Tool Calling

This example demonstrates how to use reasoning models with function calling
capabilities to solve problems step-by-step.

Key Concepts:
- Tool/Function calling with reasoning models
- Streaming and non-streaming responses
- Automatic and named function calling
- Extracting reasoning content and tool calls

Requirements:
- Model must support tool/function calling
- Model should support reasoning_content field (for reasoning models)
- Compatible models: deepseek-r1, qwq-32b, or similar reasoning models

Note: If your model doesn't support tool calling, this example will show
warning messages but won't crash. The model will return normal text responses
instead of tool calls.
"""

from src.client import create_client, get_default_model


# Now, simulate a tool call
def get_current_weather(city: str, state: str, unit: "str"):
    return (
        "The weather in Dallas, Texas is 85 degrees fahrenheit. It is "
        "partly cloudly, with highs in the 90's."
    )


available_tools = {"get_current_weather": get_current_weather}

properties = {
    "city": {
        "type": "string",
        "description": "The city to find the weather for, e.g. 'San Francisco'",
    },
    "state": {
        "type": "string",
        "description": "the two-letter abbreviation for the state that the city is"
        " in, e.g. 'CA' which would mean 'California'",
    },
    "unit": {
        "type": "string",
        "description": "The unit to fetch the temperature in",
        "enum": ["celsius", "fahrenheit"],
    },
}

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": properties,
                "required": ["city", "state", "unit"],
            },
        },
    }
]
messages = [
    {"role": "user", "content": "Hi! How are you doing today?"},
    {"role": "assistant", "content": "I'm doing well! How can I help you?"},
    {
        "role": "user",
        "content": (
            "Can you tell me what the temperate will be in Dallas, in fahrenheit?"
        ),
    },
]


def extract_reasoning_and_calls(chunks: list):
    reasoning_content = ""
    tool_call_idx = -1
    arguments = []
    function_names = []
    for chunk in chunks:
        if chunk.choices[0].delta.tool_calls:
            tool_call = chunk.choices[0].delta.tool_calls[0]
            if tool_call.index != tool_call_idx:
                tool_call_idx = chunk.choices[0].delta.tool_calls[0].index
                arguments.append("")
                function_names.append("")

            if tool_call.function:
                if tool_call.function.name:
                    function_names[tool_call_idx] = tool_call.function.name

                if tool_call.function.arguments:
                    arguments[tool_call_idx] += tool_call.function.arguments
        else:
            if hasattr(chunk.choices[0].delta, "reasoning_content"):
                reasoning_content += chunk.choices[0].delta.reasoning_content
    return reasoning_content, arguments, function_names


def main():
    """Run all reasoning with tools examples"""
    print("\n" + "🚀 GPT-OSS Reasoning with Tools Examples")
    print("=" * 60)
    
    # Create client using the standard configuration
    client = create_client()
    model = get_default_model()

    print("---------Full Generate With Automatic Function Calling-------------")
    tool_calls = client.chat.completions.create(
        messages=messages, model=model, tools=tools
    )
    
    # Check if tool calls are present
    if tool_calls.choices[0].message.tool_calls:
        print(f"reasoning_content: {tool_calls.choices[0].message.reasoning_content}")
        print(f"function name: {tool_calls.choices[0].message.tool_calls[0].function.name}")
        print(
            f"function arguments: "
            f"{tool_calls.choices[0].message.tool_calls[0].function.arguments}"
        )
    else:
        print(f"⚠️  No tool calls returned. Response content: {tool_calls.choices[0].message.content}")
        print(f"Model may not support tool calling or didn't detect the need for tools.")

    print("----------Stream Generate With Automatic Function Calling-----------")
    tool_calls_stream = client.chat.completions.create(
        messages=messages, model=model, tools=tools, stream=True
    )

    chunks = list(tool_calls_stream)

    reasoning_content, arguments, function_names = extract_reasoning_and_calls(chunks)

    if function_names and arguments:
        print(f"reasoning_content: {reasoning_content}")
        print(f"function name: {function_names[0]}")
        print(f"function arguments: {arguments[0]}")
    else:
        print(f"⚠️  No tool calls returned in stream.")
        print(f"reasoning_content: {reasoning_content}")

    print("----------Full Generate With Named Function Calling-----------------")
    tool_calls = client.chat.completions.create(
        messages=messages,
        model=model,
        tools=tools,
        tool_choice={"type": "function", "function": {"name": "get_current_weather"}},
    )

    if tool_calls.choices[0].message.tool_calls:
        tool_call = tool_calls.choices[0].message.tool_calls[0].function
        print(f"reasoning_content: {tool_calls.choices[0].message.reasoning_content}")
        print(f"function name: {tool_call.name}")
        print(f"function arguments: {tool_call.arguments}")
    else:
        print(f"⚠️  No tool calls returned. Response content: {tool_calls.choices[0].message.content}")
        print(f"Model may not support named function calling.")
    print("----------Stream Generate With Named Function Calling--------------")

    tool_calls_stream = client.chat.completions.create(
        messages=messages,
        model=model,
        tools=tools,
        tool_choice={"type": "function", "function": {"name": "get_current_weather"}},
        stream=True,
    )

    chunks = list(tool_calls_stream)

    reasoning_content, arguments, function_names = extract_reasoning_and_calls(chunks)
    
    if function_names and arguments:
        print(f"reasoning_content: {reasoning_content}")
        print(f"function name: {function_names[0]}")
        print(f"function arguments: {arguments[0]}")
    else:
        print(f"⚠️  No tool calls returned in stream.")
        print(f"reasoning_content: {reasoning_content}")
    
    print("\n" + "=" * 60)
    print("✅ All reasoning with tools examples completed!")


if __name__ == "__main__":
    main()