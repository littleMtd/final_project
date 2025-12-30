import { ref, computed } from 'vue'
import {
  getExpenseTypes,
  getIncomeTypes,
  getExpenseByType,
  getIncomeByType,
  getExpenseTotal,
  getIncomeTotal,
  listGoals,
  createGoal,
  createExpenseType,
  createIncomeType,
  createExpenseEntry,
  createIncomeEntry
} from '@/api/finance'
import type { FinanceType } from '@/types/finance'

export function useFinanceData() {
  const expenseTypes = ref<FinanceType[] | null>(null)
  const incomeTypes = ref<FinanceType[] | null>(null)

  const expenseAmounts = ref<Record<string, number>>({})
  const incomeAmounts = ref<Record<string, number>>({})

  const expenseTotal = ref(0)
  const incomeTotal = ref(0)

  const goals = ref<{
    name: string
    type: 'expense' | 'income'
    target: number
    target_month?: string
    progress?: number
    percentage?: number
  }[]>([])

  const loadingExpense = ref(false)
  const loadingIncome = ref(false)
  const loadingGoals = ref(false)
  const loadingExpenseTotal = ref(false)
  const loadingIncomeTotal = ref(false)

  const errorExpense = ref<string | null>(null)
  const errorIncome = ref<string | null>(null)
  const errorGoals = ref<string | null>(null)

  const balance = computed(() => incomeTotal.value - expenseTotal.value)

  async function loadExpense() {
    loadingExpense.value = true
    errorExpense.value = null
    try {
      const types = await getExpenseTypes()
      expenseTypes.value = types
      const names = (types || []).map(t => t.name)
      const amounts = await Promise.all(names.map(n => getExpenseByType(n)))
      const next: Record<string, number> = {}
      names.forEach((n, i) => { next[n] = amounts[i] || 0 })
      expenseAmounts.value = next
    } catch (err) {
      errorExpense.value = err instanceof Error ? err.message : '載入支出資料失敗'
    } finally {
      loadingExpense.value = false
    }

    loadingExpenseTotal.value = true
    try {
      expenseTotal.value = await getExpenseTotal()
    } finally {
      loadingExpenseTotal.value = false
    }
  }

  async function loadIncome() {
    loadingIncome.value = true
    errorIncome.value = null
    try {
      const types = await getIncomeTypes()
      incomeTypes.value = types
      const names = (types || []).map(t => t.name)
      const amounts = await Promise.all(names.map(n => getIncomeByType(n)))
      const next: Record<string, number> = {}
      names.forEach((n, i) => { next[n] = amounts[i] || 0 })
      incomeAmounts.value = next
    } catch (err) {
      errorIncome.value = err instanceof Error ? err.message : '載入收入資料失敗'
    } finally {
      loadingIncome.value = false
    }

    loadingIncomeTotal.value = true
    try {
      incomeTotal.value = await getIncomeTotal()
    } finally {
      loadingIncomeTotal.value = false
    }
  }

  async function loadGoals() {
    loadingGoals.value = true
    errorGoals.value = null
    try {
      const res = await listGoals()
      goals.value = res.goals?.map(g => ({
        name: g.name,
        type: g.type,
        target: g.target,
        target_month: g.target_month,
        progress: (g as any).progress,
        percentage: (g as any).percentage
      })) || []
    } catch (err) {
      errorGoals.value = err instanceof Error ? err.message : '無法載入目標'
    } finally {
      loadingGoals.value = false
    }
  }

  async function refreshAll() {
    await Promise.all([loadExpense(), loadIncome(), loadGoals()])
  }

  async function addGoal(payload: { name: string; type: 'expense' | 'income'; target_amount: number; target_month?: string }) {
    await createGoal(payload)
    await loadGoals()
  }

  async function addExpenseType(payload: { name: string }) {
    await createExpenseType(payload)
    await loadExpense()
  }

  async function addIncomeType(payload: { name: string }) {
    await createIncomeType(payload)
    await loadIncome()
  }

  async function addExpenseEntry(payload: { type: string; amount: number; date?: string }) {
    const res = await createExpenseEntry(payload)
    await Promise.all([loadExpense(), loadGoals()])
    return res
  }

  async function addIncomeEntry(payload: { type: string; amount: number; date?: string }) {
    const res = await createIncomeEntry(payload)
    await Promise.all([loadIncome(), loadGoals()])
    return res
  }

  return {
    expenseTypes,
    incomeTypes,
    expenseAmounts,
    incomeAmounts,
    expenseTotal,
    incomeTotal,
    goals,
    loadingExpense,
    loadingIncome,
    loadingGoals,
    loadingExpenseTotal,
    loadingIncomeTotal,
    errorExpense,
    errorIncome,
    errorGoals,
    balance,
    refreshAll,
    addGoal,
    addExpenseType,
    addIncomeType,
    addExpenseEntry,
    addIncomeEntry
  }
}
