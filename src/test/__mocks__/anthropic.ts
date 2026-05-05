import { vi } from 'vitest';

/**
 * Shared mock for the anthropic service
 * This ensures consistent mocking across all test files
 */
export const callClaude = vi.fn().mockResolvedValue({
  replyText: 'This is a test response from the AI assistant.',
  updatedHistory: [],
});
