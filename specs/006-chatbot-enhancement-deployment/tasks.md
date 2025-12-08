# Tasks: Enhanced RAG Chatbot & Multi-Platform Deployment

**Tasks ID**: `006-chatbot-enhancement-deployment`  
**Version**: 1.0.0  
**Status**: 🟡 In Progress  
**Created**: 2025-12-09

## Task List

### ✅ Phase 0: Specification & Planning (COMPLETED)
- [x] T0.1: Create specification document
- [x] T0.2: Create implementation plan
- [x] T0.3: Create task breakdown

### 🔵 Phase 1: Chatbot UI Enhancement (IN PROGRESS)

#### T1.1: Update ChatWidget Styling
- [ ] Update color palette in ChatWidget.module.css
- [ ] Add gradient backgrounds for buttons
- [ ] Implement slide-up animation for messages
- [ ] Add pulse animation for loading dots
- [ ] Enhance button hover effects with transform + shadow
- [ ] Improve message bubble styling (padding, radius, shadow)
- [ ] Update scrollbar styling for chat messages area
- [ ] Test dark mode compatibility

**Files**: `frontend/src/components/ChatWidget/ChatWidget.module.css`  
**Duration**: 30 min  
**Dependencies**: None

#### T1.2: Add Suggested Questions
- [ ] Define array of 5 suggested questions
- [ ] Add state for showing/hiding suggestions
- [ ] Create SuggestedQuestions component/section
- [ ] Style suggestion buttons (pill-shaped, hover effects)
- [ ] Implement click handler to populate input and send
- [ ] Hide suggestions after first interaction
- [ ] Test suggested questions flow

**Files**: `frontend/src/components/ChatWidget/index.tsx`  
**Duration**: 20 min  
**Dependencies**: None

#### T1.3: Implement Message History Persistence
- [ ] Add localStorage save on message change
- [ ] Add localStorage load on component mount
- [ ] Implement 50-message limit
- [ ] Add error handling for localStorage (quota, disabled)
- [ ] Create clearHistory function
- [ ] Add "Clear History" button to header
- [ ] Test persistence across page reloads
- [ ] Test in incognito mode (localStorage disabled)

**Files**: `frontend/src/components/ChatWidget/index.tsx`  
**Duration**: 25 min  
**Dependencies**: None

#### T1.4: Add Copy Message Feature
- [ ] Create copyMessage async function using Clipboard API
- [ ] Add message actions container to UI
- [ ] Create copy button with icon
- [ ] Add tooltip on hover ("Copy")
- [ ] Implement copy success feedback (toast or checkmark)
- [ ] Handle copy errors gracefully
- [ ] Test on different browsers
- [ ] Add accessibility labels

**Files**: `frontend/src/components/ChatWidget/index.tsx`, `ChatWidget.module.css`  
**Duration**: 20 min  
**Dependencies**: None

#### T1.5: Make Citations Clickable
- [ ] Update Citation interface to include path
- [ ] Generate path from module/chapter names
- [ ] Render citations as anchor tags
- [ ] Add external link icon
- [ ] Style citation links (color, hover, underline)
- [ ] Test citation navigation
- [ ] Ensure links open in same tab (Docusaurus SPA)
- [ ] Add accessibility attributes (rel, aria-label)

**Files**: `frontend/src/components/ChatWidget/index.tsx`, `ChatWidget.module.css`  
**Duration**: 20 min  
**Dependencies**: None

#### T1.6: Enhanced Error Handling
- [ ] Create error state with message and retryable flag
- [ ] Update sendMessage with try-catch improvements
- [ ] Add timeout to fetch (30s AbortSignal)
- [ ] Differentiate error types (network, server, timeout, rate limit)
- [ ] Implement auto-retry logic for network errors (1 retry)
- [ ] Create error banner component
- [ ] Add retry button to error banner
- [ ] Style error states (color, icon, position)
- [ ] Test various error scenarios

**Files**: `frontend/src/components/ChatWidget/index.tsx`, `ChatWidget.module.css`  
**Duration**: 30 min  
**Dependencies**: None

---

### 🎨 Phase 2: Visual Design Enhancements

#### T2.1: Integrate Google Fonts
- [ ] Add preconnect link to docusaurus.config.js headTags
- [ ] Add stylesheet link for Inter and Space Grotesk
- [ ] Update CSS variables for font families
- [ ] Set Inter for body text
- [ ] Set Space Grotesk for headings
- [ ] Test font rendering across pages
- [ ] Verify font weights (400, 500, 600, 700)

**Files**: `docusaurus.config.js`, `frontend/src/css/custom.css`  
**Duration**: 15 min  
**Dependencies**: None

#### T2.2: Update Color Palette
- [ ] Define new CSS custom properties for colors
- [ ] Create primary gradient variable
- [ ] Add accent colors (purple, pink)
- [ ] Update neutral grays (50-900 scale)
- [ ] Add semantic colors (success, warning, error, info)
- [ ] Override Docusaurus primary colors
- [ ] Update dark mode color variables
- [ ] Test color contrast ratios (WCAG AA)

