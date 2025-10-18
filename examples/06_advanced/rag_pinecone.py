"""
Example: Retrieval-Augmented Generation (RAG) with Pinecone

This example demonstrates how to build a complete RAG pipeline:
1. Load and embed documents
2. Store in vector database (Pinecone)
3. Retrieve relevant context
4. Generate responses with GPT-OSS

Key Concepts:
- Vector embeddings
- Semantic search
- Context retrieval
- RAG workflow
- Tool routing
"""

import os
import json
import time
import random
import string
from typing import List, Dict
from pprint import pprint

from tqdm.auto import tqdm
from pandas import DataFrame
from datasets import load_dataset
from pinecone import Pinecone, ServerlessSpec

from src.client import create_client, get_default_model, get_embedding_model
from src.config import get_config


class PineconeRAG:
    """
    RAG system using Pinecone vector database
    
    This class handles document loading, embedding, indexing, 
    retrieval, and generation.
    """
    
    def __init__(self, index_name: str = None):
        """
        Initialize RAG system
        
        Args:
            index_name: Pinecone index name (auto-generated if None)
        """
        self.client = create_client()
        self.config = get_config()
        self.model_name = get_default_model()
        self.embedding_model = get_embedding_model()
        
        # Initialize Pinecone
        self.pc = Pinecone(api_key=self.config.pinecone_api_key)
        
        # Generate index name if not provided
        if index_name is None:
            index_name = 'rag-index-' + ''.join(
                random.choices(string.ascii_lowercase + string.digits, k=10)
            )
        self.index_name = index_name
        self.index = None
    
    def load_dataset_sample(self, dataset_name: str, split: str = "train[:10]"):
        """
        Load a sample dataset
        
        Args:
            dataset_name: HuggingFace dataset name
            split: Dataset split specification
            
        Returns:
            DataFrame with processed data
        """
        print(f"\n📚 Loading dataset: {dataset_name}")
        ds = load_dataset(dataset_name, "en", split=split, trust_remote_code=True)
        df = DataFrame(ds)
        
        # Merge question and answer
        df['merged'] = df.apply(
            lambda row: f"Question: {row['Question']}\nAnswer: {row['Response']}", 
            axis=1
        )
        
        print(f"✅ Loaded {len(df)} documents")
        print(f"\nExample document:\n{df['merged'].iloc[0][:300]}...\n")
        
        return df
    
    def create_index(self, dimension: int, metric: str = "dotproduct"):
        """
        Create Pinecone index
        
        Args:
            dimension: Embedding dimension
            metric: Distance metric (dotproduct, cosine, euclidean)
        """
        print(f"\n🔧 Creating Pinecone index: {self.index_name}")
        
        # Check if index exists
        existing_indexes = self.pc.list_indexes().names()
        
        if self.index_name in existing_indexes:
            print(f"⚠️  Index '{self.index_name}' already exists. Using existing index.")
        else:
            spec = ServerlessSpec(cloud="aws", region="us-east-1")
            self.pc.create_index(
                self.index_name,
                dimension=dimension,
                metric=metric,
                spec=spec
            )
            print(f"✅ Created new index")
        
        # Connect to index
        self.index = self.pc.Index(self.index_name)
        time.sleep(1)  # Wait for index to be ready
        
        stats = self.index.describe_index_stats()
        print(f"📊 Index stats: {stats}")
    
    def embed_and_upsert(self, df: DataFrame, batch_size: int = 32):
        """
        Embed documents and upsert to Pinecone
        
        Args:
            df: DataFrame with 'merged' column containing documents
            batch_size: Batch size for processing
        """
        print(f"\n🔄 Embedding and upserting {len(df)} documents...")
        
        for i in tqdm(range(0, len(df), batch_size), desc="Processing batches"):
            i_end = min(i + batch_size, len(df))
            
            # Get batch
            batch_texts = df['merged'].iloc[i:i_end].tolist()
            batch_ids = [str(n) for n in range(i, i_end)]
            
            # Create embeddings
            embed_response = self.client.embeddings.create(
                input=batch_texts,
                model=self.embedding_model
            )
            embeddings = [record.embedding for record in embed_response.data]
            
            # Prepare metadata
            metadata = []
            for _, row in df.iloc[i:i_end].iterrows():
                metadata.append({
                    "Question": row['Question'],
                    "Answer": row['Response']
                })
            
            # Upsert to Pinecone
            vectors = list(zip(batch_ids, embeddings, metadata))
            self.index.upsert(vectors=vectors)
        
        print(f"✅ Upserted {len(df)} documents to Pinecone")
    
    def query(self, query_text: str, top_k: int = 5) -> List[Dict]:
        """
        Query the vector database
        
        Args:
            query_text: Query text
            top_k: Number of results to return
            
        Returns:
            List of matches with metadata
        """
        # Embed query
        query_embedding = self.client.embeddings.create(
            input=query_text,
            model=self.embedding_model
        ).data[0].embedding
        
        # Search
        results = self.index.query(
            vector=[query_embedding],
            top_k=top_k,
            include_metadata=True
        )
        
        return results['matches']
    
    def generate_with_context(self, query: str, top_k: int = 3) -> str:
        """
        Generate response using retrieved context
        
        Args:
            query: User query
            top_k: Number of context documents to retrieve
            
        Returns:
            Generated response text
        """
        # Retrieve context
        matches = self.query(query, top_k=top_k)
        
        # Build context string
        context_parts = []
        for i, match in enumerate(matches, 1):
            meta = match['metadata']
            context_parts.append(
                f"Document {i} (score: {match['score']:.3f}):\n"
                f"Q: {meta.get('Question', 'N/A')}\n"
                f"A: {meta.get('Answer', 'N/A')}"
            )
        
        context = "\n\n".join(context_parts)
        
        # Generate response
        prompt = (
            f"Based on the following context, answer the question.\n\n"
            f"Context:\n{context}\n\n"
            f"Question: {query}\n\n"
            f"Answer based on the context provided:"
        )
        
        response = self.client.responses.create(
            model=self.model_name,
            input=prompt,
        )
        
        return response.output_text
    
    def cleanup(self):
        """Delete the Pinecone index"""
        if self.index_name:
            print(f"\n🗑️  Deleting index: {self.index_name}")
            self.pc.delete_index(self.index_name)
            print("✅ Index deleted")


