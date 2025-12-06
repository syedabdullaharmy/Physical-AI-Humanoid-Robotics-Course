import os
import google.generativeai as genai
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from dotenv import load_dotenv
import time

load_dotenv()

# Configuration
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
COLLECTION_NAME = "textbook_rag"

# Initialize
genai.configure(api_key=GEMINI_API_KEY)
client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

# Sample content for quick testing
sample_content = [
    {
        "source": "intro.mdx",
        "content": """Welcome to the Physical AI & Humanoid Robotics Course. This comprehensive 13-week program is designed for industry practitioners who want to master the fundamentals of robotics, ROS 2, digital twins, and humanoid robotics. You'll learn hands-on skills in robot programming, simulation, and deployment."""
    },
    {
        "source": "module-1-ros2/chapter-1-intro-ros2.mdx",
        "content": """ROS 2 (Robot Operating System 2) is the next generation of ROS, designed for production robotics. It provides a flexible framework for writing robot software with features like distributed computing, real-time capabilities, and improved security. ROS 2 uses DDS (Data Distribution Service) for communication."""
    },
    {
        "source": "module-1-ros2/chapter-2-nodes-topics.mdx",
        "content": """In ROS 2, nodes are the fundamental building blocks. A node is a process that performs computation. Nodes communicate with each other using topics, which are named buses over which nodes exchange messages. Publishers send messages to topics, and subscribers receive them."""
    },
    {
        "source": "setup/workstation.mdx",
        "content": """To set up your development workstation for this course, you'll need Ubuntu 22.04 or later, ROS 2 Humble, Python 3.10+, and various simulation tools. We recommend at least 16GB RAM and a dedicated GPU for running Isaac Sim and other simulation environments."""
    },
    {
        "source": "module-4-vla-humanoids/index.mdx",
        "content": """Vision-Language-Action (VLA) models represent the cutting edge of robotics AI. These models combine computer vision, natural language understanding, and action prediction to enable robots to understand and execute complex tasks based on visual input and language instructions."""
    }
]

def create_collection():
    """Create or recreate the collection"""
    try:
        client.delete_collection(collection_name=COLLECTION_NAME)
        print(f"Deleted existing collection: {COLLECTION_NAME}")
    except:
        print(f"No existing collection to delete")
    
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=768, distance=Distance.COSINE),
    )
    print(f"Created collection: {COLLECTION_NAME}")

def embed_content(text: str):
    """Embed content with rate limit handling"""
    max_retries = 3
    for attempt in range(max_retries):
        try:
            result = genai.embed_content(
                model="models/text-embedding-004",
                content=text,
                task_type="retrieval_document"
                # title="Textbook Content"
            )
            return result['embedding']
        except Exception as e:
            if attempt < max_retries - 1:
                wait_time = (attempt + 1) * 5
                print(f"Rate limit hit, waiting {wait_time}s...")
                time.sleep(wait_time)
            else:
                print(f"Failed to embed: {e}")
                return None
    return None

def quick_ingest():
    """Quickly ingest sample content for testing"""
    print("Creating collection...")
    create_collection()
    
    points = []
    for idx, item in enumerate(sample_content):
        print(f"Processing {item['source']}...")
        embedding = embed_content(item['content'])
        
        if embedding:
            points.append(PointStruct(
                id=idx,
                vector=embedding,
                payload={"source": item['source'], "content": item['content'], "chunk_index": 0}
            ))
            # Wait between embeddings to avoid rate limits
            time.sleep(3)
    
    if points:
        client.upsert(
            collection_name=COLLECTION_NAME,
            points=points
        )
        print(f"Successfully ingested {len(points)} sample documents!")
        print("Your chatbot is now ready to answer questions about:")
        for item in sample_content:
            print(f"  - {item['source']}")
    else:
        print("❌ Failed to ingest documents due to rate limits")

if __name__ == "__main__":
    if not GEMINI_API_KEY:
        print("Error: GEMINI_API_KEY not set in .env")
    else:
        quick_ingest()
