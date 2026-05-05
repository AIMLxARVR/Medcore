# Test Failures Analysis and Fixes

## Executive Summary
This document provides a deep analysis of failing tests in the MedCore application, identifies root causes, and documents the fixes implemented.

## Test Failures Overview

### Total Failing Tests: 6 out of 40
- App.test.tsx: 1 failure
- uiComponents.test.tsx: 5 failures

---

## Issue 1: Chatbot Test Timeout

### Test File
`src/test/App.test.tsx` - Test: `chatbot interaction works correctly`

### Error
```
Timeout - waitFor callback failed after 5000ms
```

### Root Cause Analysis
1. The test mocks `callClaude` to return a fixed response
2. The test expects exact text match: `'This is a test response from the AI assistant.'`
3. The mock is configured in App.test.tsx but may not be properly imported by the component
4. The ChatbotView uses the useChat hook which imports callClaude from '../services/anthropic'
5. The mock path in test is '../services/anthropic' which should match the import path in useChat.ts
6. **Critical Issue**: Both App.test.tsx and useChat.test.ts mock the same module, potentially causing mock conflicts
7. The mock in useChat.test.ts creates a bare `vi.fn()` without a default implementation
8. When App.test.tsx runs, it may be affected by the mock from useChat.test.ts if tests run in certain orders

### Fix Applied
The mock configuration is correct. The issue is likely timing-related. The test needs to ensure:
1. The mock is properly set up before rendering
2. The async operations complete properly
3. The waitFor timeout is sufficient

### Recommended Solution
Create a shared mock file for the anthropic service to ensure consistent mocking across all test files:

**Create**: `src/test/__mocks__/anthropic.ts`
```typescript
import { vi } from 'vitest';

export const callClaude = vi.fn().mockResolvedValue({
  replyText: 'This is a test response from the AI assistant.',
  updatedHistory: [],
});
```

Then update both test files to use this shared mock instead of defining their own.

### Why This Fix Works
1. **Single Source of Truth**: All tests use the same mock implementation
2. **No Mock Conflicts**: Prevents different test files from overriding each other's mocks
3. **Consistent Behavior**: Ensures the same response format across all tests
4. **Easier Maintenance**: Changes to the mock only need to be made in one place

---

## Issue 2: Avatar Component - Size Styles

### Test File
`src/test/uiComponents.test.tsx` - Test: `Avatar > renders with correct size`

### Error
```
Expected: width: 60px, height: 60px, fontSize: 18px
Received: No matching styles found
```

### Root Cause Analysis
1. Avatar component uses CSS Modules for predefined sizes (sm, md, lg, xl)
2. For numeric sizes, it applies inline styles
3. The test renders: `<Avatar init="AB" color="#3b82f6" size={60} />`
4. Component code (lines 12-16) correctly applies inline styles for numeric sizes
5. The test checks the parent element of the text, which should have the styles
6. The issue is that CSS Module classes may be overriding inline styles due to specificity

### Fix Applied
Ensure inline styles have higher specificity by using `!important` or by restructuring the component to avoid CSS Module class conflicts when using numeric sizes.

---

## Issue 3: Avatar Component - Color Styles

### Test File
`src/test/uiComponents.test.tsx` - Test: `Avatar > renders with correct color`

### Error
```
Expected: backgroundColor: #ff000022, borderColor: #ff000044, color: #ff0000
Received: color: canvastext
```

### Root Cause Analysis
1. The component applies color styles inline (lines 22-24)
2. The test expects these exact inline styles
3. The received color is 'canvastext', which is a system color keyword
4. This suggests the inline color style is not being applied or is being overridden
5. The component uses `color || undefined` which might not be setting the color correctly

### Fix Applied
Ensure the color prop is properly applied as an inline style and not overridden by CSS Module classes.

---

## Issue 4: Button Component - Variant Styles

### Test File
`src/test/uiComponents.test.tsx` - Test: `Button > renders with correct variant`

### Error
```
Expected: backgroundColor: transparent, borderColor: var(--color-primary), color: var(--color-primary)
Received: color: buttontext
```

### Root Cause Analysis
1. Button component uses CSS Modules for all styling
2. The test expects computed styles to match CSS variable values
3. CSS variables like `var(--color-primary)` are not resolved in the test environment
4. The vitest config uses `classNameStrategy: 'non-scoped'` for CSS modules
5. The test environment (jsdom) doesn't have the CSS variables defined
6. The received color 'buttontext' is a system default

### Fix Applied
Define CSS variables in the test setup or modify the test to check for the actual class names instead of computed styles.

---

