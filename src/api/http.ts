const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || ''

export type RequestOptions = RequestInit & {
  parseJson?: boolean
}

export async function request<T>(path: string, options: RequestOptions = {}): Promise<T> {
  const { parseJson = true, headers, ...rest } = options

  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(headers || {})
    },
    ...rest
  })

  if (!response.ok) {
    throw new Error(`Request failed: ${response.status} ${response.statusText}`)
  }

  const hasBody =
    response.status !== 204 &&
    response.status !== 202 &&
    response.headers.get('Content-Length') !== '0'

  if (!parseJson || !hasBody) {
    return undefined as T
  }

  return response.json() as Promise<T>
}
