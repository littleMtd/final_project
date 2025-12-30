/**
 * Input sanitization utilities to prevent XSS attacks
 */

/**
 * Sanitize user input by removing potentially dangerous HTML/script content
 * Use this for user-generated content that might be displayed
 */
export function sanitizeText(input: string): string {
  if (!input) return ''
  
  // Remove HTML tags and script content
  return input
    .replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '')
    .replace(/<[^>]+>/g, '')
    .trim()
}

/**
 * Escape HTML special characters to prevent XSS
 * Vue 3 automatically escapes interpolations, but use this for v-html or manual DOM manipulation
 */
export function escapeHtml(input: string): string {
  if (!input) return ''
  
  const div = document.createElement('div')
  div.textContent = input
  return div.innerHTML
}

/**
 * Validate and sanitize username
 * Only allow alphanumeric, underscore, dash
 */
export function sanitizeUsername(username: string): string {
  if (!username) return ''
  
  // Remove non-alphanumeric characters except underscore and dash
  return username
    .replace(/[^a-zA-Z0-9_-]/g, '')
    .slice(0, 150) // Django default max length
}

/**
 * Sanitize number inputs
 */
export function sanitizeNumber(input: string | number): number {
  const num = typeof input === 'string' ? parseFloat(input) : input
  return isNaN(num) ? 0 : num
}

/**
 * Validate email format (basic)
 */
export function isValidEmail(email: string): boolean {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return emailRegex.test(email)
}

/**
 * Sanitize and validate amount input for financial entries
 */
export function sanitizeAmount(input: string | number): number {
  let num = typeof input === 'string' ? parseFloat(input.replace(/[^0-9.-]/g, '')) : input
  
  if (isNaN(num)) num = 0
  
  // Limit to 2 decimal places
  return Math.round(num * 100) / 100
}

/**
 * Sanitize note/description fields
 * Remove scripts but preserve basic formatting
 */
export function sanitizeNote(note: string, maxLength: number = 255): string {
  if (!note) return ''
  
  return note
    .replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '')
    .replace(/<iframe\b[^<]*(?:(?!<\/iframe>)<[^<]*)*<\/iframe>/gi, '')
    .replace(/javascript:/gi, '')
    .replace(/on\w+\s*=/gi, '') // Remove event handlers like onclick=
    .slice(0, maxLength)
    .trim()
}
