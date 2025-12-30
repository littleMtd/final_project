<template>
  <section class="summary-bar" aria-label="summary">
    <div class="kpi-card">
      <p class="kpi-value" v-if="!loadingExpenseTotal">NT$ {{ expenseTotal.toLocaleString() }}</p>
      <p class="kpi-value muted" v-else>載入中..</p>
    </div>
    <div class="kpi-card">
      <p class="kpi-value" v-if="!loadingIncomeTotal">NT$ {{ incomeTotal.toLocaleString() }}</p>
      <p class="kpi-value muted" v-else>載入中..</p>
    </div>
    <div class="kpi-card">
      <p class="kpi-value balance" :class="{ negative: balance < 0 }">NT$ {{ balance.toLocaleString() }}</p>
    </div>
  </section>
</template>

<script setup lang="ts">
defineProps<{
  expenseTotal: number
  incomeTotal: number
  balance: number
  loadingExpenseTotal: boolean
  loadingIncomeTotal: boolean
}>()
</script>

<style scoped>
.summary-bar {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.kpi-card {
  background: #ffffff;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 1.5rem;
  text-align: center;
}

.kpi-value {
  font-size: 1.75rem;
  font-weight: 600;
  margin: 0;
  color: #333;
}

.kpi-value.muted {
  color: #999;
  font-size: 1rem;
}

.kpi-value.balance {
  color: #22c55e;
}

.kpi-value.balance.negative {
  color: #ef4444;
}
</style>
