import { request } from './http'
import type {
  LoginPayload,
  RegisterPayload
} from '../types/auth'

export const login = (payload: LoginPayload) =>
  request<void>('/signup/', {
    method: 'POST',
    body: JSON.stringify(payload),
    parseJson: false
  })

export const register = (payload: RegisterPayload) =>
  request<void>('/signin/', {
    method: 'POST',
    body: JSON.stringify(payload),
    parseJson: false
  })
