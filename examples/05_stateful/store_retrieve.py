"""
Example: Stateful Conversations

This example demonstrates how to store and retrieve conversation
state using the GPT-OSS API's built-in state management.

Key Concepts:
- Storing responses with store=True
- Retrieving past conversations
- Session management
- Conversation continuity
"""

from pprint import pprint
from src.client import create_client, get_default_model


def simple_store_retrieve():
    """
    Example: Basic store and retrieve
    
    Store a response and retrieve it later by ID.
    """
    client = create_client()
    
    print("=" * 60)
    print("Example: Simple Store and Retrieve")
    print("=" * 60)
    
    # Create and store a response
    print("\n📝 Creating and storing response...")
    
    response = client.responses.create(
        model=get_default_model(),
        input="Tell me a joke about programming",
        store=True  # Enable storage
    )
    
    response_id = response.id
    print(f"\n✅ Response stored with ID: {response_id}")
    print(f"\nOriginal response: {response.output_text}")
    
    # Retrieve the stored response
    print(f"\n📥 Retrieving response {response_id}...")
    
    fetched_response = client.responses.retrieve(response_id=response_id)
    
    print(f"\n✅ Retrieved successfully!")
    print(f"Retrieved response: {fetched_response.output_text}")
    
    print("\n" + "=" * 60)
    return fetched_response


def stateful_conversation():
    """
    Example: Multi-turn stateful conversation
    
    Store multiple turns and maintain conversation state.
    """
    client = create_client()
    
    print("\n" + "=" * 60)
    print("Example: Stateful Multi-turn Conversation")
    print("=" * 60)
    
    conversation_ids = []
    
    # Turn 1
    print("\n--- Turn 1 ---")
    response_1 = client.responses.create(
        model=get_default_model(),
        input="My name is Alice. What's your name?",
        store=True
    )
    conversation_ids.append(response_1.id)
    print(f"User: My name is Alice. What's your name?")
    print(f"Assistant: {response_1.output_text}")
    
    # Turn 2 - Reference previous context
    print("\n--- Turn 2 ---")
    context = [
        {"role": "user", "content": "My name is Alice. What's your name?"},
        *response_1.output,
        {"role": "user", "content": "What's my name?"}
    ]
    
    response_2 = client.responses.create(
        model=get_default_model(),
        input=context,
        store=True
    )
    conversation_ids.append(response_2.id)
    print(f"User: What's my name?")
    print(f"Assistant: {response_2.output_text}")
    
    # Turn 3
    print("\n--- Turn 3 ---")
    context.extend(response_2.output)
    context.append({"role": "user", "content": "Can you remind me what we talked about?"})
    
    response_3 = client.responses.create(
        model=get_default_model(),
        input=context,
        store=True
    )
    conversation_ids.append(response_3.id)
    print(f"User: Can you remind me what we talked about?")
    print(f"Assistant: {response_3.output_text}")
    
    print(f"\n💾 Stored {len(conversation_ids)} conversation turns")
    print(f"Response IDs: {conversation_ids}")
    
    # Retrieve any turn
    print(f"\n📥 Retrieving Turn 1...")
    turn_1 = client.responses.retrieve(response_id=conversation_ids[0])
    print(f"Turn 1: {turn_1.output_text}")
    
    print("\n" + "=" * 60)
    return conversation_ids


