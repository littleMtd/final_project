import { computed, ref } from 'vue'
import {
  createExpenseEntry,
  createExpenseType,
  createIncomeEntry,
  createIncomeType,
  getExpenseByType,
  getExpenseTotal,
  getExpenseTypes,
  getIncomeByType,
  getIncomeTotal,
  getIncomeTypes
} from '@/api/finance'
import type { FinanceType } from '@/types/finance'

type AmountMap = Record<string, number>

export function useFinanceData() {
  const expenseTypes = ref<FinanceType[]>([])
  const incomeTypes = ref<FinanceType[]>([])
  const expenseAmounts = ref<AmountMap>({})
  const incomeAmounts = ref<AmountMap>({})
  const expenseTotal = ref(0)
  const incomeTotal = ref(0)

  const loadingExpense = ref(false)
  const loadingIncome = ref(false)
  const loadingExpenseTotal = ref(false)
  const loadingIncomeTotal = ref(false)
  const errorExpense = ref<string | null>(null)
  const errorIncome = ref<string | null>(null)

  const balance = computed(() => incomeTotal.value - expenseTotal.value)

  const fetchExpenseTypes = async () => {
    loadingExpense.value = true
    errorExpense.value = null
    try {
      expenseTypes.value = await getExpenseTypes()
    } catch (err) {
      errorExpense.value = err instanceof Error ? err.message : '無法取得支出類型'
    } finally {
      loadingExpense.value = false
    }
  }

  const fetchIncomeTypes = async () => {
    loadingIncome.value = true
    errorIncome.value = null
    try {
      incomeTypes.value = await getIncomeTypes()
    } catch (err) {
      errorIncome.value = err instanceof Error ? err.message : '無法取得收入類型'
    } finally {
      loadingIncome.value = false
    }
  }

  const fetchExpenseByType = async (typeName: string) => {
    try {
      const amount = await getExpenseByType(typeName)
      expenseAmounts.value = { ...expenseAmounts.value, [typeName]: amount }
    } catch (err) {
      console.error(`Failed to fetch expense for ${typeName}:`, err)
    }
  }

  const fetchIncomeByType = async (typeName: string) => {
    try {
      const amount = await getIncomeByType(typeName)
      incomeAmounts.value = { ...incomeAmounts.value, [typeName]: amount }
    } catch (err) {
      console.error(`Failed to fetch income for ${typeName}:`, err)
    }
  }

  const fetchExpenseTotal = async () => {
    loadingExpenseTotal.value = true
    try {
      expenseTotal.value = await getExpenseTotal()
    } catch (err) {
      console.error('Failed to fetch expense total:', err)
      expenseTotal.value = 0
    } finally {
      loadingExpenseTotal.value = false
    }
  }

  const fetchIncomeTotal = async () => {
    loadingIncomeTotal.value = true
    try {
      incomeTotal.value = await getIncomeTotal()
    } catch (err) {
      console.error('Failed to fetch income total:', err)
      incomeTotal.value = 0
    } finally {
      loadingIncomeTotal.value = false
    }
  }

  const addExpenseType = async (name: string) => {
    await createExpenseType({ name })
    await fetchExpenseTypes()
  }

  const addIncomeType = async (name: string) => {
    await createIncomeType({ name })
    await fetchIncomeTypes()
  }

  const addExpenseEntry = async (data: { type: string; amount: number; date?: string }) => {
    await createExpenseEntry(data)
    await Promise.all([fetchExpenseTotal(), fetchExpenseByType(data.type)])
  }

  const addIncomeEntry = async (data: { type: string; amount: number; date?: string }) => {
    await createIncomeEntry(data)
    await Promise.all([fetchIncomeTotal(), fetchIncomeByType(data.type)])
  }

  const refreshAll = async () => {
    await Promise.all([fetchExpenseTypes(), fetchIncomeTypes(), fetchExpenseTotal(), fetchIncomeTotal()])
  }

  return {
    expenseTypes,
    incomeTypes,
    expenseAmounts,
    incomeAmounts,
    expenseTotal,
    incomeTotal,
    loadingExpense,
    loadingIncome,
    loadingExpenseTotal,
    loadingIncomeTotal,
    errorExpense,
    errorIncome,
    balance,
    fetchExpenseByType,
    fetchIncomeByType,
    addExpenseType,
    addIncomeType,
    addExpenseEntry,
    addIncomeEntry,
    refreshAll
  }
}
