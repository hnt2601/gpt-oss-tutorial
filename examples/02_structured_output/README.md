# 02 - Structured Output

This module demonstrates how to get type-safe, structured responses from the GPT-OSS API.

## 📚 What You'll Learn

- Using JSON Schema for response validation
- Pydantic models for type-safe outputs
- The difference between `create()` and `parse()` methods
- Strict mode enforcement

## 🎯 Examples

### 1. JSON Schema (`json_schema.py`)

Use JSON Schema to define the expected response structure:

```python
response = client.responses.create(
    model="gpt-oss-20b",
    input="Alice and Bob are going to a science fair on Friday.",
    text={
        "format": {
            "type": "json_schema",
            "name": "calendar_event",
            "schema": {
                "type": "object",
                "properties": {
                    "event_name": {"type": "string"},
                    "date": {"type": "string"},
                    "participants": {"type": "array", "items": {"type": "string"}},
                },
                "required": ["event_name", "date", "participants"],
            },
            "strict": True,
        }
    }
)
```

### 2. Pydantic Models (`pydantic_parse.py`)

Use Pydantic for cleaner, type-safe code:

```python
from pydantic import BaseModel

class CalendarEvent(BaseModel):
    event_name: str
    date: str
    participants: list[str]

response = client.responses.parse(
    model="gpt-oss-20b",
    instructions="Extract the event information.",
    input="Alice and Bob are going to a science fair on Friday.",
    text_format=CalendarEvent,
)

# Type-safe access
event = response.output_parsed
print(event.event_name)  # IDE autocomplete works!
```

## 🚀 Running the Examples

```bash
# JSON Schema examples
python examples/02_structured_output/json_schema.py

# Pydantic examples
python examples/02_structured_output/pydantic_parse.py
```

## 📊 Comparison: JSON Schema vs Pydantic

| Feature | JSON Schema | Pydantic |
|---------|-------------|----------|
| Type Safety | ❌ Manual parsing | ✅ Automatic |
| IDE Support | ❌ Limited | ✅ Full autocomplete |
| Validation | ✅ Runtime | ✅ Runtime + Type hints |
| Code Style | More verbose | Cleaner, Pythonic |
| Flexibility | High | High |

**Recommendation**: Use Pydantic for Python projects, JSON Schema for language-agnostic schemas.

## 🔍 Strict Mode

Setting `"strict": True` enforces exact schema compliance:

```python
# With strict mode
{
    "strict": True,  # Model MUST follow schema exactly
    "additionalProperties": False  # No extra fields allowed
}
```

**Benefits:**
- Guaranteed output format
- No unexpected fields
- Fail-fast on schema violations

## 💡 Best Practices

### 1. Define Clear Schemas

```python
# Good: Clear, specific types
{
    "type": "object",
    "properties": {
        "price": {"type": "number"},
        "date": {"type": "string", "format": "date"},
    }
}

# Avoid: Too loose
{
    "type": "object",
    "properties": {
        "data": {"type": "string"}  # Too generic
    }
}
```

### 2. Use Optional Fields Wisely

```python
class Product(BaseModel):
    name: str  # Required
    price: float  # Required
    description: Optional[str] = None  # Optional
```

### 3. Validate Complex Structures

```python
class Meeting(BaseModel):
    title: str
    attendees: List[str]
    action_items: List[str]
    
    @validator('attendees')
    def validate_attendees(cls, v):
        if len(v) < 1:
            raise ValueError("At least one attendee required")
        return v
```

## 🎨 Use Cases

### Data Extraction

```python
# Extract structured data from unstructured text
response = client.responses.parse(
    input="Invoice #12345 for $299.99, due on 2025-01-30",
    text_format=Invoice
)
```

### Form Generation

```python
# Generate structured form data
response = client.responses.parse(
    input="Create a user registration form",
    text_format=FormSchema
)
```

### API Response Formatting

```python
# Ensure consistent API responses
response = client.responses.parse(
    input="Get user profile",
    text_format=UserProfile
)
```

## 🔗 Related Examples

- **01_basic**: Foundation concepts
- **03_tools**: Combining structured output with tool calls
- **06_advanced**: Complex schemas in RAG pipelines

## 📚 References

- [JSON Schema Specification](https://json-schema.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [OpenAI Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs)

