from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routers import chat, personalize, translate

app = FastAPI(
    title="Physical AI Textbook API",
    description="RAG chatbot API for Physical AI & Humanoid Robotics Textbook",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(personalize.router, prefix="/api/personalize", tags=["personalize"])
app.include_router(translate.router, prefix="/api/translate", tags=["translate"])


@app.get("/")
async def root():
    return {
        "message": "Physical AI Textbook API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
