# GPT-OSS Tutorial Research

Comprehensive tutorial and research repository for GPT-OSS `/v1/responses` API features.

## 📚 Overview

This repository provides structured examples and in-depth exploration of GPT-OSS API capabilities, designed for research and production use. Each module is self-contained with detailed documentation and runnable examples.

## 🎯 Features Covered

### 1. Basic Usage
- System instructions
- Simple text responses
- Stateful conversations (store & retrieve)

### 2. Structured Output
- JSON Schema formatting
- Pydantic model parsing
- Type-safe responses

### 3. Tool Integration
- Function calling
- Web search
- Model Context Protocol (MCP)
- Parallel tool calls

### 4. Multimodal
- Image input via URL
- Base64 encoded images
- Multi-modal reasoning

### 5. Advanced Features
- RAG (Retrieval-Augmented Generation)
- Vector database integration (Pinecone)
- Reasoning summaries
- Tool routing

### 6. Voice Agent
- Speech-to-text with Whisper API
- Audio transcription and processing
- OpenAI Agents SDK integration
- Vietnamese-to-English translation
- Async audio processing

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- GPT-OSS API access
- API key from FPT Cloud

### Installation

#### Quick Start (Recommended)

```bash
cd gpt-oss-tutorial

# Run the quick start script (macOS/Linux)
./quick_start.sh

# Then activate venv and verify setup
source .venv/bin/activate
python check_setup.py
```

#### Manual Installation

```bash
# Clone the repository
cd gpt-oss-tutorial

# Create virtual environment
curl -LsSf https://astral.sh/uv/install.sh | sh
uv venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install the package with standard dependencies (examples 01-07)
uv pip install -e ".[standard]"

# Or install with development dependencies
uv pip install -e ".[standard,dev]"

# For voice agent (example 08) - requires separate venv due to OpenAI SDK version conflict
# Create a separate environment:
python -m venv venv-voice
source venv-voice/bin/activate
pip install -e ".[voice]"

# Copy environment template
cp .env.example .env
# Edit .env and add your API key
```

See [INSTALL.md](INSTALL.md) for detailed installation instructions and troubleshooting.

### Configuration

Create a `.env` file with your credentials:

```env
API_KEY=your_api_key_here
BASE_URL=https://mkp-api.fptcloud.com
MODEL_NAME=gpt-oss-20b
PINECONE_API_KEY=your_api_key_here
```

## 📖 Usage

### Running Examples

Each module has its own directory with runnable examples:

```bash
# Basic usage
python examples/01_basic/instructions.py

# Structured output
python examples/02_structured_output/json_schema.py

# Function calling
python examples/03_tools/function_calling.py

# Multimodal
python examples/04_multimodal/image_url.py

# RAG
python examples/06_advanced/rag_pinecone.py

# Voice Agent (requires separate venv with voice dependencies)
python examples/08_voice_agent/voice_agent.py
```

### Using the Shared Client

```python
from src.client import create_client

# Create client with default config
client = create_client()

# Use the client
response = client.responses.create(
    model="gpt-oss-20b",
    input="Hello, GPT-OSS!"
)
print(response.output_text)
```

## 📂 Repository Structure

```
gpt-oss-tutorial/
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment template
├── .gitignore                   # Git ignore rules
│
├── src/                         # Shared utilities
│   ├── __init__.py
│   ├── config.py               # Configuration management
│   └── client.py               # OpenAI client wrapper
│
├── examples/                    # All examples organized by feature
│   ├── 01_basic/               # Basic API usage
│   │   ├── instructions.py
│   │   └── README.md
│   │
│   ├── 02_structured_output/   # Structured responses
│   │   ├── json_schema.py
│   │   ├── pydantic_parse.py
│   │   └── README.md
│   │
│   ├── 03_tools/               # Tool integration
│   │   ├── function_calling.py
│   │   ├── web_search.py
│   │   ├── mcp.py
│   │   └── README.md
│   │
│   ├── 04_multimodal/          # Image & multi-modal
│   │   ├── image_url.py
│   │   ├── image_base64.py
│   │   └── README.md
│   │
│   ├── 05_stateful/            # Conversation state
│   │   ├── store_retrieve.py
│   │   └── README.md
│   │
│   └── 06_advanced/            # Advanced features
│       ├── rag_pinecone.py
│       └── README.md
│
└── tests/                       # Unit tests
    └── test_examples.py
```

## 🔍 Module Details

### 01_basic - Basic Usage
Learn the fundamentals of the GPT-OSS API:
- Setting system instructions
- Making simple requests
- Understanding response structure

### 02_structured_output - Structured Output
Get type-safe, formatted responses:
- JSON Schema validation
- Pydantic model parsing
- Strict mode enforcement

### 03_tools - Tool Integration
Extend model capabilities with tools:
- Custom function calling
- Web search integration
- MCP server connections
- Parallel execution

