# Specification: Physical AI & Humanoid Robotics Textbook

## Overview
Create a comprehensive, AI-native textbook platform for teaching Physical AI and Humanoid Robotics. The platform combines a Docusaurus-based documentation site with an intelligent RAG chatbot, user authentication, content personalization, and multilingual support.

## Problem Statement
Industry practitioners need accessible, hands-on training to transition into robotics and embodied AI. Traditional textbooks lack:
- Interactive AI assistance for learning
- Personalized content based on user background
- Real-time Q&A capabilities
- Multilingual accessibility for diverse learners

## Target Users
1. **Primary**: Industry practitioners with Python knowledge transitioning to robotics
2. **Secondary**: Students in AI/robotics programs
3. **Tertiary**: Self-learners exploring Physical AI concepts

## Content Structure

### Course Modules (13 Weeks)
1. **Weeks 1-2**: Foundation & Setup
   - Introduction to Physical AI
   - Hardware path selection (Digital Twin Workstation / Jetson Orin / Cloud)
   - Development environment setup

2. **Weeks 3-5**: ROS 2 Fundamentals
   - ROS 2 architecture and concepts
   - Nodes, topics, services, actions
   - Robot simulation basics

3. **Weeks 6-7**: Digital Twin & Simulation
   - Gazebo simulation environment
   - Unity integration for robotics
   - Sim-to-real transfer concepts

4. **Weeks 8-10**: NVIDIA Isaac Sim
   - GPU-accelerated simulation
   - Synthetic data generation
   - Isaac Sim workflows

5. **Weeks 11-13**: Vision-Language-Action Models
   - Multimodal AI for robotics
   - VLA model integration
   - Humanoid robot control

6. **Week 14**: Capstone Project
   - Integration of all concepts
   - Real-world application

### Supporting Content
- **Glossary**: Technical terms and definitions
- **Troubleshooting**: Common issues and solutions
- **References**: External resources and citations
- **Code Examples**: Tested, runnable code snippets

## Core Features

### 1. Docusaurus Documentation Site

#### Homepage Dashboard
- Modern, card-based layout showing all modules
- Progress tracking (if authenticated)
- Quick links to popular sections
- Search functionality
- Featured content highlights

#### Content Pages
- Nested sidebar with collapsible categories
- Chapter metadata: prerequisites, learning objectives, estimated time
- Code syntax highlighting
- Embedded diagrams and visualizations
- Navigation between chapters (prev/next)
- Table of contents for long pages

#### UI Requirements
- **Responsive**: Mobile, tablet, desktop
- **Accessible**: Keyboard navigation, screen reader support
- **Dark Mode**: User preference toggle
- **Fast**: < 2s initial load, instant navigation
- **Modern**: Clean typography, generous whitespace

### 2. RAG Chatbot System

#### Architecture
```
User Query → Frontend Chat UI
    ↓
FastAPI Backend
    ↓
Query Processing → Embedding (Gemini)
    ↓
Retrieval Pipeline:
  1. Vector Search (Qdrant)
  2. Keyword Matching (Postgres FTS)
  3. Metadata Filtering
  4. Re-ranking
    ↓
Context Assembly → Prompt Construction
    ↓
Generation (Gemini API)
    ↓
Response + Citations → Frontend
```

#### Retrieval Strategy
1. **Vector Search** (Qdrant):
   - Embed user query with Gemini embeddings
   - Retrieve top-k semantically similar chunks
   - Filter by module/chapter if context available

2. **Keyword Search** (Postgres):
   - Full-text search for exact term matches
   - Boost recent/popular content

3. **Metadata Filtering**:
   - User's current chapter
   - Learning objectives
   - Prerequisite knowledge

4. **Re-ranking**:
   - Combine vector + keyword scores
   - Prioritize chunks with code examples
   - Boost content matching user's hardware path

#### Generation Strategy
- **System Prompt**: Educational assistant persona, cite sources
- **Context Window**: 
  - User query
  - Retrieved chunks (top 5-10)
  - Chat history (last 3-5 turns)
  - User profile (hardware path, experience level)
- **Parameters**:
  - Temperature: 0.7 for helpful but focused answers
  - Max tokens: Adaptive based on query complexity
  - Stop sequences: Section boundaries

#### Special Features
**Text Selection Q&A**:
- User highlights text on any page
- Right-click or floating button: "Ask AI about this"
- Context: selected text + surrounding paragraph
- Focused answers about selected content

**Chat Persistence**:
- Store conversations in Postgres
- Resume chats across sessions
- Export chat history

