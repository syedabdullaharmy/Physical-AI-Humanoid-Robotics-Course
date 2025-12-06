# Project Constitution: Physical AI & Humanoid Robotics Textbook

## Core Principles

### 1. Educational Excellence
- **Clarity First**: All content must be accessible to industry practitioners with Python knowledge
- **Hands-On Learning**: Prioritize practical, executable examples over theory
- **Progressive Complexity**: Build knowledge incrementally across 13 weeks
- **Real-World Relevance**: Focus on production-ready skills for robotics industry

### 2. AI-Native Development
- **Specification-Driven**: All features start with clear specs before implementation
- **Gemini-Powered**: Use Google Gemini API for all AI functionality (NOT OpenAI)
- **RAG Excellence**: Prioritize accurate, context-aware responses with strong retrieval
- **User Context**: Leverage user background for personalized learning experiences

### 3. Technical Standards

#### Frontend (Docusaurus 3)
- **Modern UI**: Clean, dashboard-style interface with intuitive navigation
- **Accessibility**: WCAG 2.1 AA compliance minimum
- **Performance**: Lighthouse score > 90 for all metrics
- **Mobile-First**: Responsive design for all screen sizes
- **SEO Optimized**: Proper meta tags, semantic HTML, structured data

#### Backend (FastAPI)
- **API-First**: RESTful design with OpenAPI documentation
- **Type Safety**: Full Pydantic validation for all endpoints
- **Error Handling**: Comprehensive error responses with actionable messages
- **Security**: Rate limiting, CORS, input validation
- **Observability**: Structured logging for debugging

#### RAG System
- **Strong Retrieval**: 
  - Qdrant vector database for semantic search
  - Neon Postgres for metadata and user data
  - Multi-stage retrieval (vector + keyword + metadata)
  - Context window optimization
- **Accurate Generation**:
  - Gemini API with properly tuned parameters
  - Citation tracking for verifiable answers
  - Confidence scoring for responses
- **User Features**:
  - Text selection-based queries
  - Chat history persistence
  - Context-aware follow-ups

#### Database Architecture
- **Qdrant Cloud**: Vector embeddings (free tier)
- **Neon Serverless Postgres**: 
  - User profiles and authentication
  - Chat history
  - Content metadata
  - Personalization preferences
  - Translation cache

### 4. Authentication & Personalization
- **Better-Auth**: Modern, secure authentication system
- **User Profiling**: Collect software/hardware background at signup
- **Adaptive Content**: Personalize explanations based on user expertise
- **Multilingual**: Urdu translation with caching for performance

### 5. Code Quality

#### Testing
- **Unit Tests**: 80%+ coverage for critical paths
- **Integration Tests**: API endpoints and database operations
- **E2E Tests**: Critical user journeys
- **Performance Tests**: RAG latency < 3s for 95th percentile

#### Code Standards
- **TypeScript**: Strict mode for frontend
- **Python**: Type hints, Black formatting, Ruff linting
- **Documentation**: JSDoc/Docstrings for all public APIs
- **Git Hygiene**: Conventional commits, feature branches

### 6. Deployment & Operations
- **Netlify**: Frontend deployment with automatic previews
- **Environment Separation**: Dev, staging, production configs
- **Secrets Management**: No hardcoded credentials
- **Monitoring**: Error tracking and performance metrics
- **Graceful Degradation**: Fallbacks when AI services unavailable

### 7. Content Guidelines
- **No Personal References**: Remove "Ameen Alam" and similar names
- **Panaversity Branding**: Use Panaversity organization context
- **Consistent Formatting**: Follow Docusaurus best practices
- **Code Examples**: Tested, runnable, with prerequisites
- **Visual Aids**: Diagrams for complex concepts (generate if needed)

### 8. Hackathon Success Criteria

#### Base Requirements (100 pts)
✅ Docusaurus book deployed to Netlify  
✅ Content from reference repository (without personal names)  
✅ Strong RAG chatbot with Gemini API  
✅ Qdrant + Neon database integration  
✅ Text selection Q&A feature

#### Bonus Points (200 pts possible)
🌟 Better-auth signup/signin with background questions (+50)  
🌟 Personalization button per chapter (+50)  
🌟 Urdu translation button per chapter (+50)  
🌟 Reusable Claude Code subagents/skills (+50)

### 9. Development Workflow
1. **Spec-Kit Plus Methodology**:
   - Constitution (this document) ✅
   - Specification → Plan → Tasks → Implementation
2. **Incremental Delivery**:
   - Phase 1: Basic Docusaurus setup + content migration
   - Phase 2: RAG chatbot core functionality
   - Phase 3: Authentication & user profiling
   - Phase 4: Personalization & translation
   - Phase 5: Polish & deployment
3. **Continuous Testing**: Run tests after each phase
4. **Early Deployment**: Deploy to Netlify early, iterate

### 10. Non-Negotiables
❌ **NO** OpenAI API - Use Gemini only  
❌ **NO** personal names in the deployed site  
❌ **NO** hardcoded API keys - Use environment variables  
❌ **NO** untested database migrations  
❌ **NO** deployment without linting/type checking  
✅ **YES** to strong RAG (accuracy over speed)  
✅ **YES** to beautiful, modern UI  
✅ **YES** to comprehensive documentation  

## Success Metrics
- **Functionality**: All core + bonus features working
- **Performance**: Fast page loads, responsive chatbot
- **Code Quality**: Clean, maintainable, well-documented
- **User Experience**: Intuitive, delightful, accessible
- **Demo Video**: Clear, compelling, < 90 seconds
- **Presentation**: Confident explanation of technical choices

---

_This constitution guides all development decisions for the Physical AI & Humanoid Robotics Textbook project._