def simple_rag_example():
    """
    Example: Basic RAG workflow
    
    Demonstrates the complete RAG pipeline from data loading to generation.
    """
    print("=" * 60)
    print("Example: Simple RAG with Pinecone")
    print("=" * 60)
    
    # Initialize RAG system
    rag = PineconeRAG()
    
    # Load dataset
    df = rag.load_dataset_sample(
        "FreedomIntelligence/medical-o1-reasoning-SFT",
        split="train[:10]"
    )
    
    # Get embedding dimension
    sample_embed = rag.client.embeddings.create(
        input=[df['merged'].iloc[0]],
        model=rag.embedding_model
    )
    embed_dim = len(sample_embed.data[0].embedding)
    print(f"📏 Embedding dimension: {embed_dim}")
    
    # Create index and upsert data
    rag.create_index(dimension=embed_dim)
    rag.embed_and_upsert(df)
    
    # Query the system
    query = (
        "A 45-year-old man with a history of alcohol use presents with "
        "confusion, ataxia, and ophthalmoplegia. What is the most likely "
        "diagnosis and recommended treatment?"
    )
    
    print(f"\n❓ Query: {query}")
    print("\n🔍 Retrieving relevant documents...")
    
    matches = rag.query(query, top_k=3)
    
    print("\n📄 Top matches:")
    for i, match in enumerate(matches, 1):
        print(f"\n  {i}. Score: {match['score']:.3f}")
        print(f"     Question: {match['metadata']['Question'][:100]}...")
    
    # Generate answer
    print("\n🤖 Generating answer...")
    answer = rag.generate_with_context(query, top_k=3)
    
    print("\n💡 Answer:")
    print(answer)
    
    # Cleanup
    rag.cleanup()
    
    print("\n" + "=" * 60)
    return rag


