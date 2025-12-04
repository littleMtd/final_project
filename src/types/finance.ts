export type FinanceType = {
  id: string
  name: string
  icon?: string
}

export type CreateTypePayload = {
  name: string
}

export type CreateEntryPayload = {
  type: string
  amount: number
  date?: string
}
