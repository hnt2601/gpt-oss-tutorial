# 03 - Tool Integration

This module demonstrates how to extend GPT-OSS capabilities using tools: custom functions, web search, and MCP servers.

## 📚 What You'll Learn

- Function calling workflow
- Built-in web search tool
- Model Context Protocol (MCP) integration
- Parallel tool execution
- Tool approval policies

## 🎯 Examples

### 1. Function Calling (`function_calling.py`)

Allow the model to call your custom functions:

```python
tools = [{
    "type": "function",
    "name": "get_weather",
    "description": "Get current temperature for coordinates.",
    "parameters": {
        "type": "object",
        "properties": {
            "latitude": {"type": "number"},
            "longitude": {"type": "number"}
        },
        "required": ["latitude", "longitude"],
    },
}]

response = client.responses.create(
    model="gpt-oss-20b",
    input="What's the weather in Paris?",
    tools=tools,
)

# Execute the function
tool_call = response.output[1]
args = json.loads(tool_call.arguments)
result = get_weather(**args)

# Return result to model
context.append({
    "type": "function_call_output",
    "call_id": tool_call.call_id,
    "output": str(result)
})
```

### 2. Web Search (`web_search.py`)

Enable real-time web searching:

```python
response = client.responses.create(
    model="gpt-oss-20b",
    input="What's the latest news about AI?",
    tools=[{"type": "web_search"}]
)
```

With location context:
```python
tools=[{
    "type": "web_search_preview",
    "user_location": {
        "type": "approximate",
        "country": "US",
        "region": "California",
        "city": "SF"
    },
    "search_context_size": "medium"
}]
```

### 3. MCP - Model Context Protocol (`mcp.py`)

Connect to external tool servers:

```python
response = client.responses.create(
    input="How does tiktoken work?",
    tools=[{
        "type": "mcp",
        "server_label": "gitmcp",
        "server_url": "https://gitmcp.io/openai/tiktoken",
        "allowed_tools": ["search_docs", "fetch_docs"],
        "require_approval": "never"
    }]
)
```

## 🚀 Running the Examples

```bash
# Function calling
python examples/03_tools/function_calling.py

# Web search
python examples/03_tools/web_search.py

# MCP integration
python examples/03_tools/mcp.py
```

## 🔄 Function Calling Workflow

```
1. User Query
   ↓
2. Model decides to call function
   ↓
3. Parse function call from response.output
   ↓
4. Execute function in your code
   ↓
5. Add function result to context
   ↓
6. Model generates final response
```

### Code Example:

```python
# Step 1-2: Initial request
response = client.responses.create(
    input="What's the weather?",
    tools=[get_weather_tool]
)

# Step 3: Get function call
tool_call = response.output[1]

# Step 4: Execute
args = json.loads(tool_call.arguments)
result = get_weather(**args)

# Step 5: Add result
context.append({
    "type": "function_call_output",
    "call_id": tool_call.call_id,
    "output": str(result)
})

# Step 6: Final response
response = client.responses.create(
    input=context,
    tools=[get_weather_tool]
)
```

## 🌐 Web Search Features

### Basic Search
```python
{"type": "web_search"}
```

### Advanced Search
```python
{
    "type": "web_search_preview",
    "user_location": {
        "type": "approximate",
        "country": "US",
        "region": "California"
    },
    "search_context_size": "medium"  # small|medium|large
}
```

**Use Cases:**
- Current events and news
- Fact verification
- Price comparisons
- Technical specifications
- Local information

## 🔌 MCP Integration

### Approval Policies

| Policy | Description | Use Case |
|--------|-------------|----------|
| `never` | Auto-approve all calls | Development, testing |
| `always` | Require approval for every call | Production, sensitive ops |
| `auto` | Smart approval based on operation | Balanced security |

### Tool Filtering

```python
{
    "type": "mcp",
    "server_url": "https://api.example.com",
    "allowed_tools": [
        "read_data",    # ✅ Allowed
        "search_data"   # ✅ Allowed
        # "delete_data" ❌ Not in list
    ]
}
```

## 🔀 Parallel Tool Calls

Enable multiple tools to run simultaneously:

```python
response = client.responses.create(
    input="Check weather in Paris and New York",
    tools=[weather_tool],
    parallel_tool_calls=True  # Enable parallel execution
)

# Response may contain multiple function_call items
for item in response.output:
    if item.type == "function_call":
        # Process each call
        execute_function(item)
```

## 💡 Best Practices

### 1. Function Design

```python
# Good: Clear, specific function
def get_weather(lat: float, lon: float) -> dict:
    """Get weather for coordinates"""
    return {"temp": 20, "condition": "sunny"}

# Avoid: Too broad
def do_something(data: str) -> str:
    """Does something"""
    pass
```

### 2. Error Handling

```python
try:
    result = execute_function(args)
except Exception as e:
    # Return error as function output
    context.append({
        "type": "function_call_output",
        "call_id": tool_call.call_id,
        "output": f"Error: {str(e)}"
    })
```

### 3. Tool Selection

- **Custom Functions**: For business logic, DB queries, calculations
- **Web Search**: For current info, news, facts
- **MCP**: For external services, APIs, specialized tools

## 🎨 Use Cases

### Data Retrieval
```python
# Function to query database
def get_user_orders(user_id: str) -> list:
    return db.query("SELECT * FROM orders WHERE user_id = ?", user_id)
```

### Real-time Information
```python
# Web search for current data
tools=[{"type": "web_search"}]
input="What's the current Bitcoin price?"
```

### External Services
```python
# MCP for third-party APIs
{
    "type": "mcp",
    "server_url": "https://api.stripe.com/mcp",
    "allowed_tools": ["get_payment_status"]
}
```

## 🔍 Reasoning & Debugging

Access model's reasoning:

```python
response = client.responses.create(
    input="Complex query requiring tool use",
    tools=[...],
    include=["reasoning.encrypted_content"],
    reasoning={"summary": "auto"}
)

# Get reasoning summary
reasoning_item = response.output[0]
print(reasoning_item.summary[0].text)
```

## 🔗 Related Examples

- **02_structured_output**: Combine tools with structured responses
- **06_advanced**: RAG with function calling

## 📚 References

- [OpenAI Function Calling Guide](https://platform.openai.com/docs/guides/function-calling)
- [Model Context Protocol Docs](https://modelcontextprotocol.io/)
- [Open-Meteo API](https://open-meteo.com/) (used in examples)

