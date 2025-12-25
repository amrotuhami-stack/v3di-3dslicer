<script setup>
import { ref } from 'vue'

const viewerReady = ref(false)
</script>

<template>
  <div class="viewer-page">
    <div class="viewer-toolbar">
      <div class="toolbar-group">
        <button class="btn btn-secondary">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
            <line x1="9" y1="3" x2="9" y2="21"></line>
          </svg>
          Layout
        </button>
        <button class="btn btn-secondary">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="11" cy="11" r="8"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
            <line x1="11" y1="8" x2="11" y2="14"></line>
            <line x1="8" y1="11" x2="14" y2="11"></line>
          </svg>
          Zoom
        </button>
        <button class="btn btn-secondary">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="12" y1="8" x2="12" y2="12"></line>
            <line x1="12" y1="16" x2="12.01" y2="16"></line>
          </svg>
          Window/Level
        </button>
      </div>
      
      <div class="toolbar-group">
        <button class="btn btn-primary">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
            <polyline points="17 8 12 3 7 8"></polyline>
            <line x1="12" y1="3" x2="12" y2="15"></line>
          </svg>
          Upload DICOM
        </button>
      </div>
    </div>
    
    <div class="viewer-container">
      <div class="viewer-placeholder">
        <div class="placeholder-content">
          <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" style="color: var(--text-muted);">
            <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
            <circle cx="12" cy="12" r="3"></circle>
          </svg>
          <h3>DICOM Viewer</h3>
          <p class="text-muted">Upload a DICOM study to start viewing</p>
          <button class="btn btn-primary" style="margin-top: 16px;">
            Upload DICOM
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.viewer-page {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.viewer-toolbar {
  height: 48px;
  background: var(--bg-secondary);
  border-bottom: 1px solid var(--border-primary);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 16px;
  flex-shrink: 0;
}

.toolbar-group {
  display: flex;
  gap: 8px;
}

.viewer-container {
  flex: 1;
  display: flex;
  background: var(--bg-primary);
}

.viewer-placeholder {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-secondary);
  margin: 16px;
  border-radius: var(--radius-lg);
  border: 2px dashed var(--border-primary);
}

.placeholder-content {
  text-align: center;
  padding: 40px;
}

.placeholder-content h3 {
  margin-top: 16px;
  margin-bottom: 8px;
}
</style>
