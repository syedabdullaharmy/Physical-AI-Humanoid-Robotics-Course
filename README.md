# Physical AI & Humanoid Robotics Textbook

An AI-native interactive textbook for learning Physical AI and Humanoid Robotics, featuring a powerful RAG chatbot powered by Google Gemini.

## 🚀 Features

### Core Features
- ✅ **Comprehensive Content**: 13-week course covering ROS 2, Digital Twins, NVIDIA Isaac Sim, and VLA Models
- ✅ **AI-Powered RAG Chatbot**: Ask questions and get instant, context-aware answers using Google Gemini
- ✅ **Text Selection Q&A**: Highlight any text and ask the AI about it
- ✅ **Beautiful UI**: Modern, responsive Docusaurus-based interface

### Bonus Features
- 🔐 **Authentication**: Better-Auth integration with user profiles
- ✨ **Personalization**: Content adapted to your background and experience level
- 🌐 **Urdu Translation**: Full course available in Urdu with technical terms preserved
- 🧠 **Strong RAG**: Multi-stage retrieval with Qdrant vector search and Postgres metadata filtering

## 🏗️ Architecture

### Frontend
- **Framework**: Docusaurus 3.6.3
- **Language**: TypeScript
- **Styling**: CSS Modules
- **Deployment**: Netlify

### Backend
- **Framework**: FastAPI
- **AI**: Google Gemini API (gemini-2.0-flash-exp, text-embedding-004)
- **Vector DB**: Qdrant Cloud (free tier)
- **Database**: Neon Serverless Postgres (free tier)
- **Deployment**: Railway/Render

## 📦 Installation

### Prerequisites
- Node.js 18+ and npm
- Python 3.11+
- Git

### Frontend Setup

```bash
cd frontend
npm install
npm start
```

The site will be available at `http://localhost:3000`

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys

# Run the server
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### Content Ingestion

After setting up the backend, ingest the textbook content:

```bash
cd backend
python scripts/ingest_content.py
```

## 🔑 Environment Variables

### Backend (.env)

```env
# Gemini API
GEMINI_API_KEY=your_gemini_api_key_here

# Qdrant Cloud
QDRANT_URL=your_qdrant_url_here
QDRANT_API_KEY=your_qdrant_api_key_here

# Neon Postgres
DATABASE_URL=postgresql://user:password@host/database

# App Settings
ENVIRONMENT=development
CORS_ORIGINS=http://localhost:3000
```

### Frontend (.env.local)

```env
REACT_APP_API_URL=http://localhost:8000
```

## 🚢 Deployment

### Deploy to Netlify (Frontend)

1. Connect your GitHub repository to Netlify
2. Configure build settings:
   - Build command: `cd frontend && npm run build`
   - Publish directory: `frontend/build`
3. Add environment variables in Netlify dashboard
4. Deploy!

### Deploy Backend (Railway)

1. Create a new project on Railway
2. Connect your GitHub repository
3. Add environment variables
4. Railway will auto-deploy from `backend/`

## 📚 Project Structure

```
physical-ai-textbook/
├── frontend/                 # Docusaurus application
│   ├── docs/                # Textbook content
│   ├── src/
│   │   ├── components/      # React components
│   │   │   └── ChatWidget/  # AI chatbot
│   │   └── theme/           # Theme customization
│   └── docusaurus.config.ts
│
├── backend/                  # FastAPI application
│   ├── app/
│   │   ├── main.py          # FastAPI app
│   │   ├── config.py        # Settings
│   │   ├── routers/         # API endpoints
│   │   │   ├── chat.py
│   │   │   ├── personalize.py
│   │   │   └── translate.py
│   │   └── services/        # Business logic
│   │       ├── gemini_service.py
│   │       └── rag_service.py
│   ├── scripts/
│   │   └── ingest_content.py
│   └── requirements.txt
│
└── specs/                    # Spec-Kit Plus artifacts
    ├── 000-constitution/
    └── 001-textbook-project/
```

## 🎯 Usage

### Using the Chatbot

1. Click the chat button in the bottom-right corner
2. Ask any question about the textbook content
3. Get instant, AI-powered answers with citations

### Text Selection Q&A

1. Highlight any text on the page
2. Click "Ask AI" (or right-click)
3. Ask a question about the selected text
4. Get focused, context-aware explanations

### Personalization

1. Sign up and complete your profile
2. Navigate to any chapter
3. Click "Personalize this chapter"
4. Get content adapted to your background

### Translation

1. Navigate to any chapter
2. Click "اردو میں پڑھیں" (Read in Urdu)
3. View the chapter in Urdu with technical terms preserved

## 🧪 Testing

### Backend Tests

```bash
cd backend
pytest
```

### Frontend Tests

```bash
cd frontend
npm test
```

## 🤝 Contributing

This project was built using Spec-Kit Plus methodology:

1. Constitution → Specification → Plan → Tasks → Implementation
2. All features are spec-driven
3. Reusable subagents and skills

See `specs/` directory for detailed specifications.

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- Built for the Panaversity Hackathon
- Powered by Google Gemini API
- Content structure inspired by industry best practices
- Special thanks to Panaversity, PIAIC, and GIAIC communities

## 📞 Support

- **Chatbot**: Use the built-in AI assistant
- **Issues**: GitHub Issues
- **Community**: [Panaversity](https://panaversity.org)

## 🏆 Hackathon Submission

This project achieves:
- ✅ Base requirements (100 pts): Docusaurus + Strong RAG
- ✅ Better-Auth integration (+50 pts)
- ✅ Content personalization (+50 pts)
- ✅ Urdu translation (+50 pts)
- ✅ Spec-Kit Plus usage (+50 pts)

**Total: 300 points** 🎉

---

Built with ❤️ using Spec-Kit Plus and Claude Code
