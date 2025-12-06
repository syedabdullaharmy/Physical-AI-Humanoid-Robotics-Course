import os
from qdrant_client import QdrantClient
from dotenv import load_dotenv
from pathlib import Path

# Load .env from current or parent directory
env_path = Path(__file__).parent / '.env'
if not env_path.exists():
    env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

QDRANT_PATH = os.path.join(os.path.dirname(__file__), "qdrant_data")
QDRANT_URL = os.getenv("QDRANT_URL", None)
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", "")
COLLECTION_NAME = "textbook_rag"

# Initialize client
if QDRANT_URL and QDRANT_URL != ":memory:":
    client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
    print(f"Using Qdrant Cloud: {QDRANT_URL}")
else:
    client = QdrantClient(path=QDRANT_PATH)
    print(f"Using local Qdrant storage at: {QDRANT_PATH}")

try:
    # Check if collection exists
    collections = client.get_collections()
    print(f"\nAvailable collections: {[c.name for c in collections.collections]}")
    
    if COLLECTION_NAME in [c.name for c in collections.collections]:
        # Get collection info
        collection_info = client.get_collection(COLLECTION_NAME)
        print(f"\nCollection '{COLLECTION_NAME}' exists!")
        print(f"Points count: {collection_info.points_count}")
        print(f"Vector size: {collection_info.config.params.vectors.size}")
        
        if collection_info.points_count > 0:
            print("\n✅ Collection has data - chatbot should work!")
        else:
            print("\n⚠️ Collection exists but is EMPTY - need to run ingestion!")
    else:
        print(f"\n❌ Collection '{COLLECTION_NAME}' does NOT exist - need to run ingestion!")
        
except Exception as e:
    print(f"\n❌ Error checking Qdrant: {e}")
