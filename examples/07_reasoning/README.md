# 06 - Advanced Features

This module covers advanced GPT-OSS patterns including RAG (Retrieval-Augmented Generation), tool routing, and complex workflows.

## 📚 What You'll Learn

- Building RAG pipelines
- Vector embeddings and semantic search
- Pinecone integration
- Tool routing strategies
- Multi-step workflows

## 🎯 Examples

### RAG with Pinecone (`rag_pinecone.py`)

Complete RAG implementation with vector database:

```python
from examples.advanced.rag_pinecone import PineconeRAG

# Initialize RAG system
rag = PineconeRAG()

# Load and index documents
df = rag.load_dataset_sample("dataset_name")
rag.create_index(dimension=1024)
rag.embed_and_upsert(df)

# Query with retrieval
answer = rag.generate_with_context(
    "What is the treatment for condition X?"
)
```

## 🚀 Running the Examples

```bash
# Set up Pinecone API key first
export PINECONE_API_KEY=your_key_here

# Run RAG example
python examples/06_advanced/rag_pinecone.py
```

## 🔄 RAG Pipeline Architecture

```
1. Document Loading
   ↓
2. Chunking & Preprocessing
   ↓
3. Embedding Generation
   ↓
4. Vector Storage (Pinecone)
   ↓
5. Query Processing
   ↓
6. Semantic Search
   ↓
7. Context Retrieval
   ↓
8. LLM Generation
   ↓
9. Response
```

## 📊 RAG Components

### 1. Document Loading

```python
from datasets import load_dataset
from pandas import DataFrame

# Load dataset
ds = load_dataset("dataset_name", split="train[:100]")
df = DataFrame(ds)

# Prepare documents
df['text'] = df.apply(
    lambda row: f"Q: {row['question']}\nA: {row['answer']}", 
    axis=1
)
```

### 2. Embedding Generation

```python
client = create_client()

# Generate embeddings
response = client.embeddings.create(
    input=["Document text here"],
    model="multilingual-e5-large"
)

embedding = response.data[0].embedding
dimension = len(embedding)  # e.g., 1024
```

### 3. Vector Storage

```python
from pinecone import Pinecone, ServerlessSpec

# Initialize
pc = Pinecone(api_key="your_key")

# Create index
pc.create_index(
    name="my-index",
    dimension=1024,
    metric="dotproduct",
    spec=ServerlessSpec(cloud="aws", region="us-east-1")
)

# Connect and upsert
index = pc.Index("my-index")
index.upsert(vectors=[
    ("id1", embedding1, {"text": "..."}),
    ("id2", embedding2, {"text": "..."})
])
```

### 4. Semantic Search

```python
# Query
query_embedding = client.embeddings.create(
    input="user query",
    model="multilingual-e5-large"
).data[0].embedding

# Search
results = index.query(
    vector=query_embedding,
    top_k=5,
    include_metadata=True
)

for match in results['matches']:
    print(f"Score: {match['score']}")
    print(f"Text: {match['metadata']['text']}")
```

### 5. Generation with Context

```python
# Build context from retrieved docs
context = "\n\n".join([
    match['metadata']['text'] 
    for match in results['matches']
])

# Generate answer
response = client.responses.create(
    model="gpt-oss-20b",
    input=f"Context: {context}\n\nQuestion: {query}\n\nAnswer:",
)
```

## 🧩 Tool Routing

### Strategy: Route by Query Type

```python
tools = [
    {"type": "web_search"},  # For current events
    {
        "type": "function",
        "name": "search_knowledge_base",  # For internal docs
        "description": "Search internal knowledge base"
    }
]

response = client.responses.create(
    model="gpt-oss-20b",
    input=[
        {
            "role": "system",
            "content": "Use web search for news/current events, "
                      "KB search for internal/technical questions"
        },
        {"role": "user", "content": query}
    ],
    tools=tools
)

# Model automatically selects appropriate tool
```

## 💡 Best Practices

### 1. Chunking Strategy

```python
def chunk_text(text: str, chunk_size: int = 512, overlap: int = 50):
    """Split text into overlapping chunks"""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks

# Better retrieval with smaller chunks
chunks = chunk_text(long_document)
for chunk in chunks:
    embed_and_store(chunk)
```

### 2. Metadata Management

```python
# Rich metadata for filtering/ranking
metadata = {
    "source": "medical_journal",
    "date": "2024-01-15",
    "author": "Dr. Smith",
    "category": "cardiology",
    "keywords": ["heart", "treatment"],
    "text": chunk_text
}

index.upsert(vectors=[(id, embedding, metadata)])

# Query with filters
results = index.query(
    vector=query_embedding,
    top_k=10,
    filter={"category": "cardiology"}
)
```

