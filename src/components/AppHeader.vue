<script setup>
import { useAppStore } from '../stores/app'
import { useRouter } from 'vue-router'

const store = useAppStore()
const router = useRouter()
</script>

<template>
  <header class="app-header">
    <div class="header-left">
      <button class="btn-icon" @click="store.toggleSidebar" title="Toggle Sidebar">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="3" y1="12" x2="21" y2="12"></line>
          <line x1="3" y1="6" x2="21" y2="6"></line>
          <line x1="3" y1="18" x2="21" y2="18"></line>
        </svg>
      </button>
      
      <div class="logo" @click="router.push('/')">
        <div class="logo-icon">
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none">
            <path d="M12 2L2 7L12 12L22 7L12 2Z" fill="url(#grad1)"/>
            <path d="M2 17L12 22L22 17" stroke="url(#grad2)" stroke-width="2" stroke-linecap="round"/>
            <path d="M2 12L12 17L22 12" stroke="url(#grad2)" stroke-width="2" stroke-linecap="round"/>
            <defs>
              <linearGradient id="grad1" x1="2" y1="7" x2="22" y2="7">
                <stop offset="0%" stop-color="#6366F1"/>
                <stop offset="100%" stop-color="#10B981"/>
              </linearGradient>
              <linearGradient id="grad2" x1="2" y1="17" x2="22" y2="17">
                <stop offset="0%" stop-color="#818CF8"/>
                <stop offset="100%" stop-color="#34D399"/>
              </linearGradient>
            </defs>
          </svg>
        </div>
        <div class="logo-text">
          <span class="logo-title">V3Di</span>
          <span class="logo-subtitle">3D Slicer</span>
        </div>
      </div>
    </div>
    
    <div class="header-center">
      <div v-if="store.currentStudy" class="study-info">
        <span class="badge badge-info">Active Study</span>
        <span class="study-name">{{ store.currentStudy?.patientName || 'Unknown' }}</span>
      </div>
    </div>
    
    <div class="header-right">
      <button class="btn-icon" title="Documentation">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="10"></circle>
          <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"></path>
          <line x1="12" y1="17" x2="12.01" y2="17"></line>
        </svg>
      </button>
      
      <div class="user-avatar">
        <span>U</span>
      </div>
    </div>
  </header>
</template>

<style scoped>
.app-header {
  height: 56px;
  background: var(--bg-secondary);
  border-bottom: 1px solid var(--border-primary);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 16px;
  flex-shrink: 0;
}

.header-left,
.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.header-center {
  flex: 1;
  display: flex;
  justify-content: center;
}

.btn-icon {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: none;
  border-radius: var(--radius-md);
  color: var(--text-muted);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.btn-icon:hover {
  background: var(--bg-tertiary);
  color: var(--text-primary);
}

.logo {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  padding: 6px 10px;
  border-radius: var(--radius-md);
  transition: background var(--transition-fast);
}

.logo:hover {
  background: var(--bg-tertiary);
}

.logo-icon {
  display: flex;
  align-items: center;
  justify-content: center;
}

.logo-text {
  display: flex;
  flex-direction: column;
  line-height: 1.1;
}

.logo-title {
  font-size: 16px;
  font-weight: 700;
  background: linear-gradient(135deg, var(--primary-light), var(--secondary));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.logo-subtitle {
  font-size: 10px;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.15em;
}

.study-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.study-name {
  font-weight: 600;
  color: var(--text-primary);
}

.user-avatar {
  width: 32px;
  height: 32px;
  border-radius: var(--radius-full);
  background: linear-gradient(135deg, var(--primary), var(--secondary));
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 12px;
  color: white;
  cursor: pointer;
}
</style>
