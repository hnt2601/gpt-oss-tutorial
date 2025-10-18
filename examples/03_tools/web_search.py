"""
Example: Web Search Tool

This example demonstrates how to use the built-in web search tool
to augment the model's knowledge with real-time information.

Key Concepts:
- Built-in web_search tool
- Real-time information retrieval
- Automatic source citation
"""

from pprint import pprint
from src.client import create_client, get_default_model


def simple_web_search():
    """
    Example: Basic web search usage
    
    The web_search tool allows the model to search the internet
    for current information and cite sources.
    """
    client = create_client()
    
    print("=" * 60)
    print("Example: Simple Web Search")
    print("=" * 60)
    
    response = client.responses.create(
        model=get_default_model(),
        input="What's the latest news about AI in 2025?",
        tools=[
            {
                "type": "web_search"
            }
        ]
    )
    
    print("\nQuery:", "What's the latest news about AI in 2025?")
    print("\n💬 Response:")
    pprint(response.model_dump(), indent=2)
    
    print("\n" + "=" * 60)
    return response


def web_search_with_location():
    """
    Example: Web search with location context
    
    Demonstrates how to provide location information for
    more relevant search results.
    """
    client = create_client()
    
    print("\n" + "=" * 60)
    print("Example: Web Search with Location Context")
    print("=" * 60)
    
    response = client.responses.create(
        model=get_default_model(),
        input="What are the top tech companies hiring right now?",
        tools=[
            {
                "type": "web_search_preview",
                "user_location": {
                    "type": "approximate",
                    "country": "US",
                    "region": "California",
                    "city": "SF"
                },
                "search_context_size": "medium"
            }
        ]
    )
    
    print("\nQuery: Tech companies hiring (Location: SF, CA)")
    print("\n💬 Response:")
    print(response.output_text)
    
    print("\n" + "=" * 60)
    return response


def web_search_for_verification():
    """
    Example: Using web search to verify information
    
    Shows how the model can fact-check using web search
    """
    client = create_client()
    
    print("\n" + "=" * 60)
    print("Example: Web Search for Fact Verification")
    print("=" * 60)
    
    response = client.responses.create(
        model=get_default_model(),
        input="Verify: Did SpaceX successfully launch Starship in 2024? Provide sources.",
        tools=[
            {
                "type": "web_search"
            }
        ]
    )
    
    print("\nQuery: Verify SpaceX Starship launch")
    print("\n💬 Response with Sources:")
    print(response.output_text)
    
    print("\n" + "=" * 60)
    return response


def web_search_comparative():
    """
    Example: Comparative analysis using web search
    
    Model searches and compares multiple topics
    """
    client = create_client()
    
    print("\n" + "=" * 60)
    print("Example: Comparative Analysis with Web Search")
    print("=" * 60)
    
    response = client.responses.create(
        model=get_default_model(),
        input="Compare the performance of NVIDIA and AMD GPUs released in 2024. Include benchmarks if available.",
        tools=[
            {
                "type": "web_search"
            }
        ]
    )
    
    print("\nQuery: Compare NVIDIA vs AMD GPUs (2024)")
    print("\n💬 Comparative Analysis:")
    print(response.output_text)
    
    print("\n" + "=" * 60)
    return response


def main():
    """Run all web search examples"""
    print("\n🚀 GPT-OSS Web Search Examples")
    print("=" * 60)
    
    # Example 1: Simple search
    simple_web_search()
    
    # Example 2: Search with location
    web_search_with_location()
    
    # Example 3: Verification
    web_search_for_verification()
    
    # Example 4: Comparative
    web_search_comparative()
    
    print("\n✅ All web search examples completed!")


if __name__ == "__main__":
    main()

