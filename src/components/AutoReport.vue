<template>
  <section v-if="report" class="section auto-report-section">
    <div class="section-heading">
      <div>
        <h2 class="section-title">上月自動報表</h2>
      </div>
      <div class="auto-report-actions">
        <button 
          type="button" 
          class="ghost" 
          @click="$emit('refresh')" 
          :disabled="loadingStatus || downloadingPDF"
        >
          {{ loadingStatus ? '更新中..' : '重新整理' }}
        </button>
        <button 
          type="button" 
          class="download-pdf-btn" 
          @click="handleDownloadPDF" 
          :disabled="downloadingPDF"
        >
          {{ downloadingPDF ? '匯出中..' : '下載 PDF' }}
        </button>
      </div>
    </div>
    <div class="auto-report-content" id="auto-report-content">
      <p class="report-meta">產生時間：{{ formatDateTime(report.generatedAt) }}</p>
      <div class="report-summary-inline">
        <strong>{{ report.month }} 財務總覽</strong>
        <span class="report-item">
          <strong>總收入</strong> NT$ {{ report.report.totalIncome.toLocaleString() }}
        </span>
        <span class="report-item">
          <strong>總支出</strong> NT$ {{ report.report.totalExpense.toLocaleString() }}
        </span>
        <span class="report-item balance" :class="{ negative: report.report.balance < 0 }">
          <strong>結餘</strong> NT$ {{ report.report.balance.toLocaleString() }}
        </span>
      </div>
      <div class="analysis-box">
        <h4>財務分析</h4>
        <p>{{ report.summary }}</p>
      </div>
      <div class="breakdown-grid">
        <div class="breakdown-block">
          <h4>收入明細</h4>
          <table v-if="Object.keys(report.report.incomeByType).length > 0" class="breakdown-table">
            <tbody>
              <tr v-for="(amount, type) in report.report.incomeByType" :key="type">
                <td class="type-cell">{{ type }}</td>
                <td class="amount-cell">NT$ {{ amount.toLocaleString() }}</td>
                <td class="percent-cell">{{ formatPercent(amount, report.report.totalIncome) }}%</td>
              </tr>
            </tbody>
          </table>
          <p v-else class="empty-text">沒有收入資料</p>
        </div>
        <div class="breakdown-block">
          <h4>支出明細</h4>
          <table v-if="Object.keys(report.report.expenseByType).length > 0" class="breakdown-table">
            <tbody>
              <tr v-for="(amount, type) in report.report.expenseByType" :key="type">
                <td class="type-cell">{{ type }}</td>
                <td class="amount-cell">NT$ {{ amount.toLocaleString() }}</td>
                <td class="percent-cell">{{ formatPercent(amount, report.report.totalExpense) }}%</td>
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
import { ref } from 'vue'

interface AutoReport {
  month: string
  generatedAt: string
  summary: string
  report: {
    totalIncome: number
    totalExpense: number
    balance: number
    incomeByType: Record<string, number>
    expenseByType: Record<string, number>
  }
}

const props = defineProps<{
  report: AutoReport | null
  loadingStatus: boolean
}>()

const emit = defineEmits<{
  refresh: []
  'download-pdf': []
}>()

const downloadingPDF = ref(false)

const formatDateTime = (isoString: string) => {
  return new Date(isoString).toLocaleString('zh-TW')
}

const formatPercent = (value: number, total: number) => {
  if (total === 0) return '0.0'
  return ((value / total) * 100).toFixed(1)
}

const handleDownloadPDF = async () => {
  downloadingPDF.value = true
  try {
    emit('download-pdf')
    // Wait a bit for the PDF generation
    await new Promise(resolve => setTimeout(resolve, 2000))
  } finally {
    downloadingPDF.value = false
  }
}
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

.auto-report-actions {
  display: flex;
  gap: 0.5rem;
}

button.ghost {
  background: transparent;
  border: 1px solid #ddd;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
}

button.ghost:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.download-pdf-btn {
  background: #22c55e;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
}

.download-pdf-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.auto-report-content {
  padding: 1rem;
  background: #f9fafb;
  border-radius: 8px;
}

.report-meta {
  color: #999;
  font-size: 0.875rem;
  margin: 0 0 1rem 0;
}

.report-summary-inline {
  display: flex;
  gap: 1.5rem;
  flex-wrap: wrap;
  padding: 1rem;
  background: white;
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

.analysis-box {
  background: white;
  border-radius: 6px;
  padding: 1rem;
  margin-bottom: 1.5rem;
}

.analysis-box h4 {
  margin: 0 0 0.75rem 0;
  color: #555;
  font-size: 1rem;
}

.analysis-box p {
  margin: 0;
  line-height: 1.6;
  color: #666;
}

.breakdown-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.breakdown-block {
  background: white;
  border-radius: 6px;
  padding: 1rem;
}

.breakdown-block h4 {
  margin: 0 0 0.75rem 0;
  color: #555;
  font-size: 1rem;
}

.breakdown-table {
  width: 100%;
  border-collapse: collapse;
}

.breakdown-table td {
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

.percent-cell {
  text-align: right;
  color: #999;
  font-size: 0.875rem;
}

.empty-text {
  color: #999;
  font-style: italic;
  text-align: center;
  padding: 1rem;
}
</style>
