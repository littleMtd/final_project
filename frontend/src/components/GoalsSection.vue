<template>
  <section class="section goals-section">
    <div class="section-heading">
      <div>
        <h2 class="section-title">目標設定與進度</h2>
        <div style="display: flex; align-items: center; gap: 0.5rem; margin-top: 0.5rem;">
          <label style="font-size: 0.875rem; color: #666;">建立/查看月份：</label>
          <input 
            :value="selectedMonth" 
            @input="$emit('update:selected-month', ($event.target as HTMLInputElement).value)"
            type="month" 
            style="padding: 0.375rem 0.5rem; border: 1px solid #ddd; border-radius: 4px; font-size: 0.875rem;"
          />
        </div>
      </div>
      <div class="inline-form goal-form" @submit.prevent>
        <input v-model="goalForm.name" type="text" placeholder="目標名稱 (例：本月儲蓄)" />
        <select v-model="goalForm.type">
          <option value="income">收入目標</option>
          <option value="expense">支出目標</option>
        </select>
        <input 
          v-model.number="goalForm.target_amount" 
          type="number" 
          min="1" 
          max="999999999999999999"
          step="1" 
          placeholder="金額" 
        />
        <button 
          class="primary" 
          type="button" 
          :disabled="creating" 
          @click="handleSubmit"
        >
          {{ creating ? '建立中..' : '新增目標' }}
        </button>
      </div>
    </div>
    <p v-if="error" class="error">{{ error }}</p>
    <div class="goals-grid">
      <div v-if="loading" class="loading">載入中..</div>
      <div v-else-if="goals.length === 0" class="empty-text">尚未設定目標</div>
      <div v-else class="goal-card" v-for="g in goals" :key="g.name + g.type + (g.target_month || '')">
        <div class="goal-head">
          <div>
            <h3 class="goal-title">{{ g.name }}</h3>
            <p class="goal-month muted">目標月份：{{ (g.target_month || '').slice(0,7) }}</p>
          </div>
          <div class="goal-actions">
            <div class="goal-amounts">
              <span class="goal-target">目標 NT$ {{ Math.round(g.target).toLocaleString() }}</span>
              <span class="goal-progress">進度 NT$ {{ Math.round(g.progress ?? 0).toLocaleString() }}</span>
            </div>
            <button 
              type="button" 
              class="delete-goal-btn" 
              @click="$emit('delete-goal', { name: g.name, type: g.type, month: (g.target_month || '').slice(0,7) })"
              title="刪除目標"
            >
              ×
            </button>
          </div>
        </div>
        <div class="goal-progress-bar">
          <span :style="{ width: Math.min(100, g.percentage || 0) + '%' }"></span>
        </div>
        <div class="goal-meta">
          <span>{{ Math.min(100, g.percentage || 0).toFixed(1) }}%</span>
          <span class="muted">{{ g.type === 'income' ? '已達成收入' : '已發生支出' }}</span>
        </div>
      </div>
    </div>

    <div class="insights-card">
      <div class="insights-head">
        <h3 class="section-title">本月洞察</h3>
        <button 
          type="button" 
          class="ghost" 
          style="height:28px;padding:0 8px;font-size:12px;" 
          :disabled="loadingInsights" 
          @click="$emit('refresh-insights')"
        >
          {{ loadingInsights ? '刷新中..' : '重新整理' }}
        </button>
      </div>
      <div v-if="loadingInsights" class="loading">載入建議中..</div>
      <p v-else-if="errorInsights" class="error">{{ errorInsights }}</p>
      <ul v-else-if="insights.length > 0" class="insights-list">
        <li v-for="(line, idx) in insights" :key="idx">{{ line }}</li>
      </ul>
      <p v-else class="empty-text">暫無建議</p>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref } from 'vue'

interface Goal {
  name: string
  type: string
  target: number
  target_month?: string
  progress?: number
  percentage?: number
}

const props = defineProps<{
  goals: Goal[]
  loading: boolean
  creating: boolean
  error: string
  insights: string[]
  loadingInsights: boolean
  errorInsights: string
  selectedMonth: string
}>()

const emit = defineEmits<{
  'submit-goal': [form: { name: string; type: string; target_amount: number }]
  'refresh-insights': []
  'update:selected-month': [value: string]
  'delete-goal': [params: { name: string; type: string; month: string }]
}>()

const goalForm = ref({
  name: '',
  type: 'income',
  target_amount: 0
})

const handleSubmit = () => {
  if (!goalForm.value.name || !goalForm.value.target_amount) {
    return
  }
  emit('submit-goal', { ...goalForm.value })
}

defineExpose({
  resetForm: () => {
    goalForm.value = {
      name: '',
      type: 'income',
      target_amount: 0
    }
  }
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
  align-items: flex-start;
  margin-bottom: 1rem;
  gap: 1rem;
  flex-wrap: wrap;
}

.section-title {
  font-size: 1.25rem;
  margin: 0;
  color: #333;
}

.inline-form {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
  align-items: center;
}

.goal-form input,
.goal-form select {
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 0.95rem;
}

button.primary {
  background: #3b82f6;
  color: white;
  border: none;
  padding: 0.5rem 1.5rem;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
}

button.primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

button.ghost {
  background: transparent;
  border: 1px solid #ddd;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
}

.error {
  color: #ef4444;
  margin: 0.5rem 0;
}

.goals-grid {
  display: grid;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.goal-card {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 1rem;
  background: #fafafa;
}

.goal-head {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 0.75rem;
}

.goal-actions {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
}

.goal-title {
  font-size: 1rem;
  margin: 0 0 0.25rem 0;
  color: #333;
}

.goal-month {
  font-size: 0.875rem;
  margin: 0;
}

.goal-amounts {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.25rem;
}

.delete-goal-btn {
  background: transparent;
  border: 1px solid #e5e7eb;
  color: #ef4444;
  width: 24px;
  height: 24px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 18px;
  line-height: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  flex-shrink: 0;
  padding: 0;
}

.delete-goal-btn:hover {
  background: #fee2e2;
  border-color: #ef4444;
}

.goal-target,
.goal-progress {
  font-size: 0.875rem;
}

.goal-progress-bar {
  height: 12px;
  background: #e0e0e0;
  border-radius: 6px;
  overflow: hidden;
  margin-bottom: 0.5rem;
}

.goal-progress-bar span {
  display: block;
  height: 100%;
  background: linear-gradient(90deg, #3b82f6, #22c55e);
  transition: width 0.3s;
}

.goal-meta {
  display: flex;
  justify-content: space-between;
  font-size: 0.875rem;
}

.muted {
  color: #999;
}

.loading,
.empty-text {
  text-align: center;
  color: #999;
  padding: 1rem;
}

.insights-card {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 1rem;
  background: #f9fafb;
}

.insights-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.insights-list {
  list-style: disc;
  padding-left: 1.5rem;
  margin: 0;
}

.insights-list li {
  margin-bottom: 0.5rem;
  color: #555;
}
</style>
