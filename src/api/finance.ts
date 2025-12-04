import { request } from './http'
import type { CreateEntryPayload, CreateTypePayload, FinanceType } from '../types/finance'

// GET: 類型列表
export const getExpenseTypes = () => request<FinanceType[]>('/expense/types/')
export const getIncomeTypes = () => request<FinanceType[]>('/income/types/')

// GET: 類型累計金額
export const getExpenseByType = (name: string) => request<number>(`/expense/types/${name}/`)
export const getIncomeByType = (name: string) => request<number>(`/income/types/${name}/`)

// GET: 總額
export const getExpenseTotal = () => request<number>('/expense/total/')
export const getIncomeTotal = () => request<number>('/income/total/')

// POST: 新增類型
export const createExpenseType = (payload: CreateTypePayload) =>
  request<void>('/expense/types/', {
    method: 'POST',
    body: JSON.stringify(payload),
    parseJson: false
  })

export const createIncomeType = (payload: CreateTypePayload) =>
  request<void>('/income/types/', {
    method: 'POST',
    body: JSON.stringify(payload),
    parseJson: false
  })

// POST: 新增項目
export const createExpenseEntry = (payload: CreateEntryPayload) =>
  request<void>('/expense/', {
    method: 'POST',
    body: JSON.stringify(payload),
    parseJson: false
  })

export const createIncomeEntry = (payload: CreateEntryPayload) =>
  request<void>('/income/', {
    method: 'POST',
    body: JSON.stringify(payload),
    parseJson: false
  })
