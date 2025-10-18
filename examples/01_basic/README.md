# 01 - Basic Usage

This module covers the fundamental concepts of the GPT-OSS `/v1/responses` API.

## 📚 What You'll Learn

- How to make basic API calls
- Using system instructions to guide model behavior
- Understanding response structure
- Multi-turn conversations with context

## 🎯 Examples

### 1. System Instructions (`instructions.py`)

Demonstrates how to use the `instructions` parameter to control model behavior:

```python
response = client.responses.create(
    model="gpt-oss-20b",
    instructions="Finish the answer with QED.",
    input="What is 13 * 24?",
)
```

**Key Concepts:**
- The `instructions` parameter acts like a system prompt
- Instructions persist across the conversation
- Useful for setting tone, format, or constraints

## 🚀 Running the Examples

```bash
# Run all examples
python examples/01_basic/instructions.py
```

## 📖 API Parameters

### Basic Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `model` | string | Model identifier (e.g., `gpt-oss-20b`) |
| `input` | string or array | User message(s) |
| `instructions` | string | System-level instructions (optional) |

### Input Formats

**Simple String:**
```python
input="Hello, world!"
```

**Message Array:**
```python
input=[
    {"role": "user", "content": "What is AI?"}
]
```

**Multi-turn with Context:**
```python
input=[
    {"role": "user", "content": "What is Python?"},
    {"role": "assistant", "content": "Python is a programming language..."},
    {"role": "user", "content": "What are its uses?"}
]
```

## 🔍 Response Structure

The API returns a response object with:

```python
response.id                    # Unique response ID
response.model                 # Model used
response.output                # Array of response items
response.output_text          # Convenience: extracted text
response.usage                # Token usage statistics
```

### Output Array

The `output` array contains response items:

```python
# Text response
{
    "type": "response_text",
    "content": [
        {"type": "text", "text": "The answer is..."}
    ]
}
```

## 💡 Best Practices

1. **Clear Instructions**: Be specific about expected format/behavior
2. **Context Management**: Include relevant history for multi-turn
3. **Error Handling**: Always handle potential API errors
4. **Token Awareness**: Monitor usage to optimize costs

## 🔗 Related Examples

- **02_structured_output**: For formatted/typed responses
- **05_stateful**: For conversation state management

## 📚 References

- [OpenAI Python SDK Documentation](https://github.com/openai/openai-python)
- [GPT-OSS API Reference](https://docs.fptcloud.com)

