export type AuthUser = {
  id: string
  username: string
  name?: string
}

export type AuthResponse = {
  token: string
  user: AuthUser
}

export type LoginPayload = {
  username: string
  password: string
}

export type RegisterPayload = {
  username: string
  password: string
  name?: string
}

export type AuthSuccessResponse = {
  status: number
}
