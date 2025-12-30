export type AuthUser = {
  id: number
  username: string
  email?: string
}

// Unified API response format
export type ApiResponse<T> = {
  success: true
  data?: T
  message?: string
}

export type LoginResponse = ApiResponse<{ user: AuthUser }>

export type SignupResponse = ApiResponse<{ user: AuthUser }>

export type MeResponse = ApiResponse<{ user: AuthUser }>

export type LoginPayload = {
  username: string
  password: string
}

export type RegisterPayload = {
  username: string
  password: string
  email?: string
}
