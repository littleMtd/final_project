<template>
  <div class="summary-card" :class="type">
    <h3>{{ title }}</h3>
    <p v-if="!loading" class="amount" :class="{ negative: isNegative }">
      NT$ {{ amount.toLocaleString() }}
    </p>
    <p v-else class="loading-text">載入中...</p>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  title: string
  amount: number
  loading?: boolean
  type: 'expense' | 'income' | 'balance'
}>()

const isNegative = computed(() => props.type === 'balance' && props.amount < 0)
</script>

<style scoped>
.summary-card {
  background: white;
  border-radius: 16px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

h3 {
  font-size: 1rem;
  color: #6b7280;
  margin: 0 0 0.6rem;
}

.amount {
  font-size: 2rem;
  font-weight: 700;
  margin: 0;
}

.expense .amount {
  color: #e74c3c;
}

.income .amount {
  color: #27ae60;
}

.balance .amount {
  color: #3498db;
}

.balance .amount.negative {
  color: #e74c3c;
}

.loading-text {
  color: #9ca3af;
  font-size: 1rem;
}
</style>