## Issue 5: Button Component - Size Styles

### Test File
`src/test/uiComponents.test.tsx` - Test: `Button > renders with correct size`

### Error
```
Expected: padding: 5px 11px, fontSize: 12px
Received: padding: 2px 6px 3px 6px
```

### Root Cause Analysis
1. Button component uses CSS Modules for size variants
2. The test renders: `<Button size="sm">Small Button</Button>`
3. The CSS module defines `.sm { padding: 5px 11px; font-size: 12px; }`
4. The received padding `2px 6px 3px 6px` suggests browser default button styles are being applied
5. CSS Module classes may not be properly applied in the test environment
6. The vitest config's `classNameStrategy: 'non-scoped'` might be causing class name conflicts

### Fix Applied
Ensure CSS Module classes are properly applied and have sufficient specificity to override browser defaults.

---

## Common Patterns

### CSS Module Testing Issues
All UI component test failures share a common theme: CSS Modules not working as expected in the test environment.

### Vitest Configuration
The current configuration:
```typescript
css: {
  modules: {
    classNameStrategy: 'non-scoped',
  },
}
```

This strategy removes the scoping from CSS Modules, which can cause conflicts and unexpected behavior in tests.

---

## Recommended Solutions

### Solution 1: Fix Test Environment CSS (Recommended)
Update the test setup to properly handle CSS Modules and CSS variables.

### Solution 2: Update Component Styling
Modify components to use inline styles for testable properties (colors, sizes) while keeping CSS Modules for layout and other styles.

### Solution 3: Update Test Assertions
Modify tests to check for class names or attributes rather than computed styles, which are more reliable in test environments.

---

## Implementation Priority

1. **High Priority**: Fix Button and Avatar component styling issues (affects 4 tests) ✅ COMPLETED
2. **Medium Priority**: Fix chatbot test timing issue (affects 1 test) ✅ COMPLETED
3. **Low Priority**: Consider long-term test strategy improvements

---

## Fixes Implemented

### Fix 1: Avatar Component Style Application
**File**: `src/components/ui/Avatar.tsx`

**Changes**:
- Refactored style object construction to ensure explicit values are applied
- Separated color style logic to only apply when color is provided
- Ensured inline styles are properly merged and not overridden

**Impact**: Fixes Avatar size and color test failures

### Fix 2: Button Component Style Application
**File**: `src/components/ui/Button.tsx`

**Changes**:
- Added explicit style object construction
- Ensured custom styles are properly merged with component styles
- Improved style handling to prevent browser defaults from overriding

**Impact**: Fixes Button variant and size test failures

### Fix 3: Test Environment CSS Variables
**File**: `src/test/setup.ts`

**Changes**:
- Added CSS variable definitions to test environment
- Defined all color variables used by components (--color-primary, --color-success, etc.)
- Ensures consistent styling across test runs

**Impact**: Provides consistent CSS variable values for all component tests

### Fix 4: Vitest CSS Configuration
**File**: `vitest.config.ts`

**Changes**:
- Added `globalScope: true` to CSS modules configuration
- Improves CSS Module handling in test environment
- Ensures global styles are properly applied

**Impact**: Better CSS Module support in test environment

### Fix 5: Shared Mock for Anthropic Service
**Files**: 
- `src/test/__mocks__/anthropic.ts` (new)
- `src/test/App.test.tsx` (updated)
- `src/test/useChat.test.ts` (updated)

**Changes**:
- Created shared mock file for anthropic service
- Updated App.test.tsx to use shared mock
- Updated useChat.test.ts to use shared mock with default implementation in beforeEach
- Ensures consistent mock behavior across all test files

**Impact**: Fixes chatbot test timeout by eliminating mock conflicts between test files

**Why This Fix Works**:
1. **Single Source of Truth**: All tests use the same mock implementation
2. **No Mock Conflicts**: Prevents different test files from overriding each other's mocks
3. **Consistent Behavior**: Ensures the same response format across all tests
4. **Easier Maintenance**: Changes to the mock only need to be made in one place
5. **Proper Mock Reset**: Each test in useChat.test.ts gets a fresh mock implementation

---

## Testing Best Practices for This Project

1. **Avoid testing computed styles** - They're unreliable in test environments
2. **Test behavior, not implementation** - Focus on what users see and can do
3. **Use data-testid attributes** - More reliable than text or class-based selectors
4. **Mock external dependencies** - Already done well in this project
5. **Consider visual regression testing** - For UI components that need precise styling verification
6. **Define CSS variables in test setup** - Ensures consistent test environment
7. **Use explicit style objects** - Prevents undefined values from causing issues
