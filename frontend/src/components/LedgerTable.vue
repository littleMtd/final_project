<template>
  <section class="section ledger-section">
    <div class="section-heading">
      <div>
        <h2 class="section-title">紀錄清單</h2>
      </div>
      <div class="filter-bar">
        <div class="kind-tabs">
          <button 
            type="button" 
            :class="{ active: kind === 'all' }" 
            @click="$emit('update:kind', 'all')"
          >
            全部
          </button>
          <button 
            type="button" 
            :class="{ active: kind === 'income' }" 
            @click="$emit('update:kind', 'income')"
          >
            收入
          </button>
          <button 
            type="button" 
            :class="{ active: kind === 'expense' }" 
            @click="$emit('update:kind', 'expense')"
          >
            支出
          </button>
        </div>
        <div class="pager">
          <button 
            type="button" 
            @click="$emit('prev-page')" 
            :disabled="page === 1"
          >
            上一頁
          </button>
          <span class="page-indicator muted">
            {{ page }} / {{ Math.max(1, Math.ceil(total / pageSize)) }}
          </span>
          <button 
            type="button" 
            @click="$emit('next-page')" 
            :disabled="page >= Math.max(1, Math.ceil(total / pageSize))"
          >
            下一頁
          </button>
        </div>
      </div>
    </div>
    <p v-if="error" class="error">{{ error }}</p>
    <div v-else-if="loading" class="loading">載入中..</div>
    <div v-else class="table-wrap">
      <table class="ledger-table">
        <thead>
          <tr>
            <th>日期</th>
            <th>類別</th>
            <th class="align-right">金額</th>
            <th class="align-right">操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in items" :key="item.id" class="ledger-row">
            <td class="ledger-date">
              <template v-if="editingId === item.id">
                <input v-model="editDraft.date" type="date" class="inline-input" />
              </template>
              <template v-else>{{ item.date }}</template>
            </td>
            <td class="ledger-kind" :class="item.kind">
              <span class="kind-badge" :class="item.kind">
                {{ item.kind === 'income' ? '收入' : '支出' }}
              </span>
              <span class="ledger-type">{{ item.type }}</span>
            </td>
            <td class="ledger-amount align-right" :class="item.kind">
              <template v-if="editingId === item.id">
                <input 
                  v-model.number="editDraft.amount" 
                  type="number" 
                  min="1" 
                  max="999999999999999999"
                  step="1" 
                  class="inline-input align-right" 
                />
              </template>
              <template v-else>NT$ {{ item.amount.toLocaleString() }}</template>
            </td>
            <td class="align-right action-cell">
              <template v-if="editingId === item.id">
                <button 
                  class="ghost icon-btn" 
                  type="button" 
                  aria-label="儲存" 
                  title="儲存" 
                  @click="handleSaveEdit(item)"
                >
                  💾
                </button>
                <button 
                  class="ghost icon-btn" 
                  type="button" 
                  aria-label="取消" 
                  title="取消" 
                  @click="handleCancelEdit"
                >
                  ✕
                </button>
              </template>
              <template v-else-if="pendingDeleteId === item.id">
                <span class="confirm-text">確認？</span>
                <button 
                  class="danger icon-btn" 
                  type="button" 
                  aria-label="確定刪除" 
                  title="確定刪除" 
                  @click="handleConfirmDelete(item)"
                >
                  ✔
                </button>
                <button 
                  class="ghost icon-btn" 
                  type="button" 
                  aria-label="取消" 
                  title="取消" 
                  @click="handleCancelDelete"
                >
                  ✕
                </button>
              </template>
              <template v-else>
                <button 
                  class="ghost icon-btn" 
                  type="button" 
                  aria-label="編輯" 
                  title="編輯" 
                  @click="handleStartEdit(item)"
                >
                  ✎
                </button>
                <button 
                  class="ghost icon-btn" 
                  type="button" 
                  aria-label="刪除" 
                  title="刪除" 
                  @click="handleAskDelete(item)"
                >
                  🗑
                </button>
              </template>
            </td>
          </tr>
          <tr v-if="items.length === 0">
            <td colspan="4" class="empty-text">
              沒有資料，請先使用上方「快速記帳」新增一筆記錄
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref } from 'vue'

