// Base URL for API requests. Prefer setting VITE_API_BASE_URL in env.
// Defaults to empty so paths should include '/api' explicitly.
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || ''

export type RequestOptions = RequestInit & {
  parseJson?: boolean
}

// Custom error types for better error handling
export class ApiError extends Error {
  constructor(
    message: string,
    public status: number,
    public code?: string,
    public details?: any
  ) {
    super(message)
    this.name = 'ApiError'
  }
}

export class NetworkError extends Error {
  constructor(message: string = 'Network connection failed') {
    super(message)
    this.name = 'NetworkError'
  }
}

export class ValidationError extends ApiError {
  constructor(message: string, details?: any) {
    super(message, 400, 'VALIDATION_ERROR', details)
    this.name = 'ValidationError'
  }
}

export class AuthenticationError extends ApiError {
  constructor(message: string = 'Authentication required') {
    super(message, 401, 'AUTH_ERROR')
    this.name = 'AuthenticationError'
  }
}

function getCookie(name: string): string | null {
  const value = `; ${document.cookie}`
  const parts = value.split(`; ${name}=`)
  if (parts.length === 2) return parts.pop()?.split(';').shift() || null
  return null
}

export async function request<T>(path: string, options: RequestOptions = {}): Promise<T> {
  const { parseJson = true, headers, ...rest } = options
  let csrfToken = getCookie('csrftoken')

  const method = (options.method || 'GET').toUpperCase()
  const isWrite = !method.match(/^(GET|HEAD|OPTIONS)$/)

  // Pre-fetch CSRF cookie if missing for write operations
  if (isWrite && !csrfToken) {
    try {
      await fetch('/api/csrf/', { credentials: 'include' })
      csrfToken = getCookie('csrftoken')
    } catch {
      // ignore prefetch errors; server may still accept if exempt
    }
  }

  let response: Response
  try {
    response = await fetch(`${API_BASE_URL}${path}`, {
      headers: {
        'Content-Type': 'application/json',
        ...(csrfToken && isWrite ? { 'X-CSRFToken': csrfToken } : {}),
        ...(headers || {})
      },
      credentials: 'include',
      ...rest
    })
  } catch (err) {
    // Network errors (no internet, CORS, etc.)
    throw new NetworkError(err instanceof Error ? err.message : 'Network request failed')
  }

  if (!response.ok) {
    let message = `Request failed: ${response.status} ${response.statusText}`
    let details: any = undefined
    
    try {
      const contentType = response.headers.get('Content-Type') || ''
      if (contentType.includes('application/json')) {
        const data = await response.json()
        message = (data?.error || data?.message || message)
        details = data?.errors || data?.details
      } else {
        const text = await response.text()
        if (text) message = text
      }
    } catch {
      // ignore parse errors and use default message
    }
    
    // Throw specific error types based on status code
    if (response.status === 401) {
      throw new AuthenticationError(message)
    } else if (response.status === 400) {
      throw new ValidationError(message, details)
    } else {
      throw new ApiError(message, response.status, undefined, details)
    }
  }

  const hasBody =
    response.status !== 204 &&
    response.headers.get('Content-Length') !== '0'

  if (!parseJson || !hasBody) {
    return undefined as T
  }

  return response.json() as Promise<T>
}
