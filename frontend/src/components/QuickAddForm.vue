<template>
  <section class="section quick-add">
    <div class="section-heading">
      <div>
        <h2 class="section-title">新增收支</h2>
      </div>
    </div>
    <form class="inline-form" @submit.prevent="$emit('submit', form)">
      <div class="kind-switch" role="group" aria-label="記帳類型">
        <label class="pill" :class="{ active: kind === 'expense' }">
          <input type="radio" value="expense" v-model="kind" /> 支出
        </label>
        <label class="pill" :class="{ active: kind === 'income' }">
          <input type="radio" value="income" v-model="kind" /> 收入
        </label>
      </div>
      <select v-model="form.type" :disabled="loading" required>
        <option value="" disabled>類別</option>
        <option v-for="type in typeOptions" :key="type.id" :value="type.name">
          {{ type.name }}
        </option>
      </select>
      <input 
        v-model.number="form.amount" 
        type="number" 
        min="1" 
        max="999999999999999999"
        step="1" 
        :disabled="loading" 
        placeholder="金額" 
        required 
      />
      <input v-model="form.date" type="date" :disabled="loading" required />
      <button class="primary" type="submit" :disabled="loading">
        {{ loading ? '送出中..' : '送出' }}
      </button>
      <span class="form-hint" v-if="error">{{ error }}</span>
      <span class="form-ok" v-if="success">{{ success }}</span>
    </form>
    <div v-if="success" class="toast" role="status" aria-live="polite">{{ success }}</div>
  </section>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'

interface TypeOption {
  id: string
  name: string
}

const props = defineProps<{
  expenseTypes: TypeOption[]
  incomeTypes: TypeOption[]
  loading: boolean
  error: string
  success: string
}>()

const emit = defineEmits<{
  submit: [form: { type: string; amount: number; date: string }]
}>()

const kind = ref<'expense' | 'income'>('expense')
const form = ref({
  type: '',
  amount: 0,
  date: new Date().toISOString().split('T')[0]
})

const typeOptions = computed(() => {
  return kind.value === 'expense' ? props.expenseTypes : props.incomeTypes
})

// Reset type when switching kind
watch(kind, () => {
  form.value.type = ''
})

// Expose reset method
defineExpose({
  reset: () => {
    form.value = {
      type: '',
      amount: 0,
      date: new Date().toISOString().split('T')[0]
    }
  },
  getKind: () => kind.value
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

.kind-switch {
  display: flex;
  gap: 0.5rem;
}

.pill {
  display: inline-flex;
  align-items: center;
  padding: 0.5rem 1rem;
  border: 1px solid #ddd;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.2s;
  background: #fff;
}

.pill input {
  margin-right: 0.5rem;
}

.pill.active {
  background: #3b82f6;
  color: white;
  border-color: #3b82f6;
}

input[type="number"],
input[type="date"],
select {
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

button.primary:hover:not(:disabled) {
  background: #2563eb;
}

button.primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.form-hint {
  color: #ef4444;
  font-size: 0.875rem;
}

.form-ok {
  color: #22c55e;
  font-size: 0.875rem;
}

.toast {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  background: #22c55e;
  color: white;
  padding: 1rem 1.5rem;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
  from {
    transform: translateY(100%);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}
</style>
