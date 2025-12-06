from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Gemini API
    gemini_api_key: str
    
    # Qdrant
    qdrant_url: str
    qdrant_api_key: str
    
    # Database
    database_url: str
    
    # App
    environment: str = "development"
    cors_origins: str = "http://localhost:3000"
    
    # Rate limiting
    rate_limit_per_minute: int = 10
    
    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.cors_origins.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
