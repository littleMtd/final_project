<template>
  <div class="finance-view">
    <header class="page-header">
      <div class="header-left">
        <h1>個人財經系統</h1>
      </div>
      <div class="header-right">
        <div class="user-info">
          <span class="user-icon">👤</span>
          <span class="user-name">{{ user?.name || user?.username || '使用者' }}</span>
        </div>
        <button class="ghost" type="button" @click="refreshAll" :disabled="loadingExpense || loadingIncome" title="重新整理">
          🔄
        </button>
        <button class="logout-btn" type="button" @click="handleLogout" title="登出">
          登出
        </button>
      </div>
    </header>

    <!-- 總覽 -->
    <section class="summary-section">
      <div class="summary-card expense">
        <h3>支出</h3>
        <p v-if="!loadingExpenseTotal" class="amount">NT$ {{ expenseTotal.toLocaleString() }}</p>
        <p v-else class="loading-text">載入中...</p>
      </div>
      <div class="summary-card income">
        <h3>收入</h3>
        <p v-if="!loadingIncomeTotal" class="amount">NT$ {{ incomeTotal.toLocaleString() }}</p>
        <p v-else class="loading-text">載入中...</p>
      </div>
      <div class="summary-card balance">
        <h3>結餘</h3>
        <p class="amount" :class="{ negative: balance < 0 }">NT$ {{ balance.toLocaleString() }}</p>
      </div>
    </section>

    <!-- 支出類型 -->
    <section class="section">
      <h2>支出類型</h2>
      <p v-if="errorExpense" class="error">{{ errorExpense }}</p>
      <div v-else-if="loadingExpense" class="loading">載入中...</div>
      <div v-else class="type-grid">
        <div
          v-for="type in expenseTypes"
          :key="type.id"
          class="type-card"
          @click="fetchExpenseByType(type.name)"
        >
          <span class="icon">{{ type.icon || '💸' }}</span>
          <span class="name">{{ type.name }}</span>
          <span v-if="expenseAmounts[type.name] !== undefined" class="amount-badge">
            NT$ {{ expenseAmounts[type.name].toLocaleString() }}
          </span>
        </div>
      </div>
    </section>

    <!-- 收入類型 -->
    <section class="section">
      <h2>收入類型</h2>
      <p v-if="errorIncome" class="error">{{ errorIncome }}</p>
      <div v-else-if="loadingIncome" class="loading">載入中...</div>
      <div v-else class="type-grid">
        <div
          v-for="type in incomeTypes"
          :key="type.id"
          class="type-card"
          @click="fetchIncomeByType(type.name)"
        >
          <span class="icon">{{ type.icon || '💰' }}</span>
          <span class="name">{{ type.name }}</span>
          <span v-if="incomeAmounts[type.name] !== undefined" class="amount-badge income-badge">
            NT$ {{ incomeAmounts[type.name].toLocaleString() }}
          </span>
        </div>
      </div>
    </section>

    <!-- 新增表單 -->
    <section class="section forms">
      <!-- 新增支出 -->
      <div class="form-card">
        <h3>新增支出</h3>
        <form @submit.prevent="submitExpense">
          <label>
            類型
            <div class="type-select-group">
              <select v-model="expenseForm.type" :disabled="expenseLoading || addingExpenseType" required>
                <option value="" disabled>請選擇</option>
                <option v-for="type in expenseTypes" :key="type.id" :value="type.name">
                  {{ type.name }}
                </option>
              </select>
              <button
                type="button"
                class="add-type-btn"
                @click="addingExpenseType = !addingExpenseType"
                :disabled="expenseLoading"
                :title="addingExpenseType ? '取消' : '新增類型'"
              >
                {{ addingExpenseType ? '✕' : '+' }}
              </button>
            </div>
            <div v-if="addingExpenseType" class="new-type-input">
              <input
                v-model.trim="newExpenseTypeName"
                type="text"
                placeholder="輸入新類型名稱"
                :disabled="creatingExpenseType"
                @keyup.enter="createExpenseType"
                @keyup.esc="addingExpenseType = false"
              />
              <button
                type="button"
                class="create-type-btn"
                @click="createExpenseType"
                :disabled="creatingExpenseType || !newExpenseTypeName"
              >
                {{ creatingExpenseType ? '...' : '確認' }}
              </button>
            </div>
          </label>
          <label>
            金額
            <input
              v-model.number="expenseForm.amount"
              type="number"
              min="1"
              step="1"
              :disabled="expenseLoading"
              placeholder="例如 120"
              required
            />
          </label>
          <label>
            日期 (選填)
            <input v-model="expenseForm.date" type="date" :disabled="expenseLoading" />
          </label>
          <button type="submit" :disabled="expenseLoading">
            {{ expenseLoading ? '送出中...' : '送出' }}
          </button>
          <p v-if="expenseError" class="error small">{{ expenseError }}</p>
          <p v-if="expenseSuccess" class="success small">{{ expenseSuccess }}</p>
        </form>
      </div>

      <!-- 新增收入 -->
      <div class="form-card">
        <h3>新增收入</h3>
        <form @submit.prevent="submitIncome">
          <label>
            類型
            <div class="type-select-group">
              <select v-model="incomeForm.type" :disabled="incomeLoading || addingIncomeType" required>
                <option value="" disabled>請選擇</option>
                <option v-for="type in incomeTypes" :key="type.id" :value="type.name">
                  {{ type.name }}
                </option>
              </select>
              <button
                type="button"
                class="add-type-btn"
                @click="addingIncomeType = !addingIncomeType"
                :disabled="incomeLoading"
                :title="addingIncomeType ? '取消' : '新增類型'"
              >
                {{ addingIncomeType ? '✕' : '+' }}
              </button>
            </div>
            <div v-if="addingIncomeType" class="new-type-input">
              <input
                v-model.trim="newIncomeTypeName"
                type="text"
                placeholder="輸入新類型名稱"
                :disabled="creatingIncomeType"
                @keyup.enter="createIncomeType"
                @keyup.esc="addingIncomeType = false"
              />
              <button
                type="button"
                class="create-type-btn"
                @click="createIncomeType"
                :disabled="creatingIncomeType || !newIncomeTypeName"
              >
                {{ creatingIncomeType ? '...' : '確認' }}
              </button>
            </div>
          </label>
          <label>
            金額
            <input
              v-model.number="incomeForm.amount"
              type="number"
              min="1"
              step="1"
              :disabled="incomeLoading"
              placeholder="例如 120"
              required
            />
          </label>
          <label>
            日期 (選填)
            <input v-model="incomeForm.date" type="date" :disabled="incomeLoading" />
          </label>
          <button type="submit" :disabled="incomeLoading">
            {{ incomeLoading ? '送出中...' : '送出' }}
          </button>
          <p v-if="incomeError" class="error small">{{ incomeError }}</p>
          <p v-if="incomeSuccess" class="success small">{{ incomeSuccess }}</p>
        </form>
      </div>
    </section>

    <!-- 每月報表 -->
    <section class="section">
      <h2>每月報表</h2>
      <div class="report-controls">
        <input v-model="selectedMonth" type="month" :max="currentMonth" />
        <button type="button" @click="fetchReport" :disabled="loadingReport">
          {{ loadingReport ? '載入中...' : '查詢' }}
        </button>
      </div>
      <p v-if="reportError" class="error">{{ reportError }}</p>
      <div v-else-if="monthlyReport" class="report-content">
        <div class="report-summary">
          <div class="report-item">
            <span class="label">月份</span>
            <span class="value">{{ monthlyReport.month }}</span>
          </div>
          <div class="report-item income-item">
            <span class="label">總收入</span>
            <span class="value">NT$ {{ monthlyReport.totalIncome.toLocaleString() }}</span>
          </div>
          <div class="report-item expense-item">
            <span class="label">總支出</span>
            <span class="value">NT$ {{ monthlyReport.totalExpense.toLocaleString() }}</span>
          </div>
          <div class="report-item balance-item">
            <span class="label">結餘</span>
            <span class="value" :class="{ negative: monthlyReport.balance < 0 }">
              NT$ {{ monthlyReport.balance.toLocaleString() }}
            </span>
          </div>
        </div>
        <div class="report-details">
          <div class="detail-section">
            <h4>收入明細</h4>
            <div v-if="Object.keys(monthlyReport.incomeByType).length > 0" class="detail-list">
              <div v-for="(amount, type) in monthlyReport.incomeByType" :key="type" class="detail-item">
                <span class="type-name">{{ type }}</span>
                <span class="type-amount">NT$ {{ amount.toLocaleString() }}</span>
              </div>
            </div>
            <p v-else class="empty-text">本月無收入記錄</p>
          </div>
          <div class="detail-section">
            <h4>支出明細</h4>
            <div v-if="Object.keys(monthlyReport.expenseByType).length > 0" class="detail-list">
              <div v-for="(amount, type) in monthlyReport.expenseByType" :key="type" class="detail-item">
                <span class="type-name">{{ type }}</span>
                <span class="type-amount">NT$ {{ amount.toLocaleString() }}</span>
              </div>
            </div>
            <p v-else class="empty-text">本月無支出記錄</p>
          </div>
        </div>
      </div>
    </section>

    <!-- 自動生成報表 -->
    <section v-if="autoReport" class="section auto-report-section">
      <div class="auto-report-header">
        <h2>📊 上月自動報表</h2>
        <button type="button" class="download-pdf-btn" @click="downloadPDF" :disabled="downloadingPDF">
          {{ downloadingPDF ? '生成中...' : '📥 下載 PDF' }}
        </button>
      </div>
      <div class="auto-report-content" id="auto-report-content">
        <div class="report-meta">
          <p class="generated-time">生成時間：{{ formatDateTime(autoReport.generatedAt) }}</p>
        </div>
        <div class="report-summary-box">
          <h3>{{ autoReport.month }} 財務總結</h3>
          <div class="summary-grid">
            <div class="summary-item income-bg">
              <span class="summary-label">總收入</span>
              <span class="summary-value">NT$ {{ autoReport.report.totalIncome.toLocaleString() }}</span>
            </div>
            <div class="summary-item expense-bg">
              <span class="summary-label">總支出</span>
              <span class="summary-value">NT$ {{ autoReport.report.totalExpense.toLocaleString() }}</span>
            </div>
            <div class="summary-item balance-bg">
              <span class="summary-label">結餘</span>
              <span class="summary-value" :class="{ negative: autoReport.report.balance < 0 }">
                NT$ {{ autoReport.report.balance.toLocaleString() }}
              </span>
            </div>
          </div>
        </div>
        <div class="report-analysis">
          <h4>📈 財務分析</h4>
          <p class="analysis-text">{{ autoReport.summary }}</p>
        </div>
        <div class="report-breakdown">
          <div class="breakdown-section">
            <h4>💰 收入分類</h4>
            <div v-if="Object.keys(autoReport.report.incomeByType).length > 0" class="breakdown-list">
              <div v-for="(amount, type) in autoReport.report.incomeByType" :key="type" class="breakdown-item">
                <span class="breakdown-type">{{ type }}</span>
                <span class="breakdown-amount">NT$ {{ amount.toLocaleString() }}</span>
                <span class="breakdown-percent">
                  {{ ((amount / autoReport.report.totalIncome) * 100).toFixed(1) }}%
                </span>
              </div>
            </div>
            <p v-else class="empty-text">無收入記錄</p>
          </div>
          <div class="breakdown-section">
            <h4>💸 支出分類</h4>
            <div v-if="Object.keys(autoReport.report.expenseByType).length > 0" class="breakdown-list">
              <div v-for="(amount, type) in autoReport.report.expenseByType" :key="type" class="breakdown-item">
                <span class="breakdown-type">{{ type }}</span>
                <span class="breakdown-amount">NT$ {{ amount.toLocaleString() }}</span>
                <span class="breakdown-percent">
                  {{ ((amount / autoReport.report.totalExpense) * 100).toFixed(1) }}%
                </span>
              </div>
            </div>
            <p v-else class="empty-text">無支出記錄</p>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useFinanceData } from '@/composables/useFinanceData'
