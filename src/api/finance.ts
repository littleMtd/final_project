import { request } from './http'
import type { 
  CreateEntryPayload, 
  CreateTypePayload, 
  FinanceType, 
  Purpose,
  CreatePurposePayload,
  ReportGenerateResponse
} from '../types/finance'

export const getExpenseTypes = () => request<FinanceType[]>('/expense/types/')
export const getIncomeTypes = () => request<FinanceType[]>('/income/types/')

export const getExpenseByType = (name: string) => request<number>(`/expense/types/${name}/`)
export const getIncomeByType = (name: string) => request<number>(`/income/types/${name}/`)

export const getExpenseTotal = () => request<number>('/expense/total/')
export const getIncomeTotal = () => request<number>('/income/total/')

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

export const getAllPurposes = () => request<string[]>('/purpose/')

export const getPurposeByName = (name: string) => request<number>(`/purpose/${name}/`)

export const createPurpose = (payload: CreatePurposePayload) =>
  request<void>('/purpose/', {
    method: 'POST',
    body: JSON.stringify(payload),
    parseJson: false
  })

export const generateMonthlyReport = () => 
  request<ReportGenerateResponse>('/report/generate/', {
    method: 'POST'
  })