**Confidence Scoring**:
- High confidence: Direct answer from retrieval
- Medium: Synthesized from multiple sources
- Low: Suggest manual search or clarification

#### Citations
- Show source chapter/section for each answer
- Link to exact page in textbook
- Highlight relevant passages

### 3. Authentication System (Better-Auth)

#### Signup Flow
1. Email/password or OAuth (Google, GitHub)
2. **Background Assessment** (crucial for personalization):
   - Software background:
     - [ ] No programming experience
     - [ ] Python basics
     - [ ] Python advanced
     - [ ] Other languages (specify)
   - Hardware background:
     - [ ] No robotics experience
     - [ ] Hobby electronics
     - [ ] Embedded systems
     - [ ] Industrial robotics
   - Hardware setup:
     - [ ] Digital Twin Workstation (RTX GPU)
     - [ ] Jetson Orin Nano
     - [ ] Cloud-based (AWS/Azure)
     - [ ] Not decided yet
   - Learning goals (free text)

3. Create user profile in Postgres
4. Send welcome email with getting started guide

#### User Profile
- Display name, email
- Avatar (upload or Gravatar)
- Learning preferences
- Progress tracking per module
- Bookmarks/notes

#### Protected Features
- Chat history access
- Progress tracking
- Personalized content
- Saved bookmarks

### 4. Content Personalization

#### Per-Chapter Personalization
**Button at chapter start**: "Personalize this chapter for me"

**Personalization Logic**:
Based on user profile:
- **No programming**: Add more code explanations, link to Python resources
- **No robotics**: Expand hardware concepts, add visual aids
- **Digital Twin setup**: Emphasize Gazebo/Unity examples
- **Jetson setup**: Highlight edge optimization, power constraints
- **Cloud setup**: Focus on scalable architectures, cost optimization

**Implementation**:
1. User clicks "Personalize"
2. Fetch user profile from Postgres
3. Send chapter content + profile to Gemini API
4. Prompt: "Adapt this content for a user with [background]. Add explanations for [gaps], emphasize [preferences]"
5. Display personalized version (toggle to view original)
6. Cache personalized versions in Postgres

#### Personalization Features
- Expand/simplify code examples
- Add/remove prerequisite explanations
- Suggest additional resources
- Adjust terminology level
- Highlight relevant hardware-specific notes

### 5. Urdu Translation

#### Per-Chapter Translation
**Button at chapter start**: "اردو میں پڑھیں" (Read in Urdu)

**Translation Strategy**:
1. **Technical Terms**: Preserve technical terms in English (ROS 2, Gazebo, etc.) with Urdu explanations
2. **Code**: Keep code blocks in English
3. **Explanations**: Translate to natural Urdu
4. **Mixed Script**: Urdu text with embedded English terms (common in Pakistani tech education)

**Implementation**:
1. User clicks translation button
2. Check cache (Postgres) for existing translation
3. If not cached:
   - Send chapter content to Gemini API
   - Prompt: "Translate to Urdu preserving technical terms and code blocks"
   - Store in Postgres with chapter_id + language
4. Display translated version (toggle to English)

**UI Considerations**:
- Right-to-left (RTL) layout for Urdu
- Urdu-compatible fonts (Noto Nastaliq Urdu)
- Mixed direction for code blocks (LTR within RTL)

### 6. Content Management

#### Content Source
- Base content from: https://github.com/Ameen-Alam/Physical-AI-Humanoid-Robotics-Textbook
- **Data Cleaning**:
  - Remove personal names ("Ameen Alam", etc.)
  - Update repository links to Panaversity organization
  - Verify all code examples
  - Optimize images

