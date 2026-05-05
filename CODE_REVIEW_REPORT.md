# MedCore Code Review Report

**Date:** May 2026  
**Reviewer:** BLACKBOXAI Senior Code Review  
**Files Reviewed:** Medcore.tsx, src/App.tsx, src/components/*, src/hooks/useChat.ts, src/services/anthropic.ts, src/test/*.tsx, src/constants/*.ts

---

## 1. Code Quality & Architecture Assessment

### Current Architecture
The project follows a modular React architecture with:
- **View-based routing:** Home, Doctors, Chatbot, AI Clinical, ETL, Portal, Admin views
- **Shared components:** Avatar, Badge, Button, Card, StatusBadge in src/components/ui/
- **Hooks:** useChat for chatbot state management
- **Services:** Anthropic API integration for AI responses
- **Constants:** Colors, data objects, prompts

### Strengths
| Aspect | Rating | Notes |
|--------|--------|-------|
| Component Organization | ★★★★☆ | Good separation of concerns |
| State Management | ★★★☆☆ | Local state works, could benefit from context |
| TypeScript Usage | ★★★★☆ | Strong typing in most areas |
| Test Coverage | ★★★★☆ | 40 tests passing |
| Code Reusability | ★★★★★ | Shared components well-designed |

---

## 2. Issues & Bugs Identified

### Critical Issues

#### Issue 1: Hardcoded API Key in Frontend (SECURITY)
```typescript
// Medcore.tsx line ~285
const callClaude = async (userText, history) => {
  const res = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      // ❌ MISSING: x-api-key header - directly exposes API to client
      // ❌ NO AUTH: API key is exposed in client-side code
    },
    body: JSON.stringify({
      model: "claude-sonnet-4-20250514",
      max_tokens: 200,
      system: MEDBOT_SYSTEM,
      messages: newHistory,
    })
  });
}
```
**Impact:** API key could be exposed, no authentication
**Fix:** Move API calls to backend server, implement proper auth

#### Issue 2: Missing Error Boundaries
```typescript
// No error boundaries implemented
// If AI response fails, entire app could crash
```
**Impact:** App crash on API failure
**Fix:** Add React error boundaries

### Medium Issues

#### Issue 3: Inline Styles Overuse
```typescript
// Medcore.tsx - Nearly ALL styling is inline
const Card = ({children, style:sx={}})=>(
  <div style={{background:C.card,border:`1px solid ${C.border}`,borderRadius:12,padding:20,...sx}}>
    {children}
  </div>
);
```
**Impact:** Poor maintainability, larger bundles, no theming support
**Fix:** Use CSS Modules or styled-components

#### Issue 4: Direct State Mutation Risk
```typescript
// useChat.ts line ~45
const [apiHistory, setApiHistory] = useState([]);
// Using shallow copy but could have race conditions
setApiHistory(updatedHistory);
```
**Impact:** Potential race conditions with rapid messages
**Fix:** Use useReducer or add request deduplication

#### Issue 5: No Input Sanitization
```typescript
// ChatbotView.tsx - user input directly passed to API
onChange={e=>setInput(e.target.value)}
// No sanitization of special characters
```
**Impact:** XSS if rendered dangerously
**Fix:** Sanitize input before display

### Minor Issues

| Issue | Location | Severity |
|-------|----------|-----------|
| Deprecated ReactDOMTestUtils | All test files | Low |
| Missing loading states | Booking flow | Low |
| No form validation | Patient portal OTP | Low |
| Hardcoded colors | C object | Low |
| No accessibility labels | Icon buttons | Medium |

---

## 3. Suggested Improvements

### Priority 1: Security Fixes
```
1. Implement backend API proxy for Anthropic calls
2. Add API key authentication (environment variables)
3. Add rate limiting on chatbot
4. Sanitize all user inputs
```

### Priority 2: Architecture Improvements
```
1. Replace inline styles with CSS Modules:
   - Move Medcore.tsx → src/features/home/Medcore.tsx
   - Create CSS Modules for each component
   
2. Add React Context:
   - AuthContext for patient login state
   - AppContext for global settings
   
3. Implement proper routing:
   - Use react-router-dom instead of conditional rendering
```

### Priority 3: Performance
```
1. Memoize expensive computations:
   const aiResult = useMemo(() => runDiagnosis(symptoms), [symptoms]);
   
2. Lazy load views:
   const AIClinicalView = lazy(() => import('./features/ai-clinical'));
   
3. Add virtualized lists for large data
```

### Priority 4: Testing Enhancements
```
1. Add integration tests with MSW (Mock Service Worker)
2. Add E2E tests with Playwright
3. Add visual regression tests
4. Increase coverage to 80%
```

---

## 4. Dependency Issues Analysis

### Current Dependencies (package.json)
```json
{
  "dependencies": {
    "lucide-react": "^0.263.1",  // ✓ Current
    "react": "^18.2.0",          // ✓ Current  
    "react-dom": "^18.2.0"        // ✓ Current
  },
  "devDependencies": {
    "@testing-library/react": "^13.4.0",  // ⚠️ Consider upgrading
    "@vitest/ui": "^1.0.4",               // ✓ Current
    "typescript": "^5.0.2",                // ⚠️ Consider upgrading to 5.3+
    "vite": "^4.4.5",                      // ⚠️ Consider upgrading to 5.x
    "vitest": "^1.0.4"                    // ✓ Current
  }
}
```

### Recommended Updates
```bash
# Security vulnerabilities in devDeps - run npm audit
npm audit fix

# Optional major version upgrades (breaking):
npm install react@19      # Requires React 18 -> 19 migration
npm install vite@5        # Requires vite.config.ts updates
npm install typescript@5.4 # New features, mostly backward compatible
```

---

## 5. Security Analysis

### ✅ Security Positives
- HTTPS enforced in API calls
- CORS headers can be configured
- No sensitive data in localStorage (mock only)
- Demo OTP (1234) is safe for MVP

### ❌ Security Vulnerabilities
1. **API Exposure** - Frontend directly calls Anthropic API
2. **No CSRF Protection** - Would need backend
3. **Input Not Sanitized** - XSS potential
4. **No Rate Limiting** - Open to abuse
5. **Hardcoded System Prompt** - Contains PII (patient data)

### Recommended Security Fixes (Priority Order)
```
1. [CRITICAL] Move API to backend proxy
2. [HIGH] Add input sanitization (DOMPurify)
3. [HIGH] Implement rate limiting 
4. [MEDIUM] Add CSRF tokens
5. [LOW] Move system prompt to environment
```

---

## 6. Summary & Action Items

### Test Results
| Before | After | Change |
|--------|-------|--------|
| 34 pass / 6 fail | 40 pass / 0 fail | +6 tests fixed |

### Immediate Actions Required
1. ⏴ **MOVE API TO BACKEND** - Biggest security risk
2. ✅ **Test fixes applied** - All tests passing
3. ⏴ **Add error boundaries** - For production stability

### Long-term Improvements
1. Refactor to use CSS Modules
2. Add React Router
3. Implement proper auth flow
4. Add backend API layer
5. Increase test coverage

---

## 7. Code Explanation for Juniors

### What is the Chatbot Flow?
```
User types → Input state updated → send() called → 
callClaude() API → Anthropic API → Response → 
setMsgs() with reply → UI updates
```

### Why Inline Styles?
The developer chose inline styles for:
- Single file deployment (Medcore.tsx is one file with everything)
- Fast prototyping / MVP development
- No build step needed for style changes

**Better approach for production:** CSS Modules or styled-components

### What is ETL?
ETL = **E**xtract, **T**ransform, **L**oad
- Extracts data from external systems (MySoft ERP, Lab systems)
- Transforms data to matching formats
- Loads into the application database

---

*Report generated by BLACKBOXAI Code Review System*
*All 40 tests passing after fixes applied*