import { useAuth } from '@/composables/useAuth'
import { generateMonthlyReport } from '@/api/finance'
import type { MonthlyReport, AutoGeneratedReport, ReportGenerateResponse } from '@/types/finance'

const router = useRouter()
const { user, logout } = useAuth()

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

// 登出功能
function handleLogout() {
  logout()
  router.push('/login')
}

// 每月報表
const currentMonth = new Date().toISOString().slice(0, 7)
const selectedMonth = ref(currentMonth)
const monthlyReport = ref<MonthlyReport | null>(null)
const loadingReport = ref(false)
const reportError = ref<string | null>(null)

async function fetchReport() {
  if (!selectedMonth.value) return
  loadingReport.value = true
  reportError.value = null
  monthlyReport.value = null
  try {
    const response: ReportGenerateResponse = await generateMonthlyReport()
    if (response.month === selectedMonth.value) {
      await loadReportFromResponse(response)
    } else {
      reportError.value = `後端返回的報表月份 (${response.month}) 不匹配選擇的月份 (${selectedMonth.value})`
    }
  } catch (err) {
    reportError.value = err instanceof Error ? err.message : '無法生成報表'
  } finally {
    loadingReport.value = false
  }
}

async function loadReportFromResponse(response: ReportGenerateResponse) {
  monthlyReport.value = {
    month: response.month,
    totalIncome: 0,
    totalExpense: 0,
    balance: 0,
    incomeByType: {},
    expenseByType: {}
  }
}

