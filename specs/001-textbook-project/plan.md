# Implementation Plan: Physical AI & Humanoid Robotics Textbook

## Technology Stack

### Frontend
- **Framework**: Docusaurus 3.6.3
- **Language**: TypeScript 5.x
- **Styling**: Custom CSS with CSS Modules
- **State Management**: React Context API
- **HTTP Client**: Axios
- **Build Tool**: Webpack (via Docusaurus)
- **Deployment**: Netlify

### Backend
- **Framework**: FastAPI 0.115+
- **Language**: Python 3.11+
- **ASGI Server**: Uvicorn
- **Validation**: Pydantic v2
- **Authentication**: Better-Auth integration
- **Deployment**: Railway or Render (containerized)

### Databases
1. **Qdrant Cloud** (Free Tier - 1GB):
   - Vector storage and similarity search
   - Collections: `textbook_chunks`, `user_queries`

2. **Neon Serverless Postgres** (Free Tier):
   - User data, chat history, cached content
   - Version: PostgreSQL 16
   - Extensions: `pg_trgm` for fuzzy search

### AI/ML
- **Google Gemini API**:
  - `gemini-2.0-flash-exp`: Primary chat model
  - `text-embedding-004`: Document embeddings
  - Python SDK: `google-generativeai`

### Authentication
- **Better-Auth**:
  - Email/password authentication
  - OAuth providers: Google, GitHub
  - Session management with cookies
  - CSRF protection built-in

### Development Tools
- **Version Control**: Git + GitHub
- **Package Manager**: 
  - Frontend: npm
  - Backend: Poetry or pip
- **Code Quality**:
  - Frontend: ESLint, Prettier, TypeScript
  - Backend: Ruff, Black, mypy
- **Testing**:
  - Frontend: Jest, React Testing Library
  - Backend: pytest

## Project Structure

```
physical-ai-textbook/
├── frontend/                    # Docusaurus application
│   ├── docs/                   # Textbook content (Markdown)
│   │   ├── intro.md
│   │   ├── setup/
│   │   ├── module-1-ros2/
│   │   ├── module-2-digital-twin/
│   │   ├── module-3-isaac/
│   │   ├── module-4-vla-humanoids/
│   │   ├── capstone/
│   │   └── references/
│   ├── src/
│   │   ├── components/        # React components
│   │   │   ├── ChatWidget/   # RAG chatbot UI
│   │   │   ├── AuthButton/   # Login/signup
│   │   │   ├── PersonalizeButton/
│   │   │   ├── TranslateButton/
│   │   │   ├── TextSelectionMenu/
│   │   │   └── UserProfile/
│   │   ├── pages/
│   │   │   └── index.tsx     # Custom homepage
│   │   ├── css/
│   │   │   └── custom.css
│   │   └── utils/
│   │       ├── api.ts        # API client
│   │       └── auth.ts       # Auth utilities
│   ├── static/
│   │   └── img/
│   ├── docusaurus.config.ts
│   ├── sidebars.ts
│   ├── package.json
│   └── tsconfig.json
│
├── backend/                    # FastAPI application
│   ├── app/
│   │   ├── main.py           # FastAPI app entry
│   │   ├── config.py         # Settings (env vars)
│   │   ├── models/           # Pydantic models
│   │   │   ├── user.py
│   │   │   ├── chat.py
│   │   │   └── content.py
│   │   ├── routers/          # API endpoints
│   │   │   ├── auth.py
│   │   │   ├── chat.py
│   │   │   ├── personalize.py
│   │   │   └── translate.py
│   │   ├── services/         # Business logic
│   │   │   ├── rag_service.py
│   │   │   ├── embedding_service.py
│   │   │   ├── gemini_service.py
│   │   │   └── user_service.py
│   │   ├── db/               # Database
│   │   │   ├── postgres.py   # Neon connection
│   │   │   ├── qdrant.py     # Qdrant connection
│   │   │   └── models.py     # SQLAlchemy models
│   │   └── utils/
│   │       ├── chunking.py   # Content chunking
│   │       └── validators.py
│   ├── scripts/
│   │   └── ingest_content.py # One-time content ingestion
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
│
├── specs/                      # Spec-Kit Plus artifacts
│   ├── 000-constitution/
│   │   └── constitution.md
│   └── 001-textbook-project/
│       ├── spec.md
│       ├── plan.md           # This file
│       └── tasks.md          # Generated next
│
├── .github/
│   └── workflows/
│       ├── frontend-deploy.yml
│       └── backend-deploy.yml
│
├── README.md
└── .gitignore
```

