import { request } from './http'
import type {
  LoginPayload,
  RegisterPayload,
  LoginResponse,
  SignupResponse,
  MeResponse
} from '../types/auth'

export const login = (payload: LoginPayload) =>
  request<LoginResponse>('/api/signin/', {
    method: 'POST',
    body: JSON.stringify(payload)
  })

export const register = (payload: RegisterPayload) =>
  request<SignupResponse>('/api/signup/', {
    method: 'POST',
    body: JSON.stringify(payload)
  })

export const logout = () =>
  request<{ message: string }>('/api/signout/', {
    method: 'POST'
  })

export const getMe = () =>
  request<MeResponse>('/api/me/', {
    method: 'GET'
  })
