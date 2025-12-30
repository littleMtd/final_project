<template>
  <section class="section report-section">
    <div class="section-heading">
      <div>
        <h2 class="section-title">每月報表</h2>
      </div>
      <div class="report-controls">
        <input
          :value="selectedMonth"
          @input="$emit('update:selectedMonth', ($event.target as HTMLInputElement).value)"
          type="month"
          :max="currentMonth"
        />
        <button type="button" @click="$emit('fetch-report')" :disabled="loading">
          {{ loading ? '載入中..' : '查詢' }}
        </button>
      </div>
    </div>
    <p v-if="error" class="error">{{ error }}</p>
    <div v-else-if="report" class="report-content">
      <div class="report-summary-inline">
        <span class="report-item"><strong>月份</strong> {{ report.month }}</span>
        <span class="report-item"><strong>總收入</strong> NT$ {{ report.totalIncome.toLocaleString() }}</span>
        <span class="report-item"><strong>總支出</strong> NT$ {{ report.totalExpense.toLocaleString() }}</span>
        <span class="report-item balance" :class="{ negative: report.balance < 0 }">
          <strong>結餘</strong> NT$ {{ report.balance.toLocaleString() }}
        </span>
      </div>
      <div class="report-detail-grid">
        <div class="detail-block">
          <h4>收入明細</h4>
          <table v-if="Object.keys(report.incomeByType).length > 0" class="detail-table">
            <tbody>
              <tr v-for="(amount, type) in report.incomeByType" :key="type">
                <td class="type-cell">{{ type }}</td>
                <td class="amount-cell">NT$ {{ amount.toLocaleString() }}</td>
              </tr>
            </tbody>
          </table>
          <p v-else class="empty-text">沒有收入資料</p>
        </div>
        <div class="detail-block">
          <h4>支出明細</h4>
          <table v-if="Object.keys(report.expenseByType).length > 0" class="detail-table">
            <tbody>
              <tr v-for="(amount, type) in report.expenseByType" :key="type">
                <td class="type-cell">{{ type }}</td>
                <td class="amount-cell">NT$ {{ amount.toLocaleString() }}</td>
              </tr>
            </tbody>
          </table>
          <p v-else class="empty-text">沒有支出資料</p>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface MonthlyReport {
  month: string
  totalIncome: number
  totalExpense: number
  balance: number
  incomeByType: Record<string, number>
  expenseByType: Record<string, number>
}

const props = defineProps<{
  report: MonthlyReport | null
  loading: boolean
  error: string
  selectedMonth: string
}>()

defineEmits<{
  'fetch-report': []
  'update:selectedMonth': [value: string]
}>()

const currentMonth = computed(() => {
  const now = new Date()
  return `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}`
})
</script>

<style scoped>
.section {
  background: #ffffff;
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 2rem;
  border: 1px solid #e0e0e0;
}

.section-heading {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.section-title {
  font-size: 1.25rem;
  margin: 0;
  color: #333;
}

.report-controls {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.report-controls input {
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.report-controls button {
  padding: 0.5rem 1rem;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.report-controls button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.error {
  color: #ef4444;
  margin: 0.5rem 0;
}

.report-summary-inline {
  display: flex;
  gap: 1.5rem;
  flex-wrap: wrap;
  padding: 1rem;
  background: #f9fafb;
  border-radius: 6px;
  margin-bottom: 1.5rem;
}

.report-item {
  display: flex;
  gap: 0.5rem;
}

.report-item.balance {
  color: #22c55e;
}

.report-item.balance.negative {
  color: #ef4444;
}

.report-detail-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.detail-block h4 {
  margin: 0 0 0.75rem 0;
  color: #555;
  font-size: 1rem;
}

.detail-table {
  width: 100%;
  border-collapse: collapse;
}

.detail-table td {
  padding: 0.5rem;
  border-bottom: 1px solid #f0f0f0;
}

.type-cell {
  color: #666;
}

.amount-cell {
  text-align: right;
  font-weight: 500;
}

.empty-text {
  color: #999;
  font-style: italic;
  text-align: center;
  padding: 1rem;
}
</style>
