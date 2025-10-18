# 04 - Multimodal (Vision)

This module demonstrates how to work with images alongside text using GPT-OSS's multimodal capabilities.

## 📚 What You'll Learn

- Image input via URL
- Base64 encoded images
- Multi-modal reasoning (vision + text)
- Combining images with tools
- Detail level control

## 🎯 Examples

### 1. Image via URL (`image_url.py`)

Process images from public URLs:

```python
response = client.responses.create(
    model="gpt-oss-20b",
    input=[{
        "role": "user",
        "content": [
            {"type": "input_text", "text": "What's in this image?"},
            {"type": "input_image", "image_url": "https://example.com/image.jpg"}
        ]
    }]
)
```

### 2. Base64 Encoded Images (`image_base64.py`)

Process local or private images:

```python
# Convert image to base64
base64_image = f"data:image/jpeg;base64,{base64_string}"

response = client.responses.create(
    model="gpt-oss-20b",
    input=[{
        "role": "user",
        "content": [
            {
                "type": "input_image",
                "image_url": base64_image,
                "detail": "auto"
            },
            {"type": "input_text", "text": "Analyze this image"}
        ]
    }]
)
```

## 🚀 Running the Examples

```bash
# Image URL examples
python examples/04_multimodal/image_url.py

# Base64 image examples
python examples/04_multimodal/image_base64.py
```

## 🖼️ Image Input Formats

### URL Format

```python
{
    "type": "input_image",
    "image_url": "https://example.com/image.jpg"
}
```

**Requirements:**
- Publicly accessible URL
- Supported formats: JPEG, PNG, GIF, WebP
- Max size: ~20MB (model dependent)

### Base64 Format

```python
{
    "type": "input_image",
    "image_url": "data:image/jpeg;base64,/9j/4AAQSkZJRg...",
    "detail": "auto"  # Optional: "low", "auto", "high"
}
```

## 🎚️ Detail Levels

Control image processing resolution:

| Level | Speed | Quality | Use Case |
|-------|-------|---------|----------|
| `low` | Fast | Basic | Quick analysis, thumbnails |
| `auto` | Balanced | Good | Default for most cases |
| `high` | Slow | Best | Detailed analysis, OCR |

```python
{
    "type": "input_image",
    "image_url": url,
    "detail": "high"  # More detail, more tokens
}
```

## 🔗 Combining with Other Features

### Images + Web Search

```python
response = client.responses.create(
    input=[{
        "role": "user",
        "content": [
            {"type": "input_text", "text": "Identify this and search for news"},
            {"type": "input_image", "image_url": url}
        ]
    }],
    tools=[{"type": "web_search"}]
)
```

### Images + Structured Output

```python
schema = {
    "type": "object",
    "properties": {
        "objects": {"type": "array", "items": {"type": "string"}},
        "colors": {"type": "array", "items": {"type": "string"}},
        "description": {"type": "string"}
    }
}

response = client.responses.create(
    input=[{"role": "user", "content": [image_input, text_input]}],
    text={"format": {"type": "json_schema", "schema": schema}}
)
```

### Multiple Images

```python
content = [
    {"type": "input_text", "text": "Compare these images"},
    {"type": "input_image", "image_url": url1},
    {"type": "input_image", "image_url": url2},
    {"type": "input_image", "image_url": url3}
]
```

## 💡 Best Practices

### 1. Image Quality

```python
# Good: Appropriate resolution
image = resize_image(original, max_width=2048)

# Avoid: Unnecessarily large images
image = original  # 8000x6000px - wastes tokens
```

### 2. Format Selection

**Use URL when:**
- Image is already hosted online
- Image is public
- Want to minimize request size

**Use Base64 when:**
- Image is local/private
- Need guaranteed delivery
- Processing generated images

### 3. Detail Level Selection

```python
# OCR or fine details
{"detail": "high"}

# Object detection
{"detail": "auto"}

# Quick classification
{"detail": "low"}
```

### 4. Error Handling

```python
try:
    base64_img = load_image_to_base64(path)
except FileNotFoundError:
    print("Image not found")
except Exception as e:
    print(f"Error processing image: {e}")
```

## 🎨 Use Cases

### Document Analysis

```python
# Extract text from documents
response = client.responses.create(
    input=[{
        "role": "user",
        "content": [
            {"type": "input_text", "text": "Extract all text from this document"},
            {"type": "input_image", "image_url": document_url}
        ]
    }]
)
```

### Product Cataloging

```python
# Structured product info from images
schema = {
    "properties": {
        "product_name": {"type": "string"},
        "category": {"type": "string"},
        "features": {"type": "array", "items": {"type": "string"}}
    }
}

response = client.responses.create(
    input=[product_image, "Extract product details"],
    text={"format": {"type": "json_schema", "schema": schema}}
)
```

### Medical Imaging (Healthcare)

```python
# Describe medical images (not a replacement for professional diagnosis)
response = client.responses.create(
    input=[
        {"type": "input_text", "text": "Describe visible features in this scan"},
        {"type": "input_image", "image_url": scan_url, "detail": "high"}
    ]
)
```

### Visual Q&A

```python
# Answer questions about images
questions = ["What color is the car?", "How many people?", "What's the weather?"]

for q in questions:
    response = client.responses.create(
        input=[
            {"role": "user",
             "content": [
                 {"type": "input_text", "text": q},
                 {"type": "input_image", "image_url": image_url}
             ]}
        ]
    )
    print(f"Q: {q}\nA: {response.output_text}\n")
```

## 🔧 Helper Functions

### Load Local Image

```python
import base64
from PIL import Image
from io import BytesIO

def load_local_image(path: str) -> str:
    with Image.open(path) as img:
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        buffer = BytesIO()
        img.save(buffer, format="JPEG")
        b64 = base64.b64encode(buffer.getvalue()).decode()
        
        return f"data:image/jpeg;base64,{b64}"
```

### Download and Encode

```python
import requests

def url_to_base64(url: str) -> str:
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    buffer = BytesIO()
    img.save(buffer, format="JPEG")
    b64 = base64.b64encode(buffer.getvalue()).decode()
    
    return f"data:image/jpeg;base64,{b64}"
```

## ⚠️ Limitations

- **Image Size**: Very large images may hit token limits
- **Detail vs Cost**: Higher detail = more tokens = higher cost
- **Format Support**: Stick to JPEG, PNG, WebP for best results
- **Rate Limits**: Images count toward API rate limits

## 🔗 Related Examples

- **03_tools**: Combine vision with function calling
- **02_structured_output**: Extract structured data from images
- **06_advanced**: Vision in RAG pipelines

## 📚 References

- [OpenAI Vision Guide](https://platform.openai.com/docs/guides/vision)
- [Pillow Documentation](https://pillow.readthedocs.io/)
- [Base64 Encoding](https://docs.python.org/3/library/base64.html)

