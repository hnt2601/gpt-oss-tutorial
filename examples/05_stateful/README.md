# 05 - Stateful Conversations

This module demonstrates how to store and manage conversation state using GPT-OSS API's built-in state management.

## 📚 What You'll Learn

- Storing responses with `store=True`
- Retrieving past conversations
- Multi-turn stateful conversations
- Conversation branching
- Session management

## 🎯 Examples

### Basic Store and Retrieve

```python
# Store a response
response = client.responses.create(
    model="gpt-oss-20b",
    input="Tell me a joke",
    store=True  # Enable storage
)

response_id = response.id

# Retrieve later
fetched = client.responses.retrieve(response_id=response_id)
print(fetched.output_text)
```

## 🚀 Running the Examples

```bash
python examples/05_stateful/store_retrieve.py
```

## 💾 State Management

### Enabling Storage

```python
# Without storage (default)
response = client.responses.create(
    input="Hello",
    store=False  # Not stored, cannot retrieve later
)

# With storage
response = client.responses.create(
    input="Hello",
    store=True  # Stored, can retrieve later
)
```

### Retrieving Stored Responses

```python
# Get response by ID
response = client.responses.retrieve(
    response_id="resp_abc123xyz"
)

# Access output
print(response.output_text)
print(response.model)
print(response.usage)
```

## 🔄 Multi-turn Conversations

### Building Context

```python
# Turn 1
response_1 = client.responses.create(
    input="My name is Alice",
    store=True
)

# Turn 2 - Include previous context
context = [
    {"role": "user", "content": "My name is Alice"},
    *response_1.output,  # Add previous response
    {"role": "user", "content": "What's my name?"}
]

response_2 = client.responses.create(
    input=context,
    store=True
)

# Model remembers: "Your name is Alice"
```

### Context Structure

```python
context = [
    # User message
    {"role": "user", "content": "First question"},
    
    # Assistant response (from response.output)
    {"role": "assistant", "content": [...]},
    
    # Next user message
    {"role": "user", "content": "Follow-up question"},
    
    # And so on...
]
```

## 🌳 Conversation Branching

Create different conversation paths from a single base:

```python
# Base conversation
base = client.responses.create(
    input="I want to learn programming",
    store=True
)

# Branch 1: Python path
python_context = [
    {"role": "user", "content": "I want to learn programming"},
    *base.output,
    {"role": "user", "content": "Teach me Python"}
]
python_branch = client.responses.create(input=python_context, store=True)

# Branch 2: JavaScript path
js_context = [
    {"role": "user", "content": "I want to learn programming"},
    *base.output,
    {"role": "user", "content": "Teach me JavaScript"}
]
js_branch = client.responses.create(input=js_context, store=True)

# Tree structure:
# base_id
# ├─ python_branch.id
# └─ js_branch.id
```

## 📊 Session Management

### Organizing Conversations

```python
class ConversationSession:
    def __init__(self, client, topic: str):
        self.client = client
        self.topic = topic
        self.response_ids = []
        self.context = []
    
    def send(self, message: str):
        self.context.append({"role": "user", "content": message})
        
        response = self.client.responses.create(
            input=self.context,
            store=True
        )
        
        self.response_ids.append(response.id)
        self.context.extend(response.output)
        
        return response
    
    def get_history(self):
        return [
            self.client.responses.retrieve(response_id=rid)
            for rid in self.response_ids
        ]

# Usage
session = ConversationSession(client, "Python Learning")
session.send("How do I use decorators?")
session.send("Can you show me an example?")
history = session.get_history()
```

### Metadata Tracking

```python
conversations = {}

def create_conversation(topic: str, category: str):
    response = client.responses.create(
        input=f"Let's discuss {topic}",
        store=True
    )
    
    conversations[response.id] = {
        "topic": topic,
        "category": category,
        "created_at": datetime.now(),
        "turns": 1
    }
    
    return response.id

def continue_conversation(conv_id: str, message: str):
    # Retrieve and continue...
    pass

# Create conversations
conv1 = create_conversation("Python asyncio", "technical")
conv2 = create_conversation("Autumn poems", "creative")

# Later: find conversations by category
technical_convs = [
    cid for cid, meta in conversations.items()
    if meta["category"] == "technical"
]
```

## 💡 Best Practices

### 1. Context Window Management

```python
# Good: Keep context manageable
context = context[-10:]  # Keep last 10 messages

# Avoid: Unlimited context growth
context.append(...)  # Eventually hits token limit
```

### 2. Selective Storage

```python
# Store important conversations
if is_important:
    response = client.responses.create(input=msg, store=True)
else:
    response = client.responses.create(input=msg, store=False)
```

### 3. Error Handling

```python
try:
    response = client.responses.retrieve(response_id=conv_id)
except Exception as e:
    print(f"Failed to retrieve conversation: {e}")
    # Handle missing/expired conversation
```

### 4. Conversation Lifecycle

```python
class Conversation:
    def __init__(self, client, ttl_hours=24):
        self.client = client
        self.id = None
        self.created_at = None
        self.ttl_hours = ttl_hours
    
    def is_expired(self):
        if not self.created_at:
            return True
        age = datetime.now() - self.created_at
        return age.total_seconds() > (self.ttl_hours * 3600)
    
    def get_or_create(self):
        if self.is_expired():
            # Start fresh conversation
            return self.create_new()
        else:
            # Continue existing
            return self.retrieve_existing()
```

## 🎨 Use Cases

### Customer Support

```python
# Track support tickets
ticket_id = "TICKET-123"

support_session = {
    "ticket_id": ticket_id,
    "customer": "john@example.com",
    "conversation_ids": []
}

# Each interaction stores state
response = client.responses.create(
    input=customer_message,
    store=True
)
support_session["conversation_ids"].append(response.id)

# Later: review full conversation history
for conv_id in support_session["conversation_ids"]:
    conv = client.responses.retrieve(response_id=conv_id)
    print(conv.output_text)
```

### Learning/Tutorial Sessions

```python
# Multi-lesson learning session
class LearningSession:
    def __init__(self, client, course: str):
        self.client = client
        self.course = course
        self.lessons = {}
    
    def complete_lesson(self, lesson_num: int, content: str):
        response = self.client.responses.create(
            input=f"Lesson {lesson_num}: {content}",
            store=True
        )
        self.lessons[lesson_num] = response.id
    
    def review_lesson(self, lesson_num: int):
        if lesson_num in self.lessons:
            return self.client.responses.retrieve(
                response_id=self.lessons[lesson_num]
            )
```

### A/B Testing Conversations

```python
# Test different conversation strategies
base = client.responses.create(input=query, store=True)

# Strategy A: Direct answer
strategy_a = client.responses.create(
    input=[
        *base.output,
        {"role": "user", "content": "Give me a direct answer"}
    ],
    store=True
)

# Strategy B: Socratic method
strategy_b = client.responses.create(
    input=[
        *base.output,
        {"role": "user", "content": "Help me figure it out"}
    ],
    store=True
)

# Compare results
print(f"Strategy A: {strategy_a.id}")
print(f"Strategy B: {strategy_b.id}")
```

## ⚠️ Limitations

- **Storage Duration**: Stored responses may have TTL (time-to-live)
- **Token Limits**: Context windows still have token limits
- **Retrieval**: Old conversations may expire/be purged
- **Privacy**: Be mindful of storing sensitive information

## 🔗 Related Examples

- **01_basic**: Foundation for multi-turn conversations
- **03_tools**: Stateful + tool usage
- **06_advanced**: RAG with conversation state

## 📚 References

- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [Context Window Management](https://platform.openai.com/docs/guides/context-window)