### 04_multimodal - Multimodal
Work with images and text:
- URL-based image input
- Base64 encoded images
- Vision + reasoning

### 05_stateful - Stateful Conversations
Manage conversation state:
- Store responses
- Retrieve past conversations
- Session management

### 06_advanced - Advanced Features
Production-ready patterns:
- RAG with vector databases
- Tool routing strategies
- Reasoning summaries
- Multi-step workflows

### 07_reasoning - Reasoning Models
Working with reasoning-enabled models:
- Understanding reasoning tokens
- Extracting thought processes
- Optimizing reasoning performance

### 08_voice_agent - Voice Agent
Speech-to-text integration with AI agents:
- Whisper API for audio transcription
- OpenAI Agents SDK integration
- Vietnamese language support
- Async audio processing
- Multi-language translation
- **Note**: Requires OpenAI SDK 2.x (separate venv recommended)

## 🧪 Testing

Run tests to verify examples:

```bash
# Install with dev dependencies first
uv pip install -e ".[dev]"

# Run all tests
pytest tests/

# Run specific test
pytest tests/test_examples.py::test_basic_usage

# Run with coverage
pytest tests/ --cov=src --cov=examples
```

## 📝 API Reference

### Main Endpoint: `/v1/responses`

```python
response = client.responses.create(
    model="gpt-oss-20b",          # Model name
    input="Your prompt",           # User input (str or list)
    instructions="System prompt",  # Optional system instructions
    tools=[...],                   # Optional tools
    text={"format": {...}},        # Optional structured output
    store=False,                   # Store conversation
    include=["reasoning.encrypted_content"],  # Include reasoning
)
```

### Key Parameters

- **model**: Model identifier (e.g., `gpt-oss-20b`, `gpt-oss-120b`)
- **input**: User message(s) - string or array of message objects
- **instructions**: System-level instructions
- **tools**: Array of tool definitions (function, web_search, mcp)
- **text**: Structured output configuration
- **store**: Enable conversation storage
- **include**: Additional response fields

### Response Structure

```python
response.id                    # Unique response ID
response.output               # Response content (array)
response.output_text          # Extracted text (convenience)
response.output_parsed        # Parsed structured output
response.usage                # Token usage stats
```

## 🔧 Advanced Configuration

### Custom Client

```python
from src.client import create_client

client = create_client(
    api_key="custom_key",
    base_url="https://custom.endpoint.com",
    model_name="custom-model"
)
```

### Environment Variables

```env
# Required
API_KEY=your_api_key

# Optional (with defaults)
BASE_URL=https://mkp-api.fptcloud.com
MODEL_NAME=gpt-oss-20b

# For RAG examples
PINECONE_API_KEY=your_pinecone_key
```

## 🤝 Contributing

To add new examples or features:

1. Create a new subdirectory in `examples/`
2. Add your example scripts
3. Include a README.md explaining the feature
4. Update this main README
5. Add tests if applicable

### Example Template

```python
"""
Module: <feature_name>
Description: <what this example demonstrates>
"""

from src.client import create_client

def main():
    client = create_client()
    
    # Your example code here
    response = client.responses.create(...)
    
    print(response.output_text)

if __name__ == "__main__":
    main()
```

## 📚 Resources

- [GPT-OSS Documentation](https://docs.fptcloud.com)
- [OpenAI Python SDK](https://github.com/openai/openai-python)
- [API Reference](https://platform.openai.com/docs/api-reference)
- [Compatibility Guide](COMPATIBILITY.md) - **Read this if you have errors**
- [Installation Guide](INSTALL.md)
- [Quick Reference](QUICK_REFERENCE.md)

## 🐛 Troubleshooting

### Common Issues

**ModuleNotFoundError: No module named 'src'**
```bash
# Install the package in editable mode
uv pip install -e .
```

**OpenAI validation errors (logprobs, refusal, etc.)**
```bash
# Install compatible versions
uv pip install "openai==1.12.0" "httpx<0.25"
# See COMPATIBILITY.md for details
```

**Authentication Error**: Check your API_KEY in `.env`

**Import Error**: Ensure virtual environment is activated and package is installed
```bash
source .venv/bin/activate  # Activate venv
uv pip install -e .         # Install package
```

**Setup verification**: Run the check script
```bash
python check_setup.py
```

**Rate Limit**: Implement retry logic or reduce request frequency

For detailed troubleshooting, see [COMPATIBILITY.md](COMPATIBILITY.md)

## 📄 License

MIT License - see LICENSE file for details

## 🙋 Support

For questions or issues:
- Open an issue on GitHub
- Contact: hoang.nguyentien.2601@gmail.com

---

**Note**: This is a research and tutorial repository. Always follow your organization's security and usage policies when working with APIs.