## Architecture Overview

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         User Browser                         │
│  ┌──────────────────────────────────────────────────────┐  │
│  │        Docusaurus Static Site (Netlify CDN)          │  │
│  │  ┌────────────┐  ┌──────────────┐  ┌─────────────┐  │  │
│  │  │  Content   │  │  Chat Widget │  │  Auth UI    │  │  │
│  │  │  Pages     │  │              │  │             │  │  │
│  │  └────────────┘  └──────────────┘  └─────────────┘  │  │
│  └──────────────────────────────────────────────────────┘  │
└───────────────────────┬─────────────────────────────────────┘
                        │ HTTPS REST API
┌───────────────────────▼─────────────────────────────────────┐
│               FastAPI Backend (Railway/Render)               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                    API Endpoints                      │  │
│  │  /chat  │  /auth  │  /personalize  │  /translate    │  │
│  └────┬────────────┬──────────┬──────────────┬──────────┘  │
│       │            │          │              │              │
│  ┌────▼────────┬───▼──────┬───▼──────┬───────▼──────────┐  │
│  │ RAG Service │ Gemini   │ User     │ Better-Auth      │  │
│  │             │ Service  │ Service  │ Integration      │  │
│  └────┬────────┴──────────┴──┬───────┴──────────────────┘  │
└───────┼────────────────────────┼─────────────────────────────┘
        │                        │
┌───────▼────────┐      ┌────────▼────────┐
│  Qdrant Cloud  │      │  Neon Postgres  │
│  (Vectors)     │      │  (Relational)   │
└────────────────┘      └─────────────────┘
        │
┌───────▼────────────────────────┐
│     Google Gemini API          │
│  - Chat Generation             │
│  - Text Embeddings             │
└────────────────────────────────┘
```

### RAG Pipeline Details

```
User Query: "How do I set up ROS 2 on Ubuntu?"
    │
    ▼
1. Query Preprocessing
   - Normalize text
   - Extract intent (setup question)
   - Identify entities (ROS 2, Ubuntu)
    │
    ▼
2. Embedding Generation (Gemini)
   - Generate query embedding vector
    │
    ▼
3. Retrieval (Multi-stage)
   ┌────────────────────────────────┐
   │ Stage 1: Vector Search         │
   │ - Qdrant similarity search     │
   │ - Top 20 candidates            │
   │ - Filter by module/chapter     │
   └────────────────────────────────┘
            │
   ┌────────▼────────────────────────┐
   │ Stage 2: Keyword Search         │
   │ - Postgres full-text search    │
   │ - Match: "ROS 2", "setup",     │
   │   "Ubuntu"                      │
   │ - Top 10 candidates             │
   └─────────────────────────────────┘
            │
   ┌────────▼────────────────────────┐
   │ Stage 3: Metadata Filtering     │
   │ - User's hardware path          │
   │ - Current module context        │
   │ - Difficulty level match        │
   └─────────────────────────────────┘
            │
   ┌────────▼────────────────────────┐
   │ Stage 4: Re-ranking             │
   │ - Combine vector + keyword      │
   │ - Boost code examples           │
   │ - Recency factor                │
   │ - Top 5 final chunks            │
   └─────────────────────────────────┘
    │
    ▼
4. Context Assembly
   - Retrieved chunks (top 5)
   - User profile info
   - Chat history (last 3 turns)
   - Chapter context (if on page)
    │
    ▼
5. Prompt Construction
   System: "You are an expert Physical AI instructor..."
   Context: [Retrieved chunks with citations]
   History: [Previous Q&A]
   Query: "How do I set up ROS 2 on Ubuntu?"
    │
    ▼
6. Generation (Gemini)
   - Stream response token-by-token
   - Extract citations
   - Confidence score calculation
    │
    ▼
7. Response Formatting
   {
     "answer": "To set up ROS 2 on Ubuntu...",
     "citations": [
       {"chapter": "Module 1", "section": "ROS 2 Setup", "url": "/docs/module-1-ros2/setup"}
     ],
     "confidence": "high"
   }
    │
    ▼
8. Caching & Analytics
   - Store Q&A in chat_history
   - Log query for analytics
   - Update user interaction stats