**Files**: `frontend/src/css/custom.css`  
**Duration**: 20 min  
**Dependencies**: None

#### T2.3: Add Smooth Transitions
- [ ] Add global transition for theme changes
- [ ] Create micro-animation for button hovers
- [ ] Add fade-in animation for page load
- [ ] Implement smooth scroll behavior
- [ ] Add transition for navbar background
- [ ] Create card hover lift effect
- [ ] Test animations for performance (60fps)
- [ ] Ensure reduced-motion media query respected

**Files**: `frontend/src/css/custom.css`  
**Duration**: 20 min  
**Dependencies**: None

#### T2.4: Improve Mobile Responsiveness
- [ ] Adjust ChatWidget for full-screen on mobile
- [ ] Update button sizes for touch targets (44x44px min)
- [ ] Adjust font size for mobile (15px)
- [ ] Test navbar collapse on small screens
- [ ] Improve sidebar mobile behavior
- [ ] Test on various device sizes (375px, 768px, 1024px)
- [ ] Verify touch gestures work smoothly
- [ ] Test horizontal scroll prevention

**Files**: `frontend/src/css/custom.css`, `ChatWidget.module.css`  
**Duration**: 25 min  
**Dependencies**: None

---

### 🚀 Phase 3: Deployment Configuration

#### T3.1: Create GitHub Pages Workflow
- [ ] Create `.github/workflows/deploy-gh-pages.yml`
- [ ] Configure checkout step
- [ ] Add Node.js setup (v20)
- [ ] Add npm ci step
- [ ] Add build step with env vars
- [ ] Configure artifact upload
- [ ] Add deployment step
- [ ] Set required permissions
- [ ] Test workflow on push to main

**Files**: `.github/workflows/deploy-gh-pages.yml` (new)  
**Duration**: 25 min  
**Dependencies**: T1.* (for testing deployment)

#### T3.2: Update Vercel Configuration
- [ ] Update vercel.json with correct paths
- [ ] Add environment variable configuration
- [ ] Add security headers
- [ ] Configure redirects
- [ ] Set framework to docusaurus
- [ ] Add build and dev commands
- [ ] Test configuration locally
- [ ] Document required environment variables

**Files**: `vercel.json`  
**Duration**: 15 min  
**Dependencies**: None

#### T3.3: Multi-Environment Docusaurus Config
- [ ] Add environment detection (dev, GH Pages, Vercel)
- [ ] Set dynamic URL based on platform
- [ ] Set dynamic baseUrl (/ for Vercel, /repo/ for GH Pages)
- [ ] Update REACT_APP_API_URL handling
- [ ] Add GitHub Pages specific config
- [ ] Set conditional error handling (warn vs throw)
- [ ] Test build locally
- [ ] Verify environment variables picked up

**Files**: `docusaurus.config.js`  
**Duration**: 20 min  
**Dependencies**: None

#### T3.4: Build Optimizations
- [ ] Enable experimental_faster in Docusaurus config
- [ ] Configure webpack for SWC loader (if needed)
- [ ] Enable lazy loading for Prism languages
- [ ] Optimize image assets in /static
- [ ] Enable sitemap generation
- [ ] Configure robots.txt
- [ ] Test production build size
- [ ] Run bundle analyzer

**Files**: `docusaurus.config.js`, various assets  
**Duration**: 30 min  
**Dependencies**: None

---

### ✅ Phase 4: Testing & Validation

#### T4.1: Local Build Testing
- [ ] Run `npm run build` in frontend
- [ ] Serve build locally with `npm run serve`
- [ ] Test all routes load correctly
- [ ] Test ChatWidget functionality
- [ ] Verify suggested questions appear
- [ ] Test message history persistence
- [ ] Test copy message feature
- [ ] Verify citation links work
- [ ] Test error handling (disconnect backend)
- [ ] Test dark mode toggle
- [ ] Check console for errors/warnings

**Duration**: 20 min  
**Dependencies**: T1.*, T2.*

#### T4.2: GitHub Pages Deployment
- [ ] Add BACKEND_API_URL secret to GitHub repo
- [ ] Push changes to main branch
- [ ] Monitor GitHub Actions workflow
- [ ] Check for build errors
- [ ] Verify deployment completes
- [ ] Visit deployed site URL
- [ ] Test chatbot with backend connection
- [ ] Test all major routes
- [ ] Verify search functionality
- [ ] Check mobile responsiveness

**Duration**: 20 min  
**Dependencies**: T3.1, T3.3, T4.1

#### T4.3: Vercel Deployment
- [ ] Connect GitHub repo to Vercel
- [ ] Configure root directory (if needed)
- [ ] Add REACT_APP_API_URL environment variable
- [ ] Trigger deployment
- [ ] Monitor build logs
- [ ] Check for errors/warnings
- [ ] Visit deployed Vercel URL
- [ ] Test chatbot with backend connection
- [ ] Test all major routes
- [ ] Verify search functionality
- [ ] Check mobile responsiveness

