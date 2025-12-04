<template>
  <div class="form-card">
    <h3>{{ title }}</h3>
    <form @submit.prevent="handleSubmit">
      <label>
        類型
        <div class="type-select-group">
          <select v-model="form.type" :disabled="loading || addingNewType" required>
            <option value="" disabled>請選擇</option>
            <option v-for="type in types" :key="type.id" :value="type.name">
              {{ type.name }}
            </option>
          </select>
          <button
            type="button"
            class="add-type-btn"
            @click="toggleAddType"
            :disabled="loading"
            :title="addingNewType ? '取消' : '新增類型'"
          >
            {{ addingNewType ? '✕' : '+' }}
          </button>
        </div>
        <div v-if="addingNewType" class="new-type-input">
          <input
            v-model.trim="newTypeName"
            type="text"
            placeholder="輸入新類型名稱"
            :disabled="creatingType"
            @keyup.enter="handleCreateType"
            @keyup.esc="toggleAddType"
          />
          <button
            type="button"
            class="create-type-btn"
            @click="handleCreateType"
            :disabled="creatingType || !newTypeName"
          >
            {{ creatingType ? '...' : '確認' }}
          </button>
        </div>
      </label>
      <label>
        金額
        <input
          v-model.number="form.amount"
          type="number"
          min="1"
          step="1"
          :disabled="loading"
          placeholder="例如 120"
          required
        />
      </label>
      <label>
        日期 (選填)
        <input v-model="form.date" type="date" :disabled="loading" />
      </label>
      <button type="submit" :disabled="loading">
        {{ loading ? '送出中...' : '送出' }}
      </button>
      <p v-if="error" class="error small">{{ error }}</p>
      <p v-if="success" class="success small">{{ success }}</p>
    </form>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, watch } from 'vue'
import type { FinanceType } from '@/types/finance'

const props = defineProps<{
  title: string
  types: FinanceType[]
  onSubmit: (data: { type: string; amount: number; date?: string }) => Promise<void>
  onCreateType?: (name: string) => Promise<void>
}>()

const form = reactive({
  type: '',
  amount: null as number | null,
  date: ''
})

const loading = ref(false)
const error = ref<string | null>(null)
const success = ref<string | null>(null)

const addingNewType = ref(false)
const newTypeName = ref('')
const creatingType = ref(false)

function toggleAddType() {
  addingNewType.value = !addingNewType.value
  if (!addingNewType.value) {
    newTypeName.value = ''
  }
}

async function handleCreateType() {
  if (!newTypeName.value || !props.onCreateType) return

  creatingType.value = true
  try {
    await props.onCreateType(newTypeName.value)
    form.type = newTypeName.value
    newTypeName.value = ''
    addingNewType.value = false
    success.value = '類型已新增'
  } catch (err) {
    error.value = err instanceof Error ? err.message : '新增類型失敗'
  } finally {
    creatingType.value = false
  }
}

async function handleSubmit() {
  error.value = null
  success.value = null

  if (!form.type || form.amount === null || form.amount <= 0) {
    error.value = '請選擇類型並填寫大於 0 的金額'
    return
  }

  loading.value = true
  try {
    await props.onSubmit({
      type: form.type,
      amount: form.amount,
      ...(form.date ? { date: form.date } : {})
    })
    success.value = '新增成功 (202)'
    form.amount = null
    form.date = ''
  } catch (err) {
    error.value = err instanceof Error ? err.message : '新增失敗'
  } finally {
    loading.value = false
  }
}

watch(() => [form.type, form.amount, form.date], () => {
  error.value = null
  success.value = null
})
</script>

<style scoped>
.form-card {
  background: white;
  border-radius: 12px;
  padding: 1.25rem;
  border: 1px solid #e5e7eb;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

h3 {
  margin: 0 0 0.75rem;
  color: #1f2933;
}

form {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

label {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
  color: #4b5563;
  font-weight: 600;
}

input,
select {
  font-size: 1rem;
  padding: 0.5rem 0.75rem;
  border-radius: 8px;
  border: 1px solid #d1d5db;
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

button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.error,
.success {
  border-radius: 8px;
  padding: 0.5rem;
  margin: 0;
}

.error {
  background: #fee;
  border: 1px solid #fcc;
  color: #b91c1c;
}

.success {
  background: #ecfdf3;
  border: 1px solid #bbf7d0;
  color: #15803d;
}

.small {
  font-size: 0.9rem;
}
</style>
