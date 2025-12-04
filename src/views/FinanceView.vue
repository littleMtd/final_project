<template>
  <div class="finance-view">
    <header class="page-header">
      <h1>個人財經系統</h1>
      <button class="ghost" type="button" @click="refreshAll" :disabled="loadingExpense || loadingIncome" title="重新整理">
        🔄
      </button>
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
  </div>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
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
    expenseSuccess.value = '新增成功 (202)'
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
    incomeSuccess.value = '新增成功 (202)'
    incomeForm.amount = null
    incomeForm.date = ''
  } catch (err) {
    incomeError.value = err instanceof Error ? err.message : '新增失敗'
  } finally {
    incomeLoading.value = false
  }
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
</style>