// 自動生成報表
const autoReport = ref<AutoGeneratedReport | null>(null)
const downloadingPDF = ref(false)

// 檢查是否為每月一日，自動載入上月報表
function checkAndLoadAutoReport() {
  const today = new Date()
  const dayOfMonth = today.getDate()
  
  // 每月一日自動生成報表
  if (dayOfMonth === 1) {
    const lastMonth = new Date(today.getFullYear(), today.getMonth() - 1, 1)
    const lastMonthStr = lastMonth.toISOString().slice(0, 7)
    loadAutoReport(lastMonthStr)
  } else {
    // 非一日時，檢查 localStorage 是否有本月已生成的報表
    const storedReport = localStorage.getItem('auto_report')
    if (storedReport) {
      try {
        const parsed = JSON.parse(storedReport)
        const reportDate = new Date(parsed.generatedAt)
        const thisMonth = today.toISOString().slice(0, 7)
        const reportMonth = reportDate.toISOString().slice(0, 7)
        
        // 如果是本月生成的報表，顯示它
        if (reportMonth === thisMonth) {
          autoReport.value = parsed
        }
      } catch (err) {
        console.error('Failed to parse stored report', err)
      }
    }
  }
}

async function loadAutoReport(month: string) {
  try {
    const response: ReportGenerateResponse = await generateMonthlyReport()
    
    const mockReport: MonthlyReport = {
      month: response.month,
      totalIncome: 0,
      totalExpense: 0,
      balance: 0,
      incomeByType: {},
      expenseByType: {}
    }
    
    const summary = generateSummary(mockReport)
    
    const generatedReport: AutoGeneratedReport = {
      month: response.month,
      generatedAt: new Date().toISOString(),
      report: mockReport,
      summary
    }
    
    autoReport.value = generatedReport
    localStorage.setItem('auto_report', JSON.stringify(generatedReport))
  } catch (err) {
    console.error('Failed to load auto report', err)
  }
}

