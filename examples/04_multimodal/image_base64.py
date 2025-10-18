"""
Example: Multimodal - Image Input via Base64

This example demonstrates how to process images encoded as base64 strings.
This is useful for private images, local files, or when URLs aren't available.

Key Concepts:
- Base64 encoding for images
- Processing local image files
- Image format conversion
"""

import base64
import requests
from io import BytesIO
from PIL import Image
from pprint import pprint
from src.client import create_client, get_default_model


def load_image_from_url_to_base64(url: str) -> str:
    """
    Download an image from URL and convert to base64
    
    Args:
        url: Image URL
        
    Returns:
        Base64 encoded string with data URI prefix
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    
    # Open and convert image
    img = Image.open(BytesIO(response.content))
    
    # Convert to RGB if necessary
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    # Convert to base64
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    base64_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
    
    return f"data:image/jpeg;base64,{base64_image}"


def load_local_image_to_base64(file_path: str) -> str:
    """
    Load a local image file and convert to base64
    
    Args:
        file_path: Path to local image file
        
    Returns:
        Base64 encoded string with data URI prefix
    """
    with Image.open(file_path) as img:
        # Convert to RGB if necessary
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Convert to base64
        buffered = BytesIO()
        img.save(buffered, format="JPEG")
        base64_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
        
        return f"data:image/jpeg;base64,{base64_image}"


def simple_base64_image():
    """
    Example: Analyze image from base64 encoding
    
    Demonstrates basic image analysis using base64 encoded image.
    """
    client = create_client()
    
    print("=" * 60)
    print("Example: Base64 Image Analysis")
    print("=" * 60)
    
    # Download and encode image
    raw_image_url = "https://upload.wikimedia.org/wikipedia/commons/0/0b/RGBA_comp.png"
    print(f"\nLoading image from: {raw_image_url}")
    print("Converting to base64...")
    
    base64_image = load_image_from_url_to_base64(raw_image_url)
    
    print(f"Base64 length: {len(base64_image)} characters")
    print(f"Preview: {base64_image[:80]}...")
    
    # Use base64 image in API call
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "input_image",
                    "image_url": base64_image,
                    "detail": "auto",
                },
                {"type": "input_text", "text": "What's in this image? Describe the visual elements."},
            ],
        }
    ]
    
    response = client.responses.create(
        model=get_default_model(),
        input=messages,
    )
    
    print("\n💬 Analysis:")
    print(response.output_text)
    
    print("\n" + "=" * 60)
    return response


def base64_image_with_detail_levels():
    """
    Example: Using different detail levels for image processing
    
    The 'detail' parameter controls how the model processes the image:
    - "auto": Automatic selection
    - "low": Faster, lower resolution
    - "high": Slower, higher resolution
    """
    client = create_client()
    
    print("\n" + "=" * 60)
    print("Example: Base64 with Detail Levels")
    print("=" * 60)
    
    image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/Cat_August_2010-4.jpg/1200px-Cat_August_2010-4.jpg"
    base64_image = load_image_from_url_to_base64(image_url)
    
    detail_levels = ["low", "auto", "high"]
    
    for detail in detail_levels:
        print(f"\n--- Detail Level: {detail} ---")
        
        response = client.responses.create(
            model=get_default_model(),
            input=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_image",
                            "image_url": base64_image,
                            "detail": detail,
                        },
                        {"type": "input_text", "text": "Describe this image briefly."},
                    ],
                }
            ],
        )
        
        print(f"Response: {response.output_text[:200]}...")
        if hasattr(response, 'usage'):
            print(f"Tokens used: {response.usage.total_tokens if hasattr(response.usage, 'total_tokens') else 'N/A'}")
    
    print("\n" + "=" * 60)
    return response


def multiple_base64_images():
    """
    Example: Process multiple base64 encoded images
    
    Useful for comparing multiple local images or private images.
    """
    client = create_client()
    
    print("\n" + "=" * 60)
    print("Example: Multiple Base64 Images")
    print("=" * 60)
    
    image_urls = [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Cat03.jpg/400px-Cat03.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/Cat_November_2010-1a.jpg/400px-Cat_November_2010-1a.jpg"
    ]
    
    print(f"\nLoading {len(image_urls)} images...")
    
    content = [
        {"type": "input_text", "text": "Compare these images and identify key differences."}
    ]
    
    for i, url in enumerate(image_urls):
        print(f"  {i+1}. Converting image to base64...")
        base64_img = load_image_from_url_to_base64(url)
        content.append({
            "type": "input_image",
            "image_url": base64_img,
            "detail": "auto"
        })
    
    response = client.responses.create(
        model=get_default_model(),
        input=[{"role": "user", "content": content}],
    )
    
    print("\n💬 Comparison:")
    print(response.output_text)
    
    print("\n" + "=" * 60)
    return response


def base64_with_structured_output():
    """
    Example: Combine base64 image with structured output
    
    Extract structured information from images.
    """
    client = create_client()
    
    print("\n" + "=" * 60)
    print("Example: Base64 Image + Structured Output")
    print("=" * 60)
    
    image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/Cat_August_2010-4.jpg/800px-Cat_August_2010-4.jpg"
    base64_image = load_image_from_url_to_base64(image_url)
    
    schema = {
        "type": "object",
        "properties": {
            "main_subject": {"type": "string"},
            "colors": {"type": "array", "items": {"type": "string"}},
            "setting": {"type": "string"},
            "mood": {"type": "string"},
        },
        "required": ["main_subject", "colors", "setting"],
    }
    
    response = client.responses.create(
        model=get_default_model(),
        input=[
            {"role": "system", "content": "Analyze the image and extract structured information."},
            {
                "role": "user",
                "content": [
                    {"type": "input_image", "image_url": base64_image},
                    {"type": "input_text", "text": "Extract key visual elements"},
                ],
            }
        ],
        text={
            "format": {
                "type": "json_schema",
                "name": "image_analysis",
                "schema": schema,
                "strict": True,
            }
        }
    )
    
    print("\n💬 Structured Analysis:")
    pprint(response.model_dump(), indent=2)
    
    print("\n" + "=" * 60)
    return response


def main():
    """Run all base64 image examples"""
    print("\n🚀 GPT-OSS Multimodal Examples (Base64 Images)")
    print("=" * 60)
    
    # Example 1: Simple base64
    simple_base64_image()
    
    # Example 2: Detail levels
    base64_image_with_detail_levels()
    
    # Example 3: Multiple images
    multiple_base64_images()
    
    # Example 4: Structured output
    base64_with_structured_output()
    
    print("\n✅ All base64 image examples completed!")
    print("\nℹ️  Note: For local images, use load_local_image_to_base64(filepath)")


if __name__ == "__main__":
    main()