#### Content Ingestion for RAG
1. **Extract**: Parse Markdown files from docs/
2. **Chunk**: 
   - By section (## headers)
   - Max 1000 tokens per chunk
   - Overlap 100 tokens between chunks
   - Preserve code blocks intact
3. **Embed**:
   - Generate embeddings with Gemini text-embedding model
   - Store in Qdrant with metadata:
     - `module`, `chapter`, `section`
     - `content_type` (text/code/diagram)
     - `difficulty_level`
     - `prerequisites`
4. **Index**:
   - Qdrant: vector similarity
   - Postgres: full-text search, metadata queries

## Technical Requirements

### Frontend
- **Framework**: Docusaurus 3.x
- **Language**: TypeScript (strict mode)
- **Styling**: CSS Modules or Tailwind (TBD)
- **State**: React Context for global state
- **API Client**: Axios or Fetch API
- **Build**: Static site generation for content pages

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **API Docs**: OpenAPI/Swagger auto-generated
- **Validation**: Pydantic v2
- **CORS**: Configured for Netlify domain
- **Rate Limiting**: Per-user and global

### Databases
1. **Qdrant Cloud** (Free Tier):
   - Vector embeddings
   - Collections: `textbook_content`, `chat_history_embeddings`

2. **Neon Serverless Postgres** (Free Tier):
   - Tables:
     - `users` (id, email, profile_data, created_at)
     - `chat_history` (id, user_id, session_id, messages, created_at)
     - `personalized_content` (chapter_id, user_id, content, created_at)
     - `translations` (chapter_id, language, content, created_at)
     - `content_metadata` (chunk_id, module, chapter, metadata)

### AI Services
- **Google Gemini API**:
  - Model: `gemini-2.0-flash-exp` for chat
  - Model: `text-embedding-004` for embeddings
  - API Key: Environment variable `GEMINI_API_KEY`

### Authentication
- **Better-Auth**:
  - Email/password + OAuth providers
  - Session management
  - CSRF protection

### Deployment
- **Frontend**: Netlify
  - Automatic deployments from main branch
  - Netlify Functions for API proxy (optional)
  - Environment variables for API URL

- **Backend**: 
  - Option 1: Netlify Functions (serverless)
  - Option 2: Railway/Render (containerized)
  - Option 3: Vercel Serverless Functions

## User Flows

### Flow 1: New User Onboarding
1. Land on homepage → See course overview
2. Click "Get Started" → Prompted to signup
3. Signup with email → Answer background questions
4. Redirected to Module 1 → See personalization option
5. Click "Personalize" → Content adapted to profile
6. Start reading → Highlight text → Ask chatbot
7. Chatbot provides answer with citations

### Flow 2: Authenticated User Learning
1. Login → Dashboard shows progress
2. Navigate to current chapter
3. Click "Read in Urdu" → Content translated
4. Open chatbot → Ask question
5. Chatbot retrieves context, generates answer
6. User bookmarks important section
7. Continue to next chapter

### Flow 3: Text Selection Q&A
1. User reads chapter
2. Encounters confusing paragraph
3. Highlights text
4. Clicks "Ask AI"
5. Chatbot modal opens with highlighted text as context
6. User types follow-up question
7. Chatbot provides focused explanation
8. User closes modal, continues reading

## Non-Functional Requirements

### Performance
- **Page Load**: < 2s for 95th percentile
- **Chatbot Response**: < 3s for 95th percentile
- **Search**: < 500ms
- **Translation**: < 5s (or instant from cache)

### Security
- HTTPS everywhere
- API keys in environment variables
- Input validation and sanitization
- Rate limiting (10 requests/min for chat)
- SQL injection protection (parameterized queries)

### Accessibility
- WCAG 2.1 AA compliance
- Keyboard navigation
- Screen reader compatible
- Color contrast ratios > 4.5:1
- Alt text for all images

### Scalability
- Static site scales automatically (Netlify CDN)
- Database queries optimized with indexes
- Vector search limited to top-k results
- Caching for translations and personalized content

### Monitoring
- Error tracking (Sentry or similar)
- Analytics (Plausible or Google Analytics)
- Chatbot usage metrics
- Performance monitoring (Web Vitals)

## Success Criteria

### Functional
✅ All 13 weeks of content accessible  
✅ Chatbot answers questions accurately (>80% user satisfaction in testing)  
✅ Text selection Q&A works seamlessly  
✅ Authentication flow easy and secure  
✅ Personalization meaningfully adapts content  
✅ Urdu translation readable and accurate  

### Technical
✅ Lighthouse scores > 90 across the board  
✅ Zero console errors in production  
✅ API endpoints documented and tested  
✅ Database queries < 100ms (avg)  
✅ No hardcoded secrets  

### User Experience
✅ Intuitive navigation  
✅ Helpful error messages  
✅ Responsive on all device sizes  
✅ Chatbot feels conversational  
✅ Personalization feels magical  

### Hackathon Deliverables
✅ Public GitHub repository  
✅ Deployed site on Netlify  
✅ < 90s demo video  
✅ Clear README with setup instructions  
✅ Live presentation slides (if invited)  

## Out of Scope (for v1)
- User-generated content (comments, forums)
- Video lectures
- Interactive coding environments
- Instructor dashboard
- Certificate generation
- Mobile app
- Offline mode

## Open Questions
1. Should we use Netlify Functions or separate backend hosting?
2. Tailwind CSS or CSS Modules for styling?
3. Should translations be editable by users?
4. What's the budget for Gemini API calls?
5. Should we implement analytics from day 1?

---

*This specification will be broken down into an implementation plan, tasks, and then executed using Spec-Kit Plus methodology.*