function generateSummary(report: MonthlyReport): string {
  const { totalIncome, totalExpense, balance } = report
  
  let summary = `本月總收入為 NT$ ${totalIncome.toLocaleString()}，總支出為 NT$ ${totalExpense.toLocaleString()}，`
  
  if (balance > 0) {
    summary += `結餘 NT$ ${balance.toLocaleString()}，財務狀況良好。`
  } else if (balance < 0) {
    summary += `赤字 NT$ ${Math.abs(balance).toLocaleString()}，建議控制支出。`
  } else {
    summary += `收支平衡。`
  }
  
  // 找出最大收入和支出類別
  const incomeEntries = Object.entries(report.incomeByType)
  const expenseEntries = Object.entries(report.expenseByType)
  
  if (incomeEntries.length > 0) {
    const maxIncome = incomeEntries.reduce((max, curr) => curr[1] > max[1] ? curr : max)
    summary += ` 主要收入來源為「${maxIncome[0]}」，金額 NT$ ${maxIncome[1].toLocaleString()}。`
  }
  
  if (expenseEntries.length > 0) {
    const maxExpense = expenseEntries.reduce((max, curr) => curr[1] > max[1] ? curr : max)
    summary += ` 最大支出項目為「${maxExpense[0]}」，金額 NT$ ${maxExpense[1].toLocaleString()}。`
  }
  
  return summary
}

