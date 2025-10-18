"""
Example: Structured Output with JSON Schema

This example demonstrates how to get structured, type-safe responses
from the GPT-OSS API using JSON Schema validation.

Key Concepts:
- Defining JSON Schema for response format
- Strict mode enforcement
- Type-safe output extraction
"""

from pprint import pprint
from src.client import create_client, get_default_model


def calendar_event_extraction():
    """
    Example: Extract structured data from natural language
    
    Uses JSON Schema to ensure the response matches a specific format.
    The 'strict' mode enforces schema compliance.
    """
    client = create_client()
    
    print("=" * 60)
    print("Example: Calendar Event Extraction with JSON Schema")
    print("=" * 60)
    
    # Define the expected structure
    schema = {
        "type": "object",
        "properties": {
            "event_name": {"type": "string"},
            "date": {"type": "string"},
            "participants": {"type": "array", "items": {"type": "string"}},
        },
        "required": ["event_name", "date", "participants"],
        "additionalProperties": False,
    }
    
    response = client.responses.create(
        model=get_default_model(),
        input=[
            {"role": "system", "content": "Extract the event information."},
            {
                "role": "user",
                "content": "Alice and Bob are going to a science fair on Friday.",
            },
        ],
        text={
            "format": {
                "type": "json_schema",
                "name": "calendar_event",
                "schema": schema,
                "description": "A calendar event.",
                "strict": True,
            }
        }
    )
    
    print("\nInput:", "Alice and Bob are going to a science fair on Friday.")
    print("\nSchema:", schema)
    print("\nParsed Response:")
    pprint(response.model_dump(), indent=2)
    
    # Extract structured data
    output_content = response.output[-1].content[0]
    if hasattr(output_content, 'text'):
        import json
        structured_data = json.loads(output_content.text)
        print("\nExtracted Event:")
        print(f"  Event Name: {structured_data['event_name']}")
        print(f"  Date: {structured_data['date']}")
        print(f"  Participants: {', '.join(structured_data['participants'])}")
    
    print("\n" + "=" * 60)
    return response


def product_information_extraction():
    """
    Example: Extract product information from description
    """
    client = create_client()
    
    print("\n" + "=" * 60)
    print("Example: Product Information Extraction")
    print("=" * 60)
    
    schema = {
        "type": "object",
        "properties": {
            "product_name": {"type": "string"},
            "price": {"type": "number"},
            "currency": {"type": "string"},
            "features": {"type": "array", "items": {"type": "string"}},
            "in_stock": {"type": "boolean"}
        },
        "required": ["product_name", "price", "currency"],
        "additionalProperties": False,
    }
    
    response = client.responses.create(
        model=get_default_model(),
        input=[
            {"role": "system", "content": "Extract product information in structured format."},
            {
                "role": "user",
                "content": "The iPhone 15 Pro costs $999 USD and features a titanium design, A17 Pro chip, and USB-C port. Currently in stock."
            },
        ],
        text={
            "format": {
                "type": "json_schema",
                "name": "product_info",
                "schema": schema,
                "description": "Product information",
                "strict": True,
            }
        }
    )
    
    print("\nInput: Product description")
    print("\nExtracted structured data:")
    pprint(response.model_dump(), indent=2)
    print("\n" + "=" * 60)
    
    return response


def contact_information_extraction():
    """
    Example: Extract contact information from text
    """
    client = create_client()
    
    print("\n" + "=" * 60)
    print("Example: Contact Information Extraction")
    print("=" * 60)
    
    schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "email": {"type": "string"},
            "phone": {"type": "string"},
            "company": {"type": "string"},
            "role": {"type": "string"}
        },
        "required": ["name"],
        "additionalProperties": False,
    }
    
    response = client.responses.create(
        model=get_default_model(),
        input=[
            {"role": "system", "content": "Extract contact information."},
            {
                "role": "user",
                "content": "Hi, I'm John Smith from Acme Corp. You can reach me at john.smith@acme.com or +1-555-0123. I'm the Senior Software Engineer."
            },
        ],
        text={
            "format": {
                "type": "json_schema",
                "name": "contact_info",
                "schema": schema,
                "description": "Contact information",
                "strict": True,
            }
        }
    )
    
    print("\nInput: Text with contact details")
    print("\nExtracted contact info:")
    pprint(response.model_dump(), indent=2)
    print("\n" + "=" * 60)
    
    return response


def main():
    """Run all JSON Schema examples"""
    print("\n🚀 GPT-OSS Structured Output Examples (JSON Schema)")
    print("=" * 60)
    
    # Example 1: Calendar event
    calendar_event_extraction()
    
    # Example 2: Product info
    product_information_extraction()
    
    # Example 3: Contact info
    contact_information_extraction()
    
    print("\n✅ All structured output examples completed!")


if __name__ == "__main__":
    main()

