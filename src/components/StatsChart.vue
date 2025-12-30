<template>
  <section class="section stats-section">
    <div class="section-heading">
      <div>
        <h2 class="section-title">收支類別排行</h2>
      </div>
    </div>
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-card-head">
          <div class="rank-actions">
            <div class="kind-tabs small">
              <button 
                type="button" 
                :class="{ active: activeTab === 'expense' }" 
                @click="$emit('update:activeTab', 'expense')"
              >
                支出
              </button>
              <button 
                type="button" 
                :class="{ active: activeTab === 'income' }" 
                @click="$emit('update:activeTab', 'income')"
              >
                收入
              </button>
            </div>
            <button 
              type="button" 
              class="link-btn" 
              v-if="hasMore" 
              @click="$emit('toggle-show-more')"
            >
              {{ showMore ? '收起' : '更多類別' }}
            </button>
          </div>
        </div>
        <div v-if="loading" class="loading">載入中..</div>
        <div v-else-if="!hasData" class="empty-text">沒有資料</div>
        <v-chart v-else class="rank-chart" :option="chartOption" autoresize />
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { PieChart } from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent
} from 'echarts/components'

use([
  CanvasRenderer,
  PieChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent
])

defineProps<{
  activeTab: 'expense' | 'income'
  showMore: boolean
  hasMore: boolean
  loading: boolean
  hasData: boolean
  chartOption: any
}>()

defineEmits<{
  'update:activeTab': [value: 'expense' | 'income']
  'toggle-show-more': []
}>()
</script>

<style scoped>
.section {
  background: #ffffff;
  border-radius: 8px;
  padding: 1.5rem;
  border: 1px solid #e0e0e0;
}

.section-heading {
  margin-bottom: 1rem;
}

.section-title {
  font-size: 1.25rem;
  margin: 0;
  color: #333;
}

.stat-card {
  background: #fafafa;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 1rem;
}

.stat-card-head {
  margin-bottom: 1rem;
}

.rank-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 0.5rem;
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

.kind-tabs.small button {
  padding: 0.375rem 0.75rem;
  font-size: 0.875rem;
}

.link-btn {
  background: none;
  border: none;
  color: #3b82f6;
  cursor: pointer;
  text-decoration: underline;
  font-size: 0.875rem;
}

.loading,
.empty-text {
  text-align: center;
  color: #999;
  padding: 2rem;
}

.rank-chart {
  height: 400px;
  width: 100%;
}
</style>
