"""
Content ingestion script for Physical AI textbook
Parses markdown files and ingests them into Qdrant vector database
"""
import os
import sys
import asyncio
import re
from pathlib import Path
from typing import List, Dict, Any

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from app.services.rag_service import rag_service


def chunk_markdown(content: str, max_tokens: int = 1000) -> List[Dict[str, Any]]:
    """
    Chunk markdown content intelligently
    - Split by headers
    - Preserve code blocks
    - Add overlap between chunks
    """
    chunks = []
    
    # Split by headers (##)
    sections = re.split(r'\n##\s+', content)
    
    for i, section in enumerate(sections):
        if not section.strip():
            continue
        
        # Extract section title
        lines = section.split('\n')
        title = lines[0] if i > 0 else "Introduction"
        section_content = '\n'.join(lines[1:]) if i > 0 else section
        
        # Simple token estimation (rough: 1 token ≈ 4 characters)
        estimated_tokens = len(section_content) // 4
        
        if estimated_tokens <= max_tokens:
            chunks.append({
                "text": f"## {title}\n{section_content}",
                "section": title
            })
        else:
            # Split large sections by paragraphs
            paragraphs = section_content.split('\n\n')
            current_chunk = f"## {title}\n"
            
            for para in paragraphs:
                if len(current_chunk + para) // 4 <= max_tokens:
                    current_chunk += para + "\n\n"
                else:
                    if current_chunk.strip():
                        chunks.append({
                            "text": current_chunk.strip(),
                            "section": title
                        })
                    current_chunk = f"## {title}\n{para}\n\n"
            
            if current_chunk.strip():
                chunks.append({
                    "text": current_chunk.strip(),
                    "section": title
                })
    
    return chunks


async def ingest_file(file_path: Path, module: str, chapter: str):
    """Ingest a single markdown file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove personal names
        content = re.sub(r'Ameen\s+Alam', 'Panaversity', content, flags=re.IGNORECASE)
        content = re.sub(r'github\.com/Ameen-Alam', 'github.com/panaversity', content)
        
        # Chunk content
        chunks = chunk_markdown(content)
        
        print(f"Processing {file_path.name}: {len(chunks)} chunks")
        
        # Ingest each chunk
        for i, chunk in enumerate(chunks):
            metadata = {
                "module": module,
                "chapter": chapter,
                "section": chunk.get("section", ""),
                "file": file_path.name,
                "chunk_index": i
            }
            
            await rag_service.add_content(
                text=chunk["text"],
                metadata=metadata
            )
        
        print(f"✓ Ingested {file_path.name}")
    
    except Exception as e:
        print(f"✗ Failed to ingest {file_path.name}: {e}")


async def ingest_directory(docs_dir: Path):
    """Ingest all markdown files from docs directory"""
    if not docs_dir.exists():
        print(f"Error: Directory {docs_dir} does not exist")
        return
    
    # Find all markdown files
    md_files = list(docs_dir.rglob("*.md"))
    
    if not md_files:
        print(f"No markdown files found in {docs_dir}")
        return
    
    print(f"Found {len(md_files)} markdown files")
    print("Starting ingestion...\n")
    
    for md_file in md_files:
        # Determine module and chapter from path
        relative_path = md_file.relative_to(docs_dir)
        parts = relative_path.parts
        
        module = parts[0] if len(parts) > 1 else "general"
        chapter = md_file.stem
        
        await ingest_file(md_file, module, chapter)
    
    print(f"\n✓ Ingestion complete! Processed {len(md_files)} files")


async def main():
    """Main ingestion function"""
    # Get docs directory
    docs_dir = Path(__file__).parent.parent.parent / "frontend" / "docs"
    
    if not docs_dir.exists():
        print(f"Error: Docs directory not found at {docs_dir}")
        print("Please ensure the frontend/docs directory exists with markdown content")
        return
    
    print("=" * 60)
    print("Physical AI Textbook - Content Ingestion")
    print("=" * 60)
    print(f"Docs directory: {docs_dir}")
    print()
    
    await ingest_directory(docs_dir)


if __name__ == "__main__":
    asyncio.run(main())
