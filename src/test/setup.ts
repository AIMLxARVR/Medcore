import '@testing-library/jest-dom';
import { cleanup } from '@testing-library/react';
import { afterEach } from 'vitest';

// Cleanup after each test
afterEach(() => {
  cleanup();
});

// Define CSS variables for consistent test environment
const style = document.createElement('style');
style.textContent = `
  :root {
    --color-primary: #3b82f6;
    --color-secondary: #8b5cf6;
    --color-success: #10b981;
    --color-danger: #ef4444;
    --color-warning: #f59e0b;
    --color-muted: #6b7280;
    --color-border: #e5e7eb;
    --color-green: #10b981;
    --color-red: #ef4444;
    --color-purple: #8b5cf6;
  }
`;
document.head.appendChild(style);

// Mock window.matchMedia
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: (query: string) => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: () => {},
    removeListener: () => {},
    addEventListener: () => {},
    removeEventListener: () => {},
    dispatchEvent: () => {},
  }),
});

// Mock IntersectionObserver
global.IntersectionObserver = class IntersectionObserver {
  constructor() {}
  disconnect() {}
  observe() {}
  unobserve() {}
  takeRecords() {
    return [];
  }
};

// Mock scrollIntoView
HTMLElement.prototype.scrollIntoView = vi.fn();