**Duration**: 20 min  
**Dependencies**: T3.2, T3.3, T4.1

#### T4.4: Performance Audit
- [ ] Run Lighthouse on deployed GitHub Pages site
- [ ] Run Lighthouse on deployed Vercel site
- [ ] Check Performance score (target ≥90)
- [ ] Check Accessibility score (target ≥95)
- [ ] Check Best Practices score (target ≥95)
- [ ] Check SEO score (target ≥95)
- [ ] Review bundle size
- [ ] Check First Contentful Paint (target <2s)
- [ ] Check Time to Interactive (target <3s)
- [ ] Document any issues found

**Duration**: 20 min  
**Dependencies**: T4.2, T4.3

#### T4.5: Accessibility Audit
- [ ] Test keyboard navigation (Tab, Enter, Esc)
- [ ] Test screen reader compatibility (NVDA/JAWS)
- [ ] Verify focus indicators visible
- [ ] Check color contrast with axe DevTools
- [ ] Verify ARIA labels present
- [ ] Test with WAVE browser extension
- [ ] Check heading hierarchy
- [ ] Verify alt text on all images
- [ ] Test with zoom levels (200%, 400%)
- [ ] Document any issues found

**Duration**: 25 min  
**Dependencies**: T4.2, T4.3

---

### 📋 Phase 5: Documentation & Cleanup

#### T5.1: Update README
- [ ] Add deployment links (GitHub Pages, Vercel)
- [ ] Update deployment instructions
- [ ] Document new chatbot features
- [ ] Add screenshots of enhanced UI
- [ ] Update environment variables section
- [ ] Add troubleshooting section
- [ ] Update architecture diagrams (if needed)

**Files**: `README.md`  
**Duration**: 20 min  
**Dependencies**: T4.*

#### T5.2: Create Deployment Documentation
- [ ] Document GitHub Pages setup steps
- [ ] Document Vercel setup steps
- [ ] List required secrets/environment variables
- [ ] Add troubleshooting common issues
- [ ] Document CORS configuration for backend
- [ ] Add monitoring and rollback instructions

**Files**: `DEPLOYMENT.md` (update)  
**Duration**: 15 min  
**Dependencies**: T4.*

#### T5.3: Code Cleanup
- [ ] Remove console.log statements
- [ ] Remove commented code
- [ ] Update code comments
- [ ] Check for unused imports
- [ ] Verify no TODOs left
- [ ] Run prettier/formatter
- [ ] Final git commit with clean message

**Files**: All modified files  
**Duration**: 15 min  
**Dependencies**: All previous tasks

---

## Task Summary

| Phase | Tasks | Estimated Time | Status |
|-------|-------|----------------|--------|
| Phase 0: Spec & Planning | 3 | 1h | ✅ DONE |
| Phase 1: Chatbot Enhancement | 6 | 2h 25min | 🔵 IN PROGRESS |
| Phase 2: Visual Design | 4 | 1h 20min | ⏸️ PENDING |
| Phase 3: Deployment Config | 4 | 1h 30min | ⏸️ PENDING |
| Phase 4: Testing | 5 | 1h 45min | ⏸️ PENDING |
| Phase 5: Documentation | 3 | 50min | ⏸️ PENDING |
| **TOTAL** | **25** | **~9h** | **12% Complete** |

## Implementation Order

**Recommended sequence**:
1. **Phase 1** → Chatbot improvements (visible user value)
2. **Phase 2** → Visual polish (enhanced UX)
3. **Phase 3** → Deployment setup (infrastructure)
4. **Phase 4** → Testing (quality assurance)
5. **Phase 5** → Documentation (completion)

## Risk Mitigation Checklist

- [ ] Backend CORS configured for new domains
- [ ] GitHub secrets properly set
- [ ] Vercel environment variables configured
- [ ] Local testing passed before deployment
- [ ] Rollback plan documented
- [ ] Performance baseline measured

## Acceptance Criteria

### Chatbot Enhancement ✅
- [ ] All 6 new features implemented and working
- [ ] No regressions in existing functionality
- [ ] Mobile responsive
- [ ] Accessible (keyboard nav, screen readers)

### Visual Design ✅
- [ ] Matches reference site quality
- [ ] Dark mode works perfectly
- [ ] Animations smooth (60fps)
- [ ] Color contrast meets WCAG AA

### Deployment ✅
- [ ] GitHub Pages deployment successful
- [ ] Vercel deployment successful
- [ ] Both connect to backend API
- [ ] All routes work on both platforms

### Performance ✅
- [ ] Lighthouse Performance ≥90
- [ ] Lighthouse Accessibility ≥95
- [ ] Bundle size reasonable (<500KB initial)
- [ ] Fast load times (<3s TTI)

---

**Next Step**: Begin implementation with Phase 1  
**Current Focus**: T1.1 - Update ChatWidget Styling  
**ETA for Phase 1**: ~2.5 hours
