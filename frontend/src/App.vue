<script setup lang="ts">
import Header from './components/Header.vue'
import WorkflowView from './views/WorkflowView.vue'
</script>

<template>
  <div class="min-h-screen flex flex-col bg-slate-50">
    <Header />
    <main class="flex-1">
      <WorkflowView />
    </main>
    <footer class="py-6 border-t border-slate-200 text-center text-xs text-slate-400 bg-white">
      AutoCopyright-AI &copy; 2026 — 严格遵循中国版权保护中心（CPCC）软著审核规范
    </footer>
  </div>
</template>
