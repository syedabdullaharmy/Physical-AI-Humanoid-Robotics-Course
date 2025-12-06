import os
import glob
from typing import List
import google.generativeai as genai
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from dotenv import load_dotenv
import re

load_dotenv()

# Configuration
DOCS_DIR = os.path.join(os.path.dirname(__file__), "../docs")
# Use local disk storage specific to this project to allow sharing between ingest and main
QDRANT_PATH = os.path.join(os.path.dirname(__file__), "qdrant_data")
QDRANT_URL = os.getenv("QDRANT_URL", None) # Default to None to prefer path or memory logic below
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
COLLECTION_NAME = "textbook_rag"

# Initialize Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Initialize Qdrant
# Initialize Qdrant
if QDRANT_URL and QDRANT_URL != ":memory:":
    client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
else:
    # Use local disk persistence
    print(f"Using local Qdrant storage at: {QDRANT_PATH}")
    client = QdrantClient(path=QDRANT_PATH)

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    # Improved chunking with overlap
    chunks = []
    start = 0
    text_len = len(text)

    while start < text_len:
        end = start + chunk_size
        
        # Try to find a natural break point (newline or period) near the end
        if end < text_len:
            # Look for the last newline in the window
            last_newline = text.rfind('\n', start, end)
            if last_newline != -1 and last_newline > start + chunk_size // 2:
                end = last_newline + 1
            else:
                # Look for the last period
                last_period = text.rfind('. ', start, end)
                if last_period != -1 and last_period > start + chunk_size // 2:
                    end = last_period + 1
        
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        
        # If we reached the end, break
        if end >= text_len:
            break
            
        # Move start forward, but keep overlap
        start = end - overlap
        
    return chunks

import time
import random

def embed_content(text: str) -> List[float]:
    # Use Gemini Embedding
    retries = 5
    base_delay = 2
    
    for attempt in range(retries):
        try:
            result = genai.embed_content(
                model="models/text-embedding-004",
                content=text,
                task_type="retrieval_document"
                # title="Textbook Content"
            )
            return result['embedding']
        except Exception as e:
            if "Quota exceeded" in str(e) or "429" in str(e):
                delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
                print(f"Rate limit hit. Retrying in {delay:.2f}s...")
                time.sleep(delay)
            else:
                print(f"Error embedding text: {e}")
                return []
    print("Max retries exceeded for embedding.")
    return []

def ingest_docs():
    print("Creating collection...")
    client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=768, distance=Distance.COSINE),
    )

    # Include both .md and .mdx files
    md_files = glob.glob(os.path.join(DOCS_DIR, "**/*.md"), recursive=True)
    mdx_files = glob.glob(os.path.join(DOCS_DIR, "**/*.mdx"), recursive=True)
    files = md_files + mdx_files
    print(f"Found {len(files)} markdown files ({len(md_files)} .md, {len(mdx_files)} .mdx).")
    
    points = []
    id_counter = 0

    for file_path in files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Skip empty files
            if not content.strip():
                print(f"Skipping empty file: {file_path}")
                continue
            
            # Extract title (simplified)
            title = os.path.basename(file_path)
            
            chunks = chunk_text(content)
            if not chunks:
                print(f"No chunks generated for {title}, skipping...")
                continue
                
            print(f"Processing {title}: {len(chunks)} chunks")

            for i, chunk in enumerate(chunks):
                embedding = embed_content(chunk)
                if not embedding:
                    continue
                
                points.append(PointStruct(
                    id=id_counter,
                    vector=embedding,
                    payload={"source": title, "content": chunk, "chunk_index": i}
                ))
                id_counter += 1
                
                # Batch upload to avoid memory issues
                if len(points) >= 50:
                    client.upsert(
                        collection_name=COLLECTION_NAME,
                        points=points
                    )
                    points = []
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            continue
    
    if points:
        client.upsert(
            collection_name=COLLECTION_NAME,
            points=points
        )
    
    print("Ingestion complete.")

if __name__ == "__main__":
    if not GEMINI_API_KEY:
        print("Error: GEMINI_API_KEY not set in .env")
    else:
        ingest_docs()
