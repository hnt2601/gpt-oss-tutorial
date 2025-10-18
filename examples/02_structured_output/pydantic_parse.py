"""
Example: Structured Output with Pydantic Models

This example demonstrates how to use Pydantic models for type-safe
structured outputs. The `parse` method provides automatic validation
and parsing into Python objects.

Key Concepts:
- Using Pydantic BaseModel for schema definition
- The responses.parse() method
- Type-safe output with Python objects
- Automatic validation
"""

from pprint import pprint
from pydantic import BaseModel, Field
from typing import List, Optional
from src.client import create_client, get_default_model


class CalendarEvent(BaseModel):
    """Calendar event model"""
    event_name: str
    date: str
    participants: List[str]


class ProductInfo(BaseModel):
    """Product information model"""
    product_name: str
    price: float
    currency: str
    features: Optional[List[str]] = None
    in_stock: Optional[bool] = None


class ContactInfo(BaseModel):
    """Contact information model"""
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    role: Optional[str] = None


def calendar_event_with_pydantic():
    """
    Example: Extract calendar event using Pydantic model
    
    The responses.parse() method automatically converts the response
    to a Pydantic model instance, providing type safety and validation.
    """
    client = create_client()
    
    print("=" * 60)
    print("Example: Calendar Event with Pydantic Parse")
    print("=" * 60)
    
    response = client.responses.parse(
        model=get_default_model(),
        instructions="Extract the event information.",
        input="Alice and Bob are going to a science fair on Friday.",
        text_format=CalendarEvent,
    )
    
    print("\nInput:", "Alice and Bob are going to a science fair on Friday.")
    print("\nPydantic Model:", CalendarEvent.__name__)
    
    # The output is automatically parsed into a Pydantic model
    event = response.output_parsed
    
    print("\nParsed Event Object:")
    pprint(event.model_dump(), indent=2)
    
    # Type-safe access to fields
    print("\nAccessing fields:")
    print(f"  Event Name: {event.event_name}")
    print(f"  Date: {event.date}")
    print(f"  Participants: {', '.join(event.participants)}")
    
    print("\n" + "=" * 60)
    return response


def product_info_with_pydantic():
    """
    Example: Extract product information using Pydantic
    """
    client = create_client()
    
    print("\n" + "=" * 60)
    print("Example: Product Info with Pydantic")
    print("=" * 60)
    
    response = client.responses.parse(
        model=get_default_model(),
        instructions="Extract product information.",
        input="The MacBook Pro 16-inch costs $2499 USD and features M3 Max chip, 36GB RAM, and 1TB SSD. In stock now.",
        text_format=ProductInfo,
    )
    
    product = response.output_parsed
    
    print("\nParsed Product:")
    print(f"  Name: {product.product_name}")
    print(f"  Price: {product.price} {product.currency}")
    if product.features:
        print(f"  Features: {', '.join(product.features)}")
    print(f"  In Stock: {product.in_stock}")
    
    print("\n" + "=" * 60)
    return response


def contact_info_with_pydantic():
    """
    Example: Extract contact information using Pydantic
    """
    client = create_client()
    
    print("\n" + "=" * 60)
    print("Example: Contact Info with Pydantic")
    print("=" * 60)
    
    response = client.responses.parse(
        model=get_default_model(),
        instructions="Extract contact information from the text.",
        input="My name is Sarah Johnson. I work as a Product Manager at TechCorp. Email me at sarah.j@techcorp.com or call +1-555-9876.",
        text_format=ContactInfo,
    )
    
    contact = response.output_parsed
    
    print("\nParsed Contact:")
    print(f"  Name: {contact.name}")
    print(f"  Company: {contact.company}")
    print(f"  Role: {contact.role}")
    print(f"  Email: {contact.email}")
    print(f"  Phone: {contact.phone}")
    
    print("\n" + "=" * 60)
    return response


class MeetingNotes(BaseModel):
    """Meeting notes model with nested structure"""
    title: str
    date: str
    attendees: List[str]
    action_items: List[str]
    decisions: List[str]
    next_meeting: Optional[str] = None


def complex_structured_output():
    """
    Example: Complex nested structure with Pydantic
    """
    client = create_client()
    
    print("\n" + "=" * 60)
    print("Example: Complex Nested Structure")
    print("=" * 60)
    
    meeting_text = """
    Team Standup - January 15, 2025
    
    Attendees: Alice, Bob, Charlie
    
    Decisions made:
    - Use Python 3.11 for the new project
    - Deploy to AWS instead of GCP
    
    Action items:
    - Alice: Set up CI/CD pipeline by Friday
    - Bob: Write API documentation
    - Charlie: Review security guidelines
    
    Next meeting: January 22, 2025
    """
    
    response = client.responses.parse(
        model=get_default_model(),
        instructions="Extract meeting information in structured format.",
        input=meeting_text,
        text_format=MeetingNotes,
    )
    
    notes = response.output_parsed
    
    print("\nParsed Meeting Notes:")
    print(f"  Title: {notes.title}")
    print(f"  Date: {notes.date}")
    print(f"  Attendees: {', '.join(notes.attendees)}")
    print(f"\n  Decisions:")
    for decision in notes.decisions:
        print(f"    - {decision}")
    print(f"\n  Action Items:")
    for item in notes.action_items:
        print(f"    - {item}")
    print(f"\n  Next Meeting: {notes.next_meeting}")
    
    print("\n" + "=" * 60)
    return response


def main():
    """Run all Pydantic examples"""
    print("\n🚀 GPT-OSS Structured Output Examples (Pydantic)")
    print("=" * 60)
    
    # Example 1: Calendar event
    calendar_event_with_pydantic()
    
    # Example 2: Product info
    product_info_with_pydantic()
    
    # Example 3: Contact info
    contact_info_with_pydantic()
    
    # Example 4: Complex structure
    complex_structured_output()
    
    print("\n✅ All Pydantic examples completed!")


if __name__ == "__main__":
    main()