interface LedgerItem {
  id: number
  date: string
  kind: 'income' | 'expense'
  type: string
  amount: number
}

const props = defineProps<{
  items: LedgerItem[]
  kind: 'all' | 'income' | 'expense'
  page: number
  total: number
  pageSize: number
  loading: boolean
  error: string
}>()

const emit = defineEmits<{
  'update:kind': [value: 'all' | 'income' | 'expense']
  'prev-page': []
  'next-page': []
  'edit-item': [item: LedgerItem, draft: { date: string; amount: number }]
  'delete-item': [item: LedgerItem]
}>()

const editingId = ref<number | null>(null)
const editDraft = ref({ date: '', amount: 0 })
const pendingDeleteId = ref<number | null>(null)

const handleStartEdit = (item: LedgerItem) => {
  editingId.value = item.id
  editDraft.value = {
    date: item.date,
    amount: item.amount
  }
}

const handleSaveEdit = (item: LedgerItem) => {
  emit('edit-item', item, { ...editDraft.value })
  editingId.value = null
}

const handleCancelEdit = () => {
  editingId.value = null
  editDraft.value = { date: '', amount: 0 }
}

const handleAskDelete = (item: LedgerItem) => {
  pendingDeleteId.value = item.id
}

const handleConfirmDelete = (item: LedgerItem) => {
  emit('delete-item', item)
  pendingDeleteId.value = null
}

const handleCancelDelete = () => {
  pendingDeleteId.value = null
}
</script>

<style scoped>
.section {
  background: #ffffff;
  border-radius: 8px;
  padding: 1.5rem;
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

.filter-bar {
  display: flex;
  gap: 1rem;
  align-items: center;
  flex-wrap: wrap;
}

.kind-tabs {
  display: flex;
  gap: 0.5rem;
}

.kind-tabs button {
  padding: 0.5rem 1rem;
  border: 1px solid #ddd;
  background: white;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
}

.kind-tabs button.active {
  background: #3b82f6;
  color: white;
  border-color: #3b82f6;
}

.pager {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.pager button {
  padding: 0.375rem 0.75rem;
  border: 1px solid #ddd;
  background: white;
  border-radius: 4px;
  cursor: pointer;
}

.pager button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-indicator {
  font-size: 0.875rem;
}

.muted {
  color: #999;
}

.error {
  color: #ef4444;
  margin: 0.5rem 0;
}

.loading,
.empty-text {
  text-align: center;
  color: #999;
  padding: 2rem;
}

.table-wrap {
  overflow-x: auto;
}

.ledger-table {
  width: 100%;
  border-collapse: collapse;
}

.ledger-table th {
  text-align: left;
  padding: 0.75rem;
  border-bottom: 2px solid #e0e0e0;
  font-weight: 600;
  color: #555;
}

.ledger-table td {
  padding: 0.75rem;
  border-bottom: 1px solid #f0f0f0;
}

.ledger-row:hover {
  background: #f9fafb;
}

.align-right {
  text-align: right;
}

.kind-badge {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 500;
  margin-right: 0.5rem;
}

.kind-badge.income {
  background: #d1fae5;
  color: #065f46;
}

.kind-badge.expense {
  background: #fee2e2;
  color: #991b1b;
}

.ledger-type {
  color: #666;
}

.ledger-amount.income {
  color: #22c55e;
  font-weight: 500;
}

.ledger-amount.expense {
  color: #ef4444;
  font-weight: 500;
}

.inline-input {
  padding: 0.25rem 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 0.875rem;
  width: 100%;
}

.action-cell {
  white-space: nowrap;
}

.icon-btn {
  background: none;
  border: 1px solid #ddd;
  padding: 0.25rem 0.5rem;
  cursor: pointer;
  border-radius: 4px;
  margin-left: 0.25rem;
}

.icon-btn:hover {
  background: #f0f0f0;
}

.ghost {
  background: transparent;
}

.danger {
  border-color: #ef4444;
  color: #ef4444;
}

.danger:hover {
  background: #fef2f2;
}

.confirm-text {
  font-size: 0.875rem;
  color: #999;
  margin-right: 0.5rem;
}
</style>
