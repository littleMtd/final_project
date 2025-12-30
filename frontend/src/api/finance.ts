import { request } from './http'
import type { 
  CreateEntryPayload, 
  CreateTypePayload, 
  FinanceType, 
  LedgerEntry,
  Purpose,
  CreatePurposePayload,
  ReportGenerateResponse,
  LedgerResponse,
  LedgerKind
} from '../types/finance'
import type { UpdateEntryPayload } from '../types/finance'

// Insights
type InsightsResponse = { insights: string[] }

// Goals
type GoalsListResponse = {
  goals: { name: string; type: 'expense' | 'income'; target: number; target_month: string }[]
}

type GoalProgressResponse = {
  name: string
  type: 'expense' | 'income'
  target: number
  progress: number
  percentage: number
}

// Report status
type ReportStatusResponse = {
  month: string | null
  delivered: boolean
  generated_at?: string
}

// Map backend shapes to frontend types
type TypesResponse = { types: string[] }
type TotalByNameResponse = { name: string; total: number }
type TotalResponse = { total: number }
type PurposeListResponse = { goals: { name: string; type: 'expense' | 'income'; target: number; target_month: string }[] }
type ReportOverviewResponse = {
  month: string
  income: Record<string, number>
  expense: Record<string, number>
  total_income: number
  total_expense: number
  net: number
  goals?: { name: string; type: 'expense' | 'income'; target: number; progress: number; percentage: number }[]
}

export const getLedger = async (params: { kind?: LedgerKind; type?: string; page?: number; pageSize?: number } = {}): Promise<LedgerResponse> => {
  const { kind = 'all', type, page = 1, pageSize = 10 } = params
  const query = new URLSearchParams()
  if (kind) query.set('kind', kind)
  if (type) query.set('type', type)
  query.set('page', String(page))
  query.set('page_size', String(pageSize))
  return request<LedgerResponse>(`/api/ledger/?${query.toString()}`)
}

export const getExpenseTypes = async (): Promise<FinanceType[]> => {
  const res = await request<TypesResponse>('/api/expense/types/')
  return res.types.map(name => ({ id: name, name }))
}

export const getIncomeTypes = async (): Promise<FinanceType[]> => {
  const res = await request<TypesResponse>('/api/income/types/')
  return res.types.map(name => ({ id: name, name }))
}

export const getExpenseByType = async (name: string): Promise<number> => {
  const safe = encodeURIComponent(name)
  const res = await request<TotalByNameResponse>(`/api/expense/types/${safe}/`)
  return res.total
}

export const getIncomeByType = async (name: string): Promise<number> => {
  const safe = encodeURIComponent(name)
  const res = await request<TotalByNameResponse>(`/api/income/types/${safe}/`)
  return res.total
}

export const getExpenseTotal = async (): Promise<number> => {
  const res = await request<TotalResponse>('/api/expense/total/')
  return res.total
}

export const getIncomeTotal = async (): Promise<number> => {
  const res = await request<TotalResponse>('/api/income/total/')
  return res.total
}

// Goals
export const listGoals = () => request<GoalsListResponse>('/api/purpose/')

export const createGoal = (payload: { name: string; type: 'expense' | 'income'; target_amount: number; target_month?: string }) =>
  request<void>('/api/purpose/', {
    method: 'POST',
    body: JSON.stringify(payload),
    parseJson: false
  })

export const getGoalProgress = (name: string, params?: { type?: 'expense' | 'income'; month?: string }) => {
  const query = new URLSearchParams()
  if (params?.type) query.set('type', params.type)
  if (params?.month) query.set('month', params.month)
  return request<GoalProgressResponse>(`/api/purpose/${encodeURIComponent(name)}/${query.toString() ? `?${query.toString()}` : ''}`)
}

// Insights
export const getInsights = () => request<InsightsResponse>('/api/insights/')

// Report status
export const getReportStatus = () => request<ReportStatusResponse>('/api/report/status/')

export const createExpenseType = (payload: CreateTypePayload) =>
  request<void>('/api/expense/types/', {
    method: 'POST',
    body: JSON.stringify(payload),
    parseJson: false
  })

export const createIncomeType = (payload: CreateTypePayload) =>
  request<void>('/api/income/types/', {
    method: 'POST',
    body: JSON.stringify(payload),
    parseJson: false
  })

export type CreateEntryResponse = { id: number; warning?: string }

export const createExpenseEntry = (payload: CreateEntryPayload) =>
  request<CreateEntryResponse>('/api/expense/', {
    method: 'POST',
    body: JSON.stringify({
      type: payload.type,
      amount: payload.amount,
      ...(payload.date ? { entry_date: payload.date } : {})
    }),
    parseJson: true
  })

export const createIncomeEntry = (payload: CreateEntryPayload) =>
  request<CreateEntryResponse>('/api/income/', {
    method: 'POST',
    body: JSON.stringify({
      type: payload.type,
      amount: payload.amount,
      ...(payload.date ? { entry_date: payload.date } : {})
    }),
    parseJson: true
  })

export const getAllPurposes = async (): Promise<Purpose[]> => {
  const res = await request<PurposeListResponse>('/api/purpose/')
  return res.goals.map(g => ({ name: g.name, type: g.type, targetAmount: g.target }))
}

// Adjust to return minimal info used by UI; backend returns a rich object
export const getPurposeByName = (name: string) => request<object>(`/api/purpose/${name}/`)

export const createPurpose = (payload: CreatePurposePayload) =>
  request<void>('/api/purpose/', {
    method: 'POST',
    body: JSON.stringify(payload),
    parseJson: false
  })

// Backend provides report overview via GET; normalize month to first day to avoid 400 on yyyy-MM
export const generateMonthlyReport = async (month?: string): Promise<ReportGenerateResponse> => {
  const normalizedMonth = month ? (month.length === 7 ? `${month}-01` : month) : undefined
  const query = normalizedMonth ? `?month=${normalizedMonth}` : ''
  const res = await request<ReportOverviewResponse>(`/api/report/overview/${query}`)
  return {
    month: res.month?.slice(0, 7) ?? month ?? '',
    totalIncome: res.total_income,
    totalExpense: res.total_expense,
    balance: res.net,
    incomeByType: res.income,
    expenseByType: res.expense,
    goals: res.goals?.map(g => ({
      name: g.name,
      type: g.type,
      target: g.target,
      progress: g.progress,
      percentage: g.percentage,
    }))
  }
}

// Update/delete entry helpers
type UpdateEntryPayloadInternal = UpdateEntryPayload & { type?: string; amount?: number; date?: string; note?: string }

const patchEntry = (kind: 'expense' | 'income', id: number, payload: UpdateEntryPayloadInternal) => {
  const body: Record<string, unknown> = {}
  if (payload.type) body.type = payload.type
  if (payload.amount !== undefined) body.amount = payload.amount
  if (payload.date) body.entry_date = payload.date
  if (payload.note !== undefined) body.note = payload.note
  return request<void>(`/api/${kind}/${id}/`, {
    method: 'PATCH',
    body: JSON.stringify(body),
    parseJson: false
  })
}

const deleteEntry = (kind: 'expense' | 'income', id: number) =>
  request<void>(`/api/${kind}/${id}/`, { method: 'DELETE', parseJson: false })

export const updateExpenseEntry = (id: number, payload: UpdateEntryPayload) => patchEntry('expense', id, payload)
export const updateIncomeEntry = (id: number, payload: UpdateEntryPayload) => patchEntry('income', id, payload)
export const deleteExpenseEntry = (id: number) => deleteEntry('expense', id)
export const deleteIncomeEntry = (id: number) => deleteEntry('income', id)
