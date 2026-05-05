/**
 * Input sanitization utility for XSS prevention
 * Uses DOMPurify to safely sanitize user input
 */

import DOMPurify from 'dompurify';

/**
 * Sanitize a string to prevent XSS attacks
 * Removes any HTML tags and potentially dangerous content
 * 
 * @param input - Raw user input string
 * @returns Sanitized string safe for display
 */
export function sanitizeInput(input: string): string {
  if (!input || typeof input !== 'string') {
    return '';
  }
  
  // Use DOMPurify to clean the input - strips all HTML tags
  const cleaned = DOMPurify.sanitize(input);
  return cleaned;
}

/**
 * Sanitize HTML content while preserving safe tags
 * Use this for rich text content that should allow some formatting
 * 
 * @param html - Raw HTML string
 * @returns Sanitized HTML string
 */
export function sanitizeHtml(html: string): string {
  if (!html || typeof html !== 'string') {
    return '';
  }
  
  // Allow only safe HTML tags for basic formatting
  const safeTags = ['b', 'i', 'em', 'strong', 'br', 'p', 'ul', 'ol', 'li', 'span'];
  return DOMPurify.sanitize(html, { ALLOWED_TAGS: safeTags });
}

/**
 * Strip all special characters except safe ones
 * Use for simple text inputs like names
 * 
 * @param input - Raw input string
 * @returns Sanitized string with only safe characters
 */
export function sanitizeName(input: string): string {
  if (!input || typeof input !== 'string') {
    return '';
  }
  
  // Remove any characters that could be used for injection
  // Keep only letters (including unicode), numbers, spaces, hyphens, apostrophes
  return input.replace(/[^\w\s\-''ঀ-৿À-ÿ]/g, '').trim();
}

/**
 * Validate and sanitize a phone number
 * 
 * @param phone - Raw phone number string
 * @returns Sanitized phone number or empty string
 */
export function sanitizePhone(phone: string): string {
  if (!phone || typeof phone !== 'string') {
    return '';
  }
  
  // Bangladesh phone format: 01XXXXXXXXX (11 digits starting with 01)
  // Allow only digits and + prefix
  const cleaned = phone.replace(/[^\d\+]/g, '');
  
  // Validate Bangladeshi phone number
  if (/^(\+880|0|)?1[3-9]\d{9}$/.test(cleaned)) {
    return cleaned;
  }
  
  return '';
}

/**
 * Validate email format
 * 
 * @param email - Raw email string
 * @returns Valid email or empty string
 */
export function sanitizeEmail(email: string): string {
  if (!email || typeof email !== 'string') {
    return '';
  }
  
  // Basic email validation
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  const cleaned = email.trim().toLowerCase();
  
  if (emailRegex.test(cleaned)) {
    return cleaned;
  }
  
  return '';
}