def rag_with_tool_routing():
    """
    Example: RAG with tool routing
    
    Demonstrates how to route queries between web search and RAG
    """
    print("\n" + "=" * 60)
    print("Example: RAG with Tool Routing")
    print("=" * 60)
    
    client = create_client()
    model = get_default_model()
    
    # Initialize RAG
    rag = PineconeRAG()
    df = rag.load_dataset_sample(
        "FreedomIntelligence/medical-o1-reasoning-SFT",
        split="train[:10]"
    )
    
    sample_embed = rag.client.embeddings.create(
        input=[df['merged'].iloc[0]],
        model=rag.embedding_model
    )
    embed_dim = len(sample_embed.data[0].embedding)
    
    rag.create_index(dimension=embed_dim)
    rag.embed_and_upsert(df)
    
    # Define tools
    tools = [
        {
            "type": "web_search_preview",
            "user_location": {
                "type": "approximate",
                "country": "US",
                "region": "California",
                "city": "SF"
            },
            "search_context_size": "medium"
        },
        {
            "type": "function",
            "name": "search_medical_knowledge_base",
            "description": "Search internal medical knowledge base for medical questions",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Medical question to search"
                    },
                    "top_k": {
                        "type": "integer",
                        "description": "Number of results",
                        "default": 3
                    }
                },
                "required": ["query"],
                "additionalProperties": False
            }
        }
    ]
    
    # Test queries
    queries = [
        {
            "query": "Who won the cricket world cup in 1983?",
            "expected_tool": "web_search"
        },
        {
            "query": (
                "What is the most common cause of death in patients "
                "with sickle cell disease?"
            ),
            "expected_tool": "medical_kb"
        },
        {
            "query": "What is the current Bitcoin price?",
            "expected_tool": "web_search"
        }
    ]
    
    # Process queries
    for item in queries:
        query = item["query"]
        print(f"\n🌟 Query: {query}")
        print(f"   Expected tool: {item['expected_tool']}")
        
        # Call API
        response = client.responses.create(
            model=model,
            input=[
                {
                    "role": "system",
                    "content": "Route queries appropriately: use web search for "
                               "current events/general info, use medical KB for medical questions"
                },
                {"role": "user", "content": query}
            ],
            tools=tools,
            parallel_tool_calls=True
        )
        
        # Check which tool was called
        if response.output:
            first_item = response.output[0]
            print(f"   🔧 Tool used: {first_item.type}")
            
            if first_item.type == "function_call":
                print(f"   Function: {first_item.name}")
                
                if first_item.name == "search_medical_knowledge_base":
                    # Execute RAG search
                    args = json.loads(first_item.arguments)
                    matches = rag.query(args['query'], top_k=3)
                    
                    result = {
                        "matches": [
                            {
                                "question": m['metadata']['Question'],
                                "answer": m['metadata']['Answer'][:200] + "...",
                                "score": float(m['score'])
                            }
                            for m in matches
                        ]
                    }
                    
                    print(f"   ✅ Retrieved {len(matches)} documents from KB")
    
    # Cleanup
    rag.cleanup()
    
    print("\n" + "=" * 60)
    return rag


def main():
    """Run all advanced examples"""
    print("\n🚀 GPT-OSS Advanced Examples - RAG")
    print("=" * 60)
    
    print("\nℹ️  Note: These examples require:")
    print("  • PINECONE_API_KEY environment variable")
    print("  • Internet connection for dataset download")
    print("  • May take a few minutes to run\n")
    
    config = get_config()
    if not config.pinecone_api_key:
        print("❌ Error: PINECONE_API_KEY not found in environment")
        print("   Please set it in your .env file")
        return
    
    try:
        # Example 1: Simple RAG
        simple_rag_example()
        
        # Example 2: Tool routing
        rag_with_tool_routing()
        
        print("\n✅ All advanced examples completed!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

