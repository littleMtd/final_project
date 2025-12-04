<template>
  <div id="app">
    <FinanceView />
  </div>
</template>

<script setup>
import FinanceView from './views/FinanceView.vue'
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Microsoft JhengHei', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  background: #f5f7fa;
}

#app {
  min-height: 100vh;
}
</style>
