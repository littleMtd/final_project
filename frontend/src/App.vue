<template>
  <div id="app">
    <RouterView />
  </div>
</template>

<script setup>
import { RouterView } from 'vue-router'
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  --surface: #ffffff;
  --surface-muted: #f4f6fb;
  --text: #111827;
  --text-muted: #4b5563;
  --primary: #2563eb;
  --primary-strong: #1d4ed8;
  --ring: #c7d7fe;
  --danger: #dc2626;
  font-family: var(--app-font, -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Microsoft JhengHei', sans-serif);
  color: var(--text);
  background: var(--surface-muted);
  min-height: 100vh;
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
}

#app {
  min-height: 100vh;
}

*:focus-visible {
  outline: 2px solid var(--primary);
  outline-offset: 3px;
  transition: outline-color 0.12s ease;
}
</style>