function formatDateTime(isoString: string): string {
  const date = new Date(isoString)
  return date.toLocaleString('zh-TW', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

async function downloadPDF() {
  downloadingPDF.value = true
  try {
    const html2pdf = (await import('html2pdf.js' as any)).default as any
    
    const element = document.getElementById('auto-report-content')
    if (!element) throw new Error('找不到報表內容')
    
    const opt = {
      margin: 10,
      filename: `財務報表_${autoReport.value?.month}.pdf`,
      image: { type: 'jpeg', quality: 0.98 },
      html2canvas: { scale: 2 },
      jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' }
    }
    
    await html2pdf().set(opt).from(element).save()
  } catch (err) {
    console.error('PDF 下載失敗', err)
    alert('PDF 下載失敗，請稍後再試')
  } finally {
    downloadingPDF.value = false
  }
}

// 支出表單
const expenseForm = reactive({ type: '', amount: null as number | null, date: '' })
const expenseLoading = ref(false)
const expenseError = ref<string | null>(null)
const expenseSuccess = ref<string | null>(null)
const addingExpenseType = ref(false)
const newExpenseTypeName = ref('')
const creatingExpenseType = ref(false)

async function createExpenseType() {
  if (!newExpenseTypeName.value) return
  creatingExpenseType.value = true
  try {
    await addExpenseType(newExpenseTypeName.value)
    expenseForm.type = newExpenseTypeName.value
    newExpenseTypeName.value = ''
    addingExpenseType.value = false
    expenseSuccess.value = '類型已新增'
  } catch (err) {
    expenseError.value = err instanceof Error ? err.message : '新增類型失敗'
  } finally {
    creatingExpenseType.value = false
  }
}

async function submitExpense() {
  expenseError.value = null
  expenseSuccess.value = null
  if (!expenseForm.type || expenseForm.amount === null || expenseForm.amount <= 0) {
    expenseError.value = '請選擇類型並填寫大於 0 的金額'
    return
  }
  expenseLoading.value = true
  try {
    await addExpenseEntry({
      type: expenseForm.type,
      amount: expenseForm.amount,
      ...(expenseForm.date ? { date: expenseForm.date } : {})
    })
    expenseSuccess.value = '新增成功'
    expenseForm.amount = null
    expenseForm.date = ''
  } catch (err) {
    expenseError.value = err instanceof Error ? err.message : '新增失敗'
  } finally {
    expenseLoading.value = false
  }
}

// 收入表單
const incomeForm = reactive({ type: '', amount: null as number | null, date: '' })
const incomeLoading = ref(false)
const incomeError = ref<string | null>(null)
const incomeSuccess = ref<string | null>(null)
const addingIncomeType = ref(false)
const newIncomeTypeName = ref('')
const creatingIncomeType = ref(false)

async function createIncomeType() {
  if (!newIncomeTypeName.value) return
  creatingIncomeType.value = true
  try {
    await addIncomeType(newIncomeTypeName.value)
    incomeForm.type = newIncomeTypeName.value
    newIncomeTypeName.value = ''
    addingIncomeType.value = false
    incomeSuccess.value = '類型已新增'
  } catch (err) {
    incomeError.value = err instanceof Error ? err.message : '新增類型失敗'
  } finally {
    creatingIncomeType.value = false
  }
}

async function submitIncome() {
  incomeError.value = null
  incomeSuccess.value = null
  if (!incomeForm.type || incomeForm.amount === null || incomeForm.amount <= 0) {
    incomeError.value = '請選擇類型並填寫大於 0 的金額'
    return
  }
  incomeLoading.value = true
  try {
    await addIncomeEntry({
      type: incomeForm.type,
      amount: incomeForm.amount,
      ...(incomeForm.date ? { date: incomeForm.date } : {})
    })
    incomeSuccess.value = '新增成功'
    incomeForm.amount = null
    incomeForm.date = ''
  } catch (err) {
    incomeError.value = err instanceof Error ? err.message : '新增失敗'
  } finally {
    incomeLoading.value = false
  }
}

onMounted(() => {
  checkAndLoadAutoReport()
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

.header-left {
  display: flex;
  align-items: center;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

h1 {
  margin: 0;
  color: #1f2933;
  font-size: 1.75rem;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: #f3f4f6;
  border-radius: 8px;
  font-size: 0.95rem;
}

.user-icon {
  font-size: 1.25rem;
}

.user-name {
  color: #374151;
  font-weight: 500;
}

.logout-btn {
  padding: 0.5rem 1rem;
  background: #ef4444;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
  font-size: 0.95rem;
}

.logout-btn:hover {
  background: #dc2626;
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

/* 總覽卡片 */
.summary-card {
  background: white;
  border-radius: 16px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.summary-card h3 {
  font-size: 1rem;
  color: #6b7280;
  margin: 0 0 0.6rem;
}

.summary-card .amount {
  font-size: 2rem;
  font-weight: 700;
  margin: 0;
}

.summary-card.expense .amount {
  color: #e74c3c;
}

.summary-card.income .amount {
  color: #27ae60;
}

.summary-card.balance .amount {
  color: #3498db;
}

.summary-card.balance .amount.negative {
  color: #e74c3c;
}

.summary-card .loading-text {
  color: #9ca3af;
  font-size: 1rem;
  margin: 0;
}

/* 類型卡片 */
.type-card {
  background: white;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.35rem;
  transition: all 0.2s;
  cursor: pointer;
}

.type-card:hover {
  border-color: #42b883;
  transform: translateY(-3px);
  box-shadow: 0 6px 16px rgba(66, 184, 131, 0.18);
}

.type-card .icon {
  font-size: 2rem;
}

.type-card .name {
  font-weight: 600;
  color: #1f2933;
}

.type-card .amount-badge {
  margin-top: 0.25rem;
  padding: 0.25rem 0.75rem;
  background: #fee;
  color: #e74c3c;
  border-radius: 12px;
  font-size: 0.9rem;
  font-weight: 600;
}

.type-card .income-badge {
  background: #e8f8f5;
  color: #27ae60;
}

/* 表單卡片 */
.form-card {
  background: white;
  border-radius: 12px;
  padding: 1.25rem;
  border: 1px solid #e5e7eb;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.form-card h3 {
  margin: 0 0 0.75rem;
  color: #1f2933;
}

.form-card form {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.form-card label {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
  color: #4b5563;
  font-weight: 600;
}

.form-card input,
.form-card select {
  font-size: 1rem;
  padding: 0.5rem 0.75rem;
  border-radius: 8px;
  border: 1px solid #d1d5db;
}

.type-select-group {
  display: flex;
  gap: 0.5rem;
}

.type-select-group select {
  flex: 1;
}

.add-type-btn {
  width: 36px;
  height: 36px;
  padding: 0;
  background: #f3f4f6;
  color: #374151;
  font-size: 1.2rem;
  font-weight: bold;
  border: 1px solid #d1d5db;
  display: flex;
  align-items: center;
  justify-content: center;
}

.add-type-btn:hover:not(:disabled) {
  background: #e5e7eb;
}

.new-type-input {
  display: flex;
  gap: 0.5rem;
  margin-top: 0.5rem;
  animation: slideDown 0.2s ease;
}

.new-type-input input {
  flex: 1;
}

.create-type-btn {
  padding: 0.5rem 1rem;
  background: #3b82f6;
  white-space: nowrap;
}

.create-type-btn:hover:not(:disabled) {
  background: #2563eb;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.small {
  font-size: 0.875rem;
}

.success {
  background: #d1fae5;
  border: 1px solid #a7f3d0;
  border-radius: 8px;
  padding: 0.75rem 1rem;
  color: #065f46;
  margin: 0.5rem 0;
}

/* 每月報表 */
.report-controls {
  display: flex;
  gap: 0.75rem;
  align-items: center;
  margin-bottom: 1.5rem;
}

.report-controls input[type='month'] {
  padding: 0.5rem 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 1rem;
}

.report-controls button {
  padding: 0.5rem 1.5rem;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
}

.report-controls button:hover:not(:disabled) {
  background: #2563eb;
}

.report-controls button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.report-content {
  display: grid;
  gap: 1.5rem;
}

.report-summary {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.report-item {
  background: #f9fafb;
  padding: 1rem;
  border-radius: 10px;
  border: 1px solid #e5e7eb;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.report-item .label {
  color: #6b7280;
  font-size: 0.875rem;
  font-weight: 500;
}

.report-item .value {
  color: #111827;
  font-size: 1.25rem;
  font-weight: 700;
}

.income-item {
  border-left: 4px solid #10b981;
}

.expense-item {
  border-left: 4px solid #ef4444;
}

.balance-item {
  border-left: 4px solid #3b82f6;
}

.report-details {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
}

.detail-section {
  background: #f9fafb;
  padding: 1.25rem;
  border-radius: 10px;
  border: 1px solid #e5e7eb;
}

.detail-section h4 {
  margin: 0 0 1rem 0;
  color: #374151;
  font-size: 1rem;
  font-weight: 600;
}

.detail-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem;
  background: white;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
}

.detail-item .type-name {
  color: #374151;
  font-weight: 500;
}

.detail-item .type-amount {
  color: #111827;
  font-weight: 600;
}

.empty-text {
  color: #9ca3af;
  font-size: 0.875rem;
  text-align: center;
  padding: 1rem 0;
}

/* 自動生成報表 */
.auto-report-section {
  background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
  border: 2px solid #3b82f6;
  border-radius: 12px;
  padding: 2rem;
  margin-top: 3rem;
}

.auto-report-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.auto-report-header h2 {
  margin: 0;
  color: #1e40af;
  font-size: 1.5rem;
}

.download-pdf-btn {
  padding: 0.75rem 1.5rem;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  font-size: 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.download-pdf-btn:hover:not(:disabled) {
  background: #2563eb;
}

.download-pdf-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.auto-report-content {
  background: white;
  border-radius: 10px;
  padding: 2rem;
}

.report-meta {
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #e5e7eb;
}

.generated-time {
  color: #6b7280;
  font-size: 0.875rem;
  margin: 0;
}

.report-summary-box {
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: #f9fafb;
  border-radius: 10px;
}

.report-summary-box h3 {
  margin: 0 0 1.5rem 0;
  color: #111827;
  font-size: 1.25rem;
  text-align: center;
}

.summary-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.summary-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  padding: 1.25rem;
  border-radius: 10px;
  text-align: center;
}

.income-bg {
  background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
  border: 2px solid #10b981;
}

.expense-bg {
  background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
  border: 2px solid #ef4444;
}

.balance-bg {
  background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
  border: 2px solid #3b82f6;
}

.summary-label {
  font-size: 0.875rem;
  color: #374151;
  font-weight: 500;
}

.summary-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: #111827;
}

.report-analysis {
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: #fffbeb;
  border-left: 4px solid #f59e0b;
  border-radius: 8px;
}

.report-analysis h4 {
  margin: 0 0 1rem 0;
  color: #92400e;
  font-size: 1.1rem;
}

.analysis-text {
  margin: 0;
  color: #78350f;
  line-height: 1.6;
  font-size: 1rem;
}

.report-breakdown {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.breakdown-section {
  background: #f9fafb;
  padding: 1.5rem;
  border-radius: 10px;
  border: 1px solid #e5e7eb;
}

.breakdown-section h4 {
  margin: 0 0 1rem 0;
  color: #374151;
  font-size: 1.05rem;
  font-weight: 600;
}

.breakdown-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.breakdown-item {
  display: grid;
  grid-template-columns: 1fr auto auto;
  gap: 1rem;
  align-items: center;
  padding: 0.75rem 1rem;
  background: white;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
}

.breakdown-type {
  color: #374151;
  font-weight: 500;
}

.breakdown-amount {
  color: #111827;
  font-weight: 600;
}

.breakdown-percent {
  color: #6b7280;
  font-size: 0.875rem;
  font-weight: 500;
  min-width: 50px;
  text-align: right;
}
</style>