### 3. Hybrid Search

```python
# Combine semantic + keyword search
def hybrid_search(query: str, keywords: List[str]):
    # Semantic search
    semantic_results = vector_search(query)
    
    # Keyword filter
    filtered = [
        r for r in semantic_results
        if any(kw in r['metadata']['text'] for kw in keywords)
    ]
    
    return filtered

results = hybrid_search(
    "heart disease treatment",
    keywords=["medication", "surgery", "therapy"]
)
```

### 4. Re-ranking

```python
def rerank_results(query: str, results: List[Dict]):
    """Re-rank results using cross-encoder"""
    # Score each result
    scored = []
    for result in results:
        # Calculate relevance score
        score = calculate_relevance(query, result['text'])
        scored.append((score, result))
    
    # Sort by score
    scored.sort(reverse=True)
    return [r for _, r in scored]

# Apply re-ranking
initial_results = index.query(vector=query_emb, top_k=20)
final_results = rerank_results(query, initial_results)[:5]
```

## 🎨 Use Cases

### Knowledge Base Q&A

```python
class KnowledgeBaseRAG:
    def __init__(self):
        self.rag = PineconeRAG()
        
    def load_documents(self, docs: List[str]):
        """Load company docs into KB"""
        df = DataFrame({"text": docs})
        self.rag.embed_and_upsert(df)
    
    def answer_question(self, question: str):
        """Answer using KB context"""
        return self.rag.generate_with_context(question)

# Usage
kb = KnowledgeBaseRAG()
kb.load_documents(company_docs)
answer = kb.answer_question("What is our return policy?")
```

### Customer Support

```python
def customer_support_rag(query: str, user_id: str):
    """Context-aware support with user history"""
    
    # Retrieve relevant docs
    doc_context = rag.query(query, top_k=3)
    
    # Get user history
    user_history = get_user_history(user_id)
    
    # Combine contexts
    full_context = f"""
    User History: {user_history}
    
    Relevant Documentation:
    {format_docs(doc_context)}
    
    User Question: {query}
    """
    
    return client.responses.create(
        input=full_context,
        model="gpt-oss-20b"
    )
```

### Multi-modal RAG

```python
def multimodal_rag(text_query: str, image_url: str):
    """RAG with text + image"""
    
    # Text retrieval
    text_results = rag.query(text_query, top_k=3)
    context = format_context(text_results)
    
    # Generate with image + context
    response = client.responses.create(
        input=[{
            "role": "user",
            "content": [
                {"type": "input_text", "text": f"Context: {context}\n\nQuestion: {text_query}"},
                {"type": "input_image", "image_url": image_url}
            ]
        }]
    )
    
    return response.output_text
```

## 🔧 Optimization Tips

### 1. Batch Processing

```python
# Process embeddings in batches
batch_size = 32
for i in range(0, len(documents), batch_size):
    batch = documents[i:i+batch_size]
    embeddings = client.embeddings.create(
        input=batch,
        model="multilingual-e5-large"
    )
    # Upsert batch
```

### 2. Caching

```python
import hashlib
from functools import lru_cache

@lru_cache(maxsize=1000)
def get_embedding(text: str):
    """Cache embeddings to avoid recomputation"""
    response = client.embeddings.create(
        input=[text],
        model="multilingual-e5-large"
    )
    return response.data[0].embedding
```

### 3. Index Optimization

```python
# Use namespaces for logical separation
index.upsert(
    vectors=vectors,
    namespace="medical_docs"
)

index.upsert(
    vectors=vectors,
    namespace="legal_docs"
)

# Query specific namespace
results = index.query(
    vector=query_emb,
    top_k=5,
    namespace="medical_docs"
)
```

## ⚠️ Considerations

- **Cost**: Embedding generation + vector storage costs
- **Latency**: Retrieval adds latency to responses
- **Quality**: Depends on document quality and chunking
- **Updates**: Need to re-embed when documents change
- **Scale**: Index size limits (check Pinecone pricing)

## 🔗 Related Examples

- **02_structured_output**: Extract structured data from RAG
- **03_tools**: Combine RAG with other tools
- **05_stateful**: Stateful RAG conversations

## 📚 References

- [Pinecone Documentation](https://docs.pinecone.io/)
- [Vector Embeddings Guide](https://www.pinecone.io/learn/vector-embeddings/)
- [RAG Best Practices](https://www.pinecone.io/learn/retrieval-augmented-generation/)
- [Embedding Models](https://huggingface.co/models?pipeline_tag=sentence-similarity)

