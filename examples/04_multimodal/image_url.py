"""
Example: Multimodal - Image Input via URL

This example demonstrates how to process images alongside text
using publicly accessible image URLs.

Key Concepts:
- Image input via URL
- Multi-modal reasoning (vision + text)
- Combining images with tool calls
"""

import json
from pprint import pprint
from src.client import create_client, get_default_model


def simple_image_analysis():
    """
    Example: Basic image analysis
    
    Analyze an image from a URL and get a text description.
    """
    client = create_client()
    
    print("=" * 60)
    print("Example: Simple Image Analysis")
    print("=" * 60)
    
    image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/Cat_August_2010-4.jpg/2880px-Cat_August_2010-4.jpg"
    
    response = client.responses.create(
        model=get_default_model(),
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": "What's in this image? Describe it in detail."},
                    {"type": "input_image", "image_url": image_url}
                ]
            }
        ],
    )
    
    print(f"\nImage URL: {image_url}")
    print("\n💬 Analysis:")
    print(response.output_text)
    
    print("\n" + "=" * 60)
    return response


def image_with_web_search():
    """
    Example: Image analysis combined with web search
    
    Demonstrates how to analyze an image and then search for
    related information on the web.
    """
    client = create_client()
    
    print("\n" + "=" * 60)
    print("Example: Image Analysis + Web Search")
    print("=" * 60)
    
    image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/Cat_August_2010-4.jpg/2880px-Cat_August_2010-4.jpg"
    
    response = client.responses.create(
        model=get_default_model(),
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text", 
                        "text": "Identify the main subject in this image, then search for recent news about this topic. Summarize the findings."
                    },
                    {"type": "input_image", "image_url": image_url}
                ]
            }
        ],
        tools=[
            {"type": "web_search"}
        ]
    )
    
    print(f"\nImage URL: {image_url}")
    print("\n💬 Analysis + Search Results:")
    
    # Print response structure
    print("\nResponse structure:")
    for i, item in enumerate(response.output):
        print(f"  [{i}] {item.type}")
    
    # Print final text
    print("\n" + response.output_text)
    
    print("\n" + "=" * 60)
    return response


def multiple_images_analysis():
    """
    Example: Analyze multiple images
    
    Compare or analyze multiple images in a single request.
    """
    client = create_client()
    
    print("\n" + "=" * 60)
    print("Example: Multiple Images Analysis")
    print("=" * 60)
    
    images = [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Cat03.jpg/1200px-Cat03.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/Cat_November_2010-1a.jpg/1200px-Cat_November_2010-1a.jpg"
    ]
    
    content = [
        {"type": "input_text", "text": "Compare these two images. What are the similarities and differences?"}
    ]
    
    for img_url in images:
        content.append({"type": "input_image", "image_url": img_url})
    
    response = client.responses.create(
        model=get_default_model(),
        input=[{"role": "user", "content": content}],
    )
    
    print(f"\nNumber of images: {len(images)}")
    print("\n💬 Comparison:")
    print(response.output_text)
    
    print("\n" + "=" * 60)
    return response


def image_ocr_extraction():
    """
    Example: Extract text from image (OCR)
    
    Use the model's vision capabilities to read text from images.
    """
    client = create_client()
    
    print("\n" + "=" * 60)
    print("Example: Text Extraction from Image (OCR)")
    print("=" * 60)
    
    # Image with text/diagram
    image_url = "https://upload.wikimedia.org/wikipedia/commons/0/0b/RGBA_comp.png"
    
    response = client.responses.create(
        model=get_default_model(),
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": "Extract and list all text visible in this image."},
                    {"type": "input_image", "image_url": image_url}
                ]
            }
        ],
    )
    
    print(f"\nImage URL: {image_url}")
    print("\n💬 Extracted Text:")
    print(response.output_text)
    
    print("\n" + "=" * 60)
    return response


def image_based_qa():
    """
    Example: Question answering based on image
    
    Ask specific questions about image content.
    """
    client = create_client()
    
    print("\n" + "=" * 60)
    print("Example: Image-based Q&A")
    print("=" * 60)
    
    image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/Cat_August_2010-4.jpg/2880px-Cat_August_2010-4.jpg"
    
    questions = [
        "What color is the main subject?",
        "What is the background like?",
        "What is the subject doing?"
    ]
    
    print(f"\nImage URL: {image_url}\n")
    
    for question in questions:
        response = client.responses.create(
            model=get_default_model(),
            input=[
                {
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": question},
                        {"type": "input_image", "image_url": image_url}
                    ]
                }
            ],
        )
        
        print(f"Q: {question}")
        print(f"A: {response.output_text}\n")
    
    print("=" * 60)
    return response


def main():
    """Run all image URL examples"""
    print("\n🚀 GPT-OSS Multimodal Examples (Image URL)")
    print("=" * 60)
    
    # Example 1: Simple analysis
    simple_image_analysis()
    
    # Example 2: With web search
    image_with_web_search()
    
    # Example 3: Multiple images
    multiple_images_analysis()
    
    # Example 4: OCR
    image_ocr_extraction()
    
    # Example 5: Q&A
    image_based_qa()
    
    print("\n✅ All image URL examples completed!")


if __name__ == "__main__":
    main()

