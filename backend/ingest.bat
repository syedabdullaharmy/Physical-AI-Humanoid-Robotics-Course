@echo off
echo ========================================
echo Physical AI Textbook - Content Ingestion
echo ========================================
echo.

REM Activate virtual environment
call venv\Scripts\activate

REM Check if .env exists
if not exist ".env" (
    echo ERROR: .env file not found!
    echo Please set up your .env file first.
    pause
    exit /b 1
)

echo.
echo Starting content ingestion...
echo This will:
echo   1. Parse markdown files from ../frontend/docs
echo   2. Chunk content intelligently
echo   3. Generate embeddings with Gemini
echo   4. Store in Qdrant vector database
echo.

python scripts\ingest_content.py

echo.
echo Ingestion complete!
pause