```

## Implementation Phases

### Phase 1: Foundation (Days 1-2)
**Goal**: Basic Docusaurus site with content

#### Tasks:
1. Initialize Docusaurus project
   - `npx create-docusaurus@latest frontend classic --typescript`
   - Configure `docusaurus.config.ts`
   - Set up custom homepage

2. Migrate content from reference repository
   - Clone Ameen-Alam repository
   - Remove personal names/references
   - Update links to Panaversity org
   - Organize into module folders

3. Configure navigation
   - Create `sidebars.ts` with nested structure
   - Add module landing pages
   - Set up breadcrumbs

4. Style customization
   - Modern color palette
   - Custom CSS for dashboard homepage
   - Card components for modules
   - Dark mode support

5. Deploy to Netlify
   - Connect GitHub repository
   - Configure build settings
   - Set up custom domain (if available)

**Deliverable**: Live Docusaurus site with all content, deployed to Netlify

### Phase 2: RAG Chatbot Backend (Days 3-5)
**Goal**: Functional RAG system with strong retrieval

#### Tasks:
1. Set up backend infrastructure
   - Initialize FastAPI project
   - Configure Poetry/requirements.txt
   - Create `.env.example`
   - Set up Dockerfile

2. Database setup
   - **Neon Postgres**:
     - Create free tier account
     - Define schema (users, chat_history, etc.)
     - Set up SQLAlchemy models
     - Create migrations
   - **Qdrant Cloud**:
     - Create free tier account
     - Define collections schema
     - Set up Python client

3. Content ingestion pipeline
   - Parse Markdown files from docs/
   - Chunk content intelligently:
     - By section headers
     - Max 1000 tokens
     - Overlap 100 tokens
     - Keep code blocks intact
   - Generate embeddings with Gemini
   - Store vectors in Qdrant
   - Store metadata in Postgres

4. RAG service implementation
   - Query embedding generation
   - Multi-stage retrieval:
     - Vector search (Qdrant)
     - Keyword search (Postgres FTS)
     - Metadata filtering
     - Re-ranking algorithm
   - Context assembly
   - Prompt template engineering
   - Gemini API integration
   - Response streaming

5. Chat API endpoints
   - `POST /api/chat/query`: Main chat endpoint
   - `GET /api/chat/history`: Get chat history
   - `DELETE /api/chat/clear`: Clear history
   - WebSocket for streaming (optional)

6. Testing
   - Unit tests for chunking logic
   - Integration tests for retrieval
   - End-to-end tests for chat flow
   - Evaluate retrieval quality (manual)

**Deliverable**: FastAPI backend with working RAG, deployed to Railway/Render

### Phase 3: Frontend Chat Integration (Days 6-7)
**Goal**: Beautiful, functional chat widget in Docusaurus

#### Tasks:
1. Chat widget component
   - Minimized button (bottom-right corner)
   - Expandable chat panel
   - Message history display
   - Input with send button
   - Loading states
   - Error handling

2. API integration
   - Create API client (`src/utils/api.ts`)
   - Connect to backend endpoints
   - Handle authentication headers
   - Implement retry logic

3. Text selection Q&A
   - Detect text selection on page
   - Show floating "Ask AI" button
   - Open chat with selected text as context
   - Highlight source text in chat

4. Chat UX improvements
   - Markdown rendering in responses
   - Citation links to chapters
   - Copy message button
   - Clear chat option
   - Typing indicators

5. Performance optimization
   - Debounce API calls
   - Cache responses (session storage)
   - Lazy load chat component

**Deliverable**: Fully functional chatbot integrated in Docusaurus site

### Phase 4: Authentication (Days 8-9)
**Goal**: Secure user authentication with Better-Auth

#### Tasks:
1. Better-Auth setup
   - Install Better-Auth in frontend
   - Configure OAuth providers (Google, GitHub)
   - Set up email/password auth
   - Create auth endpoints in backend

2. User profile system
   - Signup flow with background questions
   - User profile model (Postgres)
   - Profile page component
   - Edit profile functionality

3. Protected routes
   - Auth middleware in backend
   - Protected API endpoints
   - Conditional rendering in frontend
   - Redirect logic

4. Integration with RAG
   - Pass user context to RAG service
   - Personalized retrieval based on profile
   - Chat history tied to user ID

**Deliverable**: Working authentication with user profiles

### Phase 5: Personalization (Days 10-11)
**Goal**: Per-chapter content personalization

#### Tasks:
1. Personalization service
   - Backend endpoint: `POST /api/personalize`
   - Input: chapter_id, user_profile
   - Gemini prompt engineering for adaptation
   - Cache personalized content (Postgres)

2. Frontend button component
   - "Personalize for me" button at chapter start
   - Loading state while generating
   - Toggle between original/personalized
   - Visual indicator of personalized view

3. Personalization logic
   - Analyze user background
   - Adapt code complexity
   - Add/remove explanations
   - Suggest relevant resources
   - Adjust terminology

4. Testing personalization quality
   - Test with different user profiles
   - Validate adaptations make sense
   - Ensure technical accuracy

**Deliverable**: Working personalization feature

### Phase 6: Urdu Translation (Days 12-13)
**Goal**: High-quality Urdu translation

#### Tasks:
1. Translation service
   - Backend endpoint: `POST /api/translate`
   - Input: chapter_id, language="ur"
   - Gemini prompt for translation
   - Preserve technical terms
   - Cache translations (Postgres)

2. Frontend button component
   - "اردو میں پڑھیں" button
   - RTL layout for Urdu content
   - Toggle between English/Urdu
   - Load Urdu fonts (Noto Nastaliq Urdu)

3. RTL styling
   - CSS for right-to-left layout
   - Keep code blocks LTR
   - Mixed direction handling
   - Navigation adjustments

4. Translation quality
   - Test with native Urdu speakers
   - Verify technical terms preserved
   - Ensure readability

**Deliverable**: Working Urdu translation feature

### Phase 7: Polish & Optimization (Days 14-15)
**Goal**: Production-ready quality

#### Tasks:
1. Performance optimization
   - Lighthouse audit
   - Optimize images
   - Code splitting
   - Lazy loading
   - CDN configuration

2. Accessibility audit
   - Keyboard navigation
   - Screen reader testing
   - Color contrast fixes
   - ARIA labels

3. Error handling
   - User-friendly error messages
   - Fallback UI for API failures
   - Offline detection
   - Rate limit messaging

4. Documentation
   - README with setup instructions
   - API documentation
   - Deployment guide
   - User guide

5. Final testing
   - Cross-browser testing
   - Mobile responsiveness
   - Chat functionality
   - Auth flows
   - Personalization
   - Translation

**Deliverable**: Polished, production-ready application

### Phase 8: Demo & Submission (Day 16)
**Goal**: Compelling demo and submission

#### Tasks:
1. Create demo video
   - Script the demo (< 90 seconds)
   - Screen recording with voice-over
   - Show all key features:
     - Navigation through textbook
     - Ask chatbot a question
     - Text selection Q&A
     - Personalization demo
     - Urdu translation demo
     - Signup/signin flow
   - Edit video for clarity
   - Upload to YouTube/Vimeo

2. Prepare submission
   - Clean up GitHub repository
   - Write compelling README
   - Add screenshots to README
   - Tag final release
   - Test all public URLs

3. Fill out submission form
   - GitHub repository link
   - Deployed site link (Netlify)
   - Demo video link
   - WhatsApp number

4. Prepare for presentation (if invited)
   - Create slides
   - Practice pitch
   - Prepare for Q&A
   - Test demo environment

**Deliverable**: Submitted project, ready for judging

## Key Technical Decisions

### Decision 1: Backend Hosting
**Options**:
1. Netlify Functions (serverless)
2. Railway (containerized, $5/month after free tier)
3. Render (containerized, free tier with spin-down)

**Choice**: **Railway** ($5/month if needed)
**Rationale**:
- Persistent container (no cold starts)
- Good for FastAPI with long-running process
- Qdrant/Neon connections stay warm
- Easy deployment with GitHub integration

### Decision 2: Styling Approach
**Options**:
1. Tailwind CSS
2. CSS Modules
3. Styled Components

**Choice**: **CSS Modules** with custom CSS
**Rationale**:
- Docusaurus has good CSS Modules support
- More control over styling
- Avoid Tailwind bloat
- Easier for RTL layout customization

### Decision 3: Chat UI
**Options**:
1. Modal overlay
2. Side panel
3. Bottom-right widget

**Choice**: **Bottom-right widget** (expandable)
**Rationale**:
- Non-intrusive
- Allows reading + chatting simultaneously
- Mobile-friendly
- Industry standard (Intercom-style)

### Decision 4: Caching Strategy
**Personalization & Translation**:
- Cache in Postgres by `(chapter_id, user_id)` for personalization
- Cache in Postgres by `(chapter_id, language)` for translation
- TTL: 30 days (re-generate if stale)

**Chat Responses**:
- No caching (each conversation is contextual)
- Store history for user reference

### Decision 5: Gemini API Usage
**Embedding Model**: `text-embedding-004`
- 768 dimensions
- Good performance/cost balance

**Chat Model**: `gemini-2.0-flash-exp`
- Fast responses
- Good instruction following
- Supports long context

**Parameters**:
- Temperature: 0.7 (helpful but focused)
- Max output tokens: 1024 (adjustable)
- Safety settings: Default (block harmful content)

## Security Considerations

1. **API Keys**: 
   - Never commit to Git
   - Use environment variables
   - Backend validates keys on startup

2. **User Input**:
   - Sanitize all inputs
   - Validate with Pydantic
   - Prevent SQL injection (parameterized queries)
   - Prevent XSS (sanitize markdown rendering)

3. **Rate Limiting**:
   - Per-user: 10 chat requests/minute
   - Global: 1000 requests/hour
   - Prevent abuse of Gemini API

4. **Authentication**:
   - HTTPS only
   - Secure cookie settings
   - CSRF protection (Better-Auth)
   - Password hashing (Better-Auth)

5. **CORS**:
   - Allow only Netlify domain
   - Credentials allowed for auth cookies

## Cost Estimation

### Gemini API
- **Embeddings**: 
  - ~500 chunks × 1000 tokens = 500k tokens
  - Embedding cost: ~$0.0125 for 500k tokens
  - Ongoing: 100 queries/day × 200 tokens = 20k tokens/day ~ $0.001/day

- **Chat**:
  - 100 queries/day × 2k tokens (input+output) = 200k tokens/day
  - Cost: ~$0.005/day

**Total Gemini**: ~$0.50/month for moderate usage

### Qdrant Cloud
- Free tier: 1GB storage, 100k vectors
- **Cost**: $0

### Neon Postgres
- Free tier: 0.5GB storage, 500 hours compute/month
- **Cost**: $0

### Netlify
- Free tier: 100GB bandwidth
- **Cost**: $0

### Railway (Backend)
- Free trial: $5 credit
- After: ~$5-10/month for small instance
- **Cost**: $5-10/month (or use Render free tier)

**Total Monthly Cost**: ~$5-10 (or $0 if using free tiers)

## Risk Mitigation

### Risk 1: Gemini API Rate Limits
**Mitigation**:
- Implement exponential backoff
- Queue requests if needed
- Cache embeddings for content (one-time generation)
- Show graceful error to user

### Risk 2: Poor Retrieval Quality
**Mitigation**:
- Test retrieval with diverse queries
- Tune chunk size and overlap
- Adjust re-ranking algorithm
- Add fallback to keyword search only

### Risk 3: Slow Response Times
**Mitigation**:
- Stream responses token-by-token
- Show typing indicator immediately
- Optimize vector search (limit top-k)
- Use CDN for static assets

### Risk 4: Translation Accuracy
**Mitigation**:
- Test with native speakers
- Review sensitive content manually
- Allow users to report issues
- Keep original always accessible

### Risk 5: Deployment Issues
**Mitigation**:
- Deploy early and often
- Test in staging environment
- Use environment variables correctly
- Have rollback plan

## Timeline Summary

| Phase | Days | Deliverable |
|-------|------|-------------|
| Foundation | 1-2 | Docusaurus site with content |
| RAG Backend | 3-5 | FastAPI + RAG working |
| Chat Frontend | 6-7 | Chat widget integrated |
| Authentication | 8-9 | Better-Auth working |
| Personalization | 10-11 | Content personalization |
| Translation | 12-13 | Urdu translation |
| Polish | 14-15 | Production-ready |
| Demo | 16 | Submitted project |

**Total**: 16 days for full implementation

**Aggressive Timeline**: Can compress to 10-12 days if working full-time

## Success Metrics

### Hackathon Points
- **Base (100 pts)**: Docusaurus + strong RAG chatbot ✅
- **Bonus 1 (+50 pts)**: Better-auth with background questions ✅
- **Bonus 2 (+50 pts)**: Per-chapter personalization ✅
- **Bonus 3 (+50 pts)**: Urdu translation ✅
- **Bonus 4 (+50 pts)**: Reusable subagents/skills (Spec-Kit Plus usage) ✅

**Maximum Points**: 300 🏆

### Quality Metrics
- Lighthouse score: 90+
- RAG accuracy: 80%+ user satisfaction (subjective testing)
- Page load time: < 2s
- Chat response time: < 3s
- Zero critical bugs

## Next Steps

1. Review this plan
2. Generate tasks with `/sp.tasks`
3. Start implementation with `/sp.implement`
4. Iterate quickly, deploy early
5. Win the hackathon! 🚀

---

*This implementation plan provides a clear roadmap from specification to working product.*