def conversation_with_metadata():
    """
    Example: Store conversations with metadata
    
    Demonstrates how to organize stored conversations.
    """
    client = create_client()
    
    print("\n" + "=" * 60)
    print("Example: Conversations with Metadata")
    print("=" * 60)
    
    # Simulate multiple conversation sessions
    sessions = []
    
    # Session 1: Technical help
    print("\n📋 Session 1: Technical Help")
    response = client.responses.create(
        model=get_default_model(),
        input="How do I use asyncio in Python?",
        store=True
    )
    sessions.append({
        "id": response.id,
        "topic": "Python asyncio",
        "category": "technical_help",
        "summary": response.output_text[:100] + "..."
    })
    print(f"Stored: {response.id}")
    
    # Session 2: Creative writing
    print("\n📋 Session 2: Creative Writing")
    response = client.responses.create(
        model=get_default_model(),
        input="Write a short poem about autumn",
        store=True
    )
    sessions.append({
        "id": response.id,
        "topic": "Autumn poem",
        "category": "creative",
        "summary": response.output_text[:100] + "..."
    })
    print(f"Stored: {response.id}")
    
    # Session 3: Data analysis
    print("\n📋 Session 3: Data Analysis")
    response = client.responses.create(
        model=get_default_model(),
        input="Explain principal component analysis",
        store=True
    )
    sessions.append({
        "id": response.id,
        "topic": "PCA explanation",
        "category": "data_science",
        "summary": response.output_text[:100] + "..."
    })
    print(f"Stored: {response.id}")
    
    # Display session catalog
    print("\n📚 Session Catalog:")
    for i, session in enumerate(sessions, 1):
        print(f"\n  Session {i}:")
        print(f"    ID: {session['id']}")
        print(f"    Topic: {session['topic']}")
        print(f"    Category: {session['category']}")
        print(f"    Preview: {session['summary']}")
    
    # Retrieve specific session
    print(f"\n📥 Retrieving Session 2 (Creative Writing)...")
    retrieved = client.responses.retrieve(response_id=sessions[1]['id'])
    print(f"\n{retrieved.output_text}")
    
    print("\n" + "=" * 60)
    return sessions


def conversation_branching():
    """
    Example: Branching conversations
    
    Demonstrates how to create conversation branches from stored state.
    """
    client = create_client()
    
    print("\n" + "=" * 60)
    print("Example: Conversation Branching")
    print("=" * 60)
    
    # Base conversation
    print("\n🌳 Base Conversation:")
    base_response = client.responses.create(
        model=get_default_model(),
        input="I'm interested in learning about machine learning",
        store=True
    )
    base_id = base_response.id
    print(f"User: I'm interested in learning about machine learning")
    print(f"Assistant: {base_response.output_text[:150]}...")
    print(f"Stored as: {base_id}")
    
    # Branch 1: Beginner path
    print("\n🌿 Branch 1: Beginner Path")
    context_beginner = [
        {"role": "user", "content": "I'm interested in learning about machine learning"},
        *base_response.output,
        {"role": "user", "content": "I'm a complete beginner. Where should I start?"}
    ]
    
    branch_1 = client.responses.create(
        model=get_default_model(),
        input=context_beginner,
        store=True
    )
    print(f"Branched to: {branch_1.id}")
    print(f"Response: {branch_1.output_text[:150]}...")
    
    # Branch 2: Advanced path
    print("\n🌿 Branch 2: Advanced Path")
    context_advanced = [
        {"role": "user", "content": "I'm interested in learning about machine learning"},
        *base_response.output,
        {"role": "user", "content": "I have a PhD in statistics. What's the latest in deep learning?"}
    ]
    
    branch_2 = client.responses.create(
        model=get_default_model(),
        input=context_advanced,
        store=True
    )
    print(f"Branched to: {branch_2.id}")
    print(f"Response: {branch_2.output_text[:150]}...")
    
    print("\n🌳 Conversation Tree:")
    print(f"  Base: {base_id}")
    print(f"  ├─ Branch 1 (Beginner): {branch_1.id}")
    print(f"  └─ Branch 2 (Advanced): {branch_2.id}")
    
    print("\n" + "=" * 60)
    return (base_id, branch_1.id, branch_2.id)


def main():
    """Run all stateful examples"""
    print("\n🚀 GPT-OSS Stateful Conversation Examples")
    print("=" * 60)
    
    # Example 1: Simple store/retrieve
    simple_store_retrieve()
    
    # Example 2: Multi-turn conversation
    stateful_conversation()
    
    # Example 3: Metadata tracking
    conversation_with_metadata()
    
    # Example 4: Branching
    conversation_branching()
    
    print("\n✅ All stateful examples completed!")
    print("\n💡 Tip: Use store=True to enable conversation state persistence")


if __name__ == "__main__":
    main()

