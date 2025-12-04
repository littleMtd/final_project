<template>
  <div class="type-card clickable" @click="$emit('click')">
    <span class="icon">{{ icon }}</span>
    <span class="name">{{ name }}</span>
    <span v-if="amount !== undefined" class="amount-badge" :class="badgeClass">
      NT$ {{ amount.toLocaleString() }}
    </span>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  name: string
  icon?: string
  amount?: number
  type: 'expense' | 'income'
}>()

defineEmits<{
  click: []
}>()

const badgeClass = props.type === 'income' ? 'income-badge' : ''
</script>

<style scoped>
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

.icon {
  font-size: 2rem;
}

.name {
  font-weight: 600;
  color: #1f2933;
}

.amount-badge {
  margin-top: 0.25rem;
  padding: 0.25rem 0.75rem;
  background: #fee;
  color: #e74c3c;
  border-radius: 12px;
  font-size: 0.9rem;
  font-weight: 600;
}

.income-badge {
  background: #e8f8f5;
  color: #27ae60;
}
</style>
