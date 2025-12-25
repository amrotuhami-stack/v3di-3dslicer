<script setup>
import { computed } from 'vue'
import { useAppStore } from './stores/app'
import AppHeader from './components/AppHeader.vue'
import AppSidebar from './components/AppSidebar.vue'

const store = useAppStore()
const sidebarCollapsed = computed(() => store.sidebarCollapsed)
</script>

<template>
  <div class="app-layout">
    <AppHeader />
    
    <div class="app-body">
      <AppSidebar :collapsed="sidebarCollapsed" />
      
      <main class="app-main">
        <router-view />
      </main>
    </div>
    
    <!-- Processing Overlay -->
    <div v-if="store.isProcessing" class="processing-overlay">
      <div class="processing-modal">
        <div class="spinner"></div>
        <h3>Processing</h3>
        <p class="text-muted">{{ store.processingMessage || 'Please wait...' }}</p>
        <div class="progress" style="width: 200px; margin-top: 16px;">
          <div class="progress-bar" :style="{ width: store.processingProgress + '%' }"></div>
        </div>
        <span class="text-muted" style="font-size: 12px; margin-top: 8px;">
          {{ store.processingProgress }}%
        </span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.app-layout {
  height: 100vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.app-body {
  flex: 1;
  display: flex;
  overflow: hidden;
}

.app-main {
  flex: 1;
  overflow: auto;
  background: var(--bg-primary);
}

.processing-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.processing-modal {
  background: var(--bg-secondary);
  border: 1px solid var(--border-primary);
  border-radius: var(--radius-lg);
  padding: 32px;
  display: flex;
  flex-direction: column;
  align-items: center;
  box-shadow: var(--shadow-xl);
}

.processing-modal h3 {
  margin-top: 16px;
  margin-bottom: 8px;
}
</style>
