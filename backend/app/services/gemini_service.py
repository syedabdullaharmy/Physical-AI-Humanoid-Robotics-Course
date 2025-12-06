import google.generativeai as genai
from app.config import settings
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

# Configure Gemini
genai.configure(api_key=settings.gemini_api_key)


class GeminiService:
    """Service for interacting with Google Gemini API"""
    
    def __init__(self):
        self.chat_model = genai.GenerativeModel('gemini-2.0-flash-exp')
        self.embedding_model = 'models/text-embedding-004'
    
    async def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding vector for text"""
        try:
            result = genai.embed_content(
                model=self.embedding_model,
                content=text,
                task_type="retrieval_document"
            )
            return result['embedding']
        except Exception as e:
            logger.error(f"Embedding generation failed: {e}")
            raise
    
    async def generate_query_embedding(self, query: str) -> List[float]:
        """Generate embedding for search query"""
        try:
            result = genai.embed_content(
                model=self.embedding_model,
                content=query,
                task_type="retrieval_query"
            )
            return result['embedding']
        except Exception as e:
            logger.error(f"Query embedding generation failed: {e}")
            raise
    
    async def chat(
        self,
        query: str,
        context: str,
        chat_history: List[Dict[str, str]] = None
    ) -> str:
        """Generate chat response with context"""
        try:
            system_prompt = """You are an expert instructor for Physical AI and Humanoid Robotics.
Your role is to help students learn about ROS 2, digital twins, NVIDIA Isaac Sim, and Vision-Language-Action models for humanoid robots.

Guidelines:
- Provide clear, accurate, and helpful explanations
- Use the provided context to answer questions
- Cite sources when referencing specific chapters or sections
- If you're unsure, say so and suggest where to find more information
- Keep responses concise but comprehensive
- Use code examples when helpful
- Adapt explanations to the user's background level

Context from textbook:
{context}

Answer the user's question based on this context."""
            
            prompt = system_prompt.format(context=context) + f"\n\nUser question: {query}"
            
            response = self.chat_model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7,
                    max_output_tokens=1024,
                )
            )
            
            return response.text
        except Exception as e:
            logger.error(f"Chat generation failed: {e}")
            raise
    
    async def personalize_content(
        self,
        content: str,
        user_profile: Dict[str, Any]
    ) -> str:
        """Personalize content based on user profile"""
        try:
            software_bg = user_profile.get('software_background', 'unknown')
            hardware_bg = user_profile.get('hardware_background', 'unknown')
            hardware_setup = user_profile.get('hardware_setup', 'unknown')
            
            prompt = f"""Adapt the following educational content for a learner with this background:
- Software experience: {software_bg}
- Hardware experience: {hardware_bg}
- Hardware setup: {hardware_setup}

Guidelines for adaptation:
- If beginner in programming: Add more code explanations and link to Python resources
- If no robotics experience: Expand hardware concepts and add visual aids
- If using Digital Twin: Emphasize Gazebo/Unity examples
- If using Jetson: Highlight edge optimization and power constraints
- If using Cloud: Focus on scalable architectures

Original content:
{content}

Provide the adapted version that maintains technical accuracy while being more accessible to this learner."""
            
            response = self.chat_model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7,
                    max_output_tokens=2048,
                )
            )
            
            return response.text
        except Exception as e:
            logger.error(f"Personalization failed: {e}")
            raise
    
    async def translate_to_urdu(self, content: str) -> str:
        """Translate content to Urdu while preserving technical terms"""
        try:
            prompt = f"""Translate the following technical content to Urdu.

Important rules:
1. Keep ALL technical terms in English (ROS 2, Gazebo, NVIDIA Isaac Sim, Python, etc.)
2. Keep ALL code blocks exactly as they are in English
3. Translate explanations and descriptions to natural Urdu
4. Use mixed script (Urdu text with embedded English technical terms) - this is common in Pakistani technical education
5. Maintain the same formatting and structure

Content to translate:
{content}

Provide the Urdu translation following these rules."""
            
            response = self.chat_model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.5,
                    max_output_tokens=2048,
                )
            )
            
            return response.text
        except Exception as e:
            logger.error(f"Translation failed: {e}")
            raise


# Singleton instance
gemini_service = GeminiService()
