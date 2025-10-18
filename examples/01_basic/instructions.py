"""
Example: Basic Usage with System Instructions

This example demonstrates how to use system instructions to guide
the model's behavior and response format.

Key Concepts:
- Setting system instructions via the 'instructions' parameter
- Simple text input and output
- Response structure basics
"""

from pprint import pprint
from src.client import create_client, get_default_model


def basic_instructions_example():
    """
    Example: Using instructions parameter to guide model behavior
    
    The instructions parameter acts as a system prompt that persists
    across the conversation and guides the model's behavior.
    """
    client = create_client()
    
    print("=" * 60)
    print("Example: Basic Instructions")
    print("=" * 60)
    
    response = client.responses.create(
        model=get_default_model(),
        instructions="Finish the answer with QED.",
        input="What is 13 * 24?",
    )
    
    # Extract the output text from the response
    output_text = response.output[-1].content[0].text
    
    print("\nInput:", "What is 13 * 24?")
    print("\nInstructions:", "Finish the answer with QED.")
    print("\nOutput:", output_text)
    print("\n" + "=" * 60)
    
    return response


def simple_conversation_example():
    """
    Example: Simple conversation without special instructions
    """
    client = create_client()
    
    print("\n" + "=" * 60)
    print("Example: Simple Conversation")
    print("=" * 60)
    
    response = client.responses.create(
        model=get_default_model(),
        input="Explain quantum computing in simple terms.",
    )
    
    print("\nInput:", "Explain quantum computing in simple terms.")
    print("\nOutput:", response.output_text)
    print("\n" + "=" * 60)
    
    return response


def multi_turn_conversation_example():
    """
    Example: Multi-turn conversation using message history
    
    Demonstrates how to maintain context across multiple exchanges.
    """
    client = create_client()
    
    print("\n" + "=" * 60)
    print("Example: Multi-turn Conversation")
    print("=" * 60)
    
    # First turn
    context = [
        {"role": "user", "content": "What is Python?"}
    ]
    
    response_1 = client.responses.create(
        model=get_default_model(),
        input=context,
    )
    
    print("\nTurn 1:")
    print("User:", context[0]["content"])
    print("Assistant:", response_1.output_text)
    
    # Add response to context
    context.extend(response_1.output)
    
    # Second turn
    context.append({"role": "user", "content": "What are its main uses?"})
    
    response_2 = client.responses.create(
        model=get_default_model(),
        input=context,
    )
    
    print("\nTurn 2:")
    print("User:", context[-1]["content"])
    print("Assistant:", response_2.output_text)
    print("\n" + "=" * 60)
    
    return response_2


def main():
    """Run all basic examples"""
    print("\n" + "🚀 GPT-OSS Basic Usage Examples")
    print("=" * 60)
    
    # Example 1: Instructions
    basic_instructions_example()
    
    # Example 2: Simple conversation
    simple_conversation_example()
    
    # Example 3: Multi-turn
    multi_turn_conversation_example()
    
    print("\n✅ All basic examples completed!")


if __name__ == "__main__":
    main()

