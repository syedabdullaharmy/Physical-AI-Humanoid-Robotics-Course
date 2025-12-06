from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
import os
import google.generativeai as genai
from qdrant_client import QdrantClient
from dotenv import load_dotenv

from pathlib import Path

# Load .env from current or parent directory
env_path = Path(__file__).parent / '.env'
if not env_path.exists():
    env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# Configuration
QDRANT_PATH = os.path.join(os.path.dirname(__file__), "qdrant_data")
QDRANT_URL = os.getenv("QDRANT_URL", None)
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
COLLECTION_NAME = "textbook_rag"

# Initialize
# Initialize
genai.configure(api_key=GEMINI_API_KEY)

if QDRANT_URL and QDRANT_URL != ":memory:":
    client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
else:
    # Use local disk persistence specific to this backend folder
    print(f"Using local Qdrant storage at: {QDRANT_PATH}")
    client = QdrantClient(path=QDRANT_PATH)

app = FastAPI()

# Add CORS
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    context: str = "" # Selected text from UI

def get_embedding(text: str):
    try:
        result = genai.embed_content(
            model="models/text-embedding-004",
            content=text,
            task_type="retrieval_query"
            # title="Query" # Not supported for retrieval_query
        )
        return result['embedding']
    except Exception as e:
        print(f"Embedding error: {e}")
        return []

def retrieve_context(query: str, limit: int = 5):
    try:
        # Check if collection exists and has data
        try:
            collection_info = client.get_collection(COLLECTION_NAME)
            if collection_info.points_count == 0:
                print("Warning: Collection is empty, skipping retrieval")
                return []
        except Exception as e:
            print(f"Collection check error: {e}")
            return []
        
        embedding = get_embedding(query)
        if not embedding:
            return []
        
        hits = client.search(
            collection_name=COLLECTION_NAME,
            query_vector=embedding,
            limit=limit
        )
        return [hit.payload for hit in hits]
    except Exception as e:
        print(f"Retrieval error: {e}")
        return []

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        user_query = request.message
        selected_context = request.context
        
        if not user_query.strip():
            return {"response": "Please provide a question."}
        
        # Validate input length
        if len(user_query) > 2000:
            return {"response": "Your question is too long. Please keep it under 2000 characters."}
        
        # Retrieve context from vector database
        retrieved_docs = retrieve_context(user_query, limit=5)
        
        if not retrieved_docs:
            # Fallback if no context found
            prompt = f"""You are an advanced AI Tutor for the Physical AI & Humanoid Robotics Textbook.
            
The user asked: {user_query}

Unfortunately, I couldn't find specific content from the textbook related to this question.
However, I can provide a general answer based on my knowledge of robotics and AI.

Instructions:
1. Provide a helpful, educational response related to Physical AI, Humanoid Robotics, ROS 2, Digital Twins, Isaac Sim, or VLA models.
2. Be clear that this is general knowledge, not from the specific textbook content.
3. Keep your response concise but informative (2-3 paragraphs).
4. Use bullet points or numbered lists when appropriate.
5. Be encouraging and suggest the user check the textbook for more specific information.

Answer:"""
        else:
            # Build context with source information
            doc_context = "\n\n".join([
                f"[Source: {d.get('source', 'Unknown')}]\n{d.get('content', '')}" 
                for d in retrieved_docs
            ])
            
            # Construct enhanced prompt
            prompt = f"""You are an advanced AI Tutor for the Physical AI & Humanoid Robotics Textbook.
Your goal is to provide accurate, educational, and easy-to-understand answers based on the provided course material.

INSTRUCTIONS:
1. **Primary Source**: Use the Context below as your primary source of truth.
2. **Relevance Check**: If the user's question correlates with the context, answer it using the context.
3. **Fallback**: If the context is not relevant, acknowledge that and provide general knowledge but mention it's not from the specific textbook.
4. **Pedagogical Approach**: Be encouraging, clear, and educational. Break down complex concepts.
5. **Selected Context Priority**: If there is User Selected Context, pay special attention to it as the user is asking about that specific text.
6. **Formatting**: 
   - Use clear, structured formatting with bullet points or numbered lists when appropriate
   - Use **bold** for key terms
   - Keep responses concise but comprehensive (3-5 paragraphs max)
7. **Code Examples**: If explaining code or technical concepts, provide brief examples when helpful.
8. **Accuracy**: Only provide information you're confident about. If uncertain, say so.

CONTEXT FROM TEXTBOOK:
{doc_context}

USER SELECTED CONTEXT (if any):
{selected_context if selected_context else "None"}

USER QUESTION: 
{user_query}

ANSWER:"""
        
        # Generate response with Gemini
        try:
            model = genai.GenerativeModel(
                'gemini-2.0-flash-lite-preview-02-05',  # Updated to working model
                generation_config={
                    'temperature': 0.7,
                    'top_p': 0.95,
                    'top_k': 40,
                    'max_output_tokens': 1024,
                }
            )
            response = model.generate_content(prompt)
            
            # Validate response
            if not response or not response.text:
                raise Exception("Empty response from AI model")
            
            response_text = response.text.strip()
            
            # Check for blocked or filtered responses
            if hasattr(response, 'prompt_feedback') and response.prompt_feedback.block_reason:
                return {
                    "response": "I apologize, but I cannot provide a response to that question. Please try rephrasing or ask a different question about the course material."
                }
            
            return {"response": response_text}
            
        except Exception as model_error:
            print(f"Model generation error: {str(model_error)}")
            return {
                "response": f"I encountered an issue generating a response. Error details: {str(model_error)}",
                "error": str(model_error)
            }
        
    except Exception as e:
        print(f"Chat error: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            "response": "I apologize, but I encountered an unexpected error processing your question. Please try again or contact support if the issue persists.",
            "error": str(e)
        }


class PersonalizeRequest(BaseModel):
    user_profile: dict
    content: str # The chapter content or summary

@app.post("/personalize")
async def personalize(request: PersonalizeRequest):
    profile = request.user_profile
    content = request.content
    
    prompt = f"""You are an expert tutor. Personalize the following course content introduction for a student with this profile:
    Software Experience: {profile.get('softwareBg')}
    Hardware Experience: {profile.get('hardwareBg')}
    Name: {profile.get('name')}
    
    Content to Personalize (Intro/Summary):
    {content[:2000]} # Limit to first 2000 chars for speed
    
    Output a personalized welcome message and a summary of why this chapter matters to them specifically.
    """
    
    try:
        model = genai.GenerativeModel('gemini-2.0-flash-lite-preview-02-05')
        response = model.generate_content(prompt)
        return {"response": response.text}
    except Exception as e:
        return {"response": f"Error: {e}"}

class TranslateRequest(BaseModel):
    content: str
    target_language: str = "Urdu"

@app.post("/translate")
async def translate(request: TranslateRequest):
    content = request.content
    
    # Translate the first chunk or summary
    prompt = f"""Translate the following technical text into {request.target_language}. Maintain technical accuracy but use appropriate local terminology where fit.
    
    Text:
    {content[:3000]}
    """
    
    try:
        model = genai.GenerativeModel('gemini-2.0-flash-lite-preview-02-05')
        response = model.generate_content(prompt)
        return {"response": response.text}
    except Exception as e:
        return {"response": f"Error: {e}"}
