<template>
  <div class="finance-view">
    <header class="page-header">
      <h1>個人財經系統</h1>
      <button class="ghost" type="button" @click="refreshAll" :disabled="loadingExpense || loadingIncome" title="重新整理">
        🔄
      </button>
    </header>

    <section class="summary-section">
      <SummaryCard
        title="支出總額 "
        :amount="expenseTotal"
        :loading="loadingExpenseTotal"
        type="expense"
      />
      <SummaryCard
        title="收入總額 "
        :amount="incomeTotal"
        :loading="loadingIncomeTotal"
        type="income"
      />
      <SummaryCard title="結餘" :amount="balance" type="balance" />
    </section>

    <section class="section">
      <h2>支出類型</h2>
      <p v-if="errorExpense" class="error">{{ errorExpense }}</p>
      <div v-else-if="loadingExpense" class="loading">載入中...</div>
      <div v-else class="type-grid">
        <TypeCard
          v-for="type in expenseTypes"
          :key="type.id"
          :name="type.name"
          :icon="type.icon || '💸'"
          :amount="expenseAmounts[type.name]"
          type="expense"
          @click="fetchExpenseByType(type.name)"
        />
      </div>
    </section>

    <section class="section">
      <h2>收入類型</h2>
      <p v-if="errorIncome" class="error">{{ errorIncome }}</p>
      <div v-else-if="loadingIncome" class="loading">載入中...</div>
      <div v-else class="type-grid">
        <TypeCard
          v-for="type in incomeTypes"
          :key="type.id"
          :name="type.name"
          :icon="type.icon || '💰'"
          :amount="incomeAmounts[type.name]"
          type="income"
          @click="fetchIncomeByType(type.name)"
        />
      </div>
    </section>

    <section class="section forms">
      <EntryForm
        title="新增支出"
        :types="expenseTypes"
        :onSubmit="handleCreateExpenseEntry"
        :onCreateType="handleCreateExpenseTypeInline"
      />
      <EntryForm
        title="新增收入"
        :types="incomeTypes"
        :onSubmit="handleCreateIncomeEntry"
        :onCreateType="handleCreateIncomeTypeInline"
      />
    </section>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import SummaryCard from '@/components/SummaryCard.vue'
import TypeCard from '@/components/TypeCard.vue'
import EntryForm from '@/components/EntryForm.vue'
import { useFinanceData } from '@/composables/useFinanceData'

const {
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
} = useFinanceData()

const handleCreateExpenseTypeInline = async (name: string) => {
  await addExpenseType(name)
}

const handleCreateIncomeTypeInline = async (name: string) => {
  await addIncomeType(name)
}

const handleCreateExpenseEntry = async (data: { type: string; amount: number; date?: string }) => {
  await addExpenseEntry(data)
}

const handleCreateIncomeEntry = async (data: { type: string; amount: number; date?: string }) => {
  await addIncomeEntry(data)
}

onMounted(() => {
  refreshAll()
})
</script>

<style scoped>
.finance-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1rem 3rem;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  margin-bottom: 2rem;
}

h1 {
  margin: 0;
  color: #1f2933;
  font-size: 1.75rem;
}

.ghost {
  border: 1px solid #d1d5db;
  background: white;
  color: #374151;
  padding: 0.5rem;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1.25rem;
  min-width: 36px;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.ghost:hover:not(:disabled) {
  background: #f9fafb;
}

.ghost:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.summary-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.section {
  margin-bottom: 2.5rem;
}

h2 {
  margin: 0 0 1rem;
  color: #1f2933;
  font-size: 1.25rem;
  font-weight: 600;
}

input {
  font-size: 1rem;
  padding: 0.5rem 0.75rem;
  border-radius: 8px;
  border: 1px solid #d1d5db;
  min-width: 180px;
}

button {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 8px;
  background: #42b883;
  color: white;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.2s, transform 0.1s;
}

button:hover:not(:disabled) {
  background: #2e9b70;
}

button:active:not(:disabled) {
  transform: translateY(1px);
}

button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.type-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 0.75rem;
}

.loading {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.error {
  background: #fee;
  border: 1px solid #fcc;
  border-radius: 8px;
  padding: 0.75rem 1rem;
  color: #b91c1c;
  margin: 0.5rem 0;
}

.forms {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1rem;
}
</style>
