<script setup>
import { ref } from 'vue'
import { useAppStore } from '../stores/app'

const store = useAppStore()

const selectedModel = ref('teeth')
const isRunning = ref(false)

const models = [
  { id: 'teeth', name: 'Teeth Segmentation', description: 'Segment individual teeth from CBCT' },
  { id: 'anatomy', name: 'Anatomy Segmentation', description: 'Segment maxilla, mandible, canals' },
  { id: 'implant', name: 'Implant Planning', description: 'Plan dental implant placement' },
]

const runSegmentation = async () => {
  isRunning.value = true
  store.setProcessing(true, 'Initializing 3D Slicer...')
  
  // Simulated progress
  const steps = [
    { progress: 10, message: 'Loading volume...' },
    { progress: 30, message: 'Preprocessing data...' },
    { progress: 50, message: 'Running AI model...' },
    { progress: 70, message: 'Generating meshes...' },
    { progress: 90, message: 'Uploading results...' },
    { progress: 100, message: 'Complete!' },
  ]
  
  for (const step of steps) {
    await new Promise(r => setTimeout(r, 1000))
    store.updateProgress(step.progress, step.message)
  }
  
  await new Promise(r => setTimeout(r, 500))
  store.setProcessing(false)
  isRunning.value = false
}
</script>

<template>
  <div class="segmentation-page">
    <div class="page-header">
      <h1>AI Segmentation</h1>
      <p class="text-muted">Powered by 3D Slicer + nnU-Net</p>
    </div>
    
    <div class="content-grid">
      <!-- Model Selection -->
      <div class="panel">
        <div class="panel-header">
          <span class="panel-title">Select Model</span>
        </div>
        <div class="panel-content">
          <div class="model-list">
            <label
              v-for="model in models"
              :key="model.id"
              class="model-option"
              :class="{ selected: selectedModel === model.id }"
            >
              <input
                type="radio"
                :value="model.id"
                v-model="selectedModel"
                hidden
              />
              <div class="model-radio"></div>
              <div class="model-info">
                <span class="model-name">{{ model.name }}</span>
                <span class="model-desc">{{ model.description }}</span>
              </div>
            </label>
          </div>
          
          <button
            class="btn btn-primary w-full"
            style="margin-top: 20px;"
            @click="runSegmentation"
            :disabled="isRunning"
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polygon points="5 3 19 12 5 21 5 3"></polygon>
            </svg>
            {{ isRunning ? 'Processing...' : 'Run Segmentation' }}
          </button>
        </div>
      </div>
      
      <!-- Results Panel -->
      <div class="panel">
        <div class="panel-header">
          <span class="panel-title">Results</span>
        </div>
        <div class="panel-content">
          <div v-if="store.stlFiles.length === 0" class="empty-state">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" style="color: var(--text-muted);">
              <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path>
            </svg>
            <p class="text-muted" style="margin-top: 12px;">No segmentation results yet</p>
            <p class="text-muted" style="font-size: 12px;">Run a segmentation to generate STL files</p>
          </div>
          
          <div v-else class="stl-list">
            <div v-for="file in store.stlFiles" :key="file.id" class="stl-item">
              <span>{{ file.name }}</span>
              <button class="btn btn-secondary" style="padding: 4px 8px; font-size: 11px;">
                Download
              </button>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 3D Preview -->
      <div class="preview-panel">
        <div class="panel-header">
          <span class="panel-title">3D Preview</span>
        </div>
        <div class="preview-container">
          <div class="preview-placeholder">
            <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" style="color: var(--text-muted);">
              <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path>
              <polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline>
              <line x1="12" y1="22.08" x2="12" y2="12"></line>
            </svg>
            <p class="text-muted" style="margin-top: 16px;">3D Preview Area</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.segmentation-page {
  padding: 24px;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.page-header {
  margin-bottom: 24px;
}

.page-header h1 {
  margin-bottom: 4px;
}

.content-grid {
  display: grid;
  grid-template-columns: 300px 300px 1fr;
  gap: 16px;
  flex: 1;
  min-height: 0;
}

.panel {
  background: var(--bg-secondary);
  border: 1px solid var(--border-primary);
  border-radius: var(--radius-lg);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.panel-header {
  padding: 16px;
  border-bottom: 1px solid var(--border-primary);
  background: linear-gradient(135deg, var(--primary-soft), transparent);
}

.panel-title {
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--primary-light);
}

.panel-content {
  padding: 16px;
  flex: 1;
  overflow-y: auto;
}

.model-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.model-option {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 12px;
  border: 1px solid var(--border-primary);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.model-option:hover {
  background: var(--bg-tertiary);
}

.model-option.selected {
  border-color: var(--primary);
  background: var(--primary-soft);
}

.model-radio {
  width: 18px;
  height: 18px;
  border: 2px solid var(--border-light);
  border-radius: 50%;
  flex-shrink: 0;
  margin-top: 2px;
  position: relative;
}

.model-option.selected .model-radio {
  border-color: var(--primary);
}

.model-option.selected .model-radio::after {
  content: '';
  position: absolute;
  top: 3px;
  left: 3px;
  width: 8px;
  height: 8px;
  background: var(--primary);
  border-radius: 50%;
}

.model-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.model-name {
  font-weight: 600;
  color: var(--text-primary);
}

.model-desc {
  font-size: 12px;
  color: var(--text-muted);
}

.empty-state {
  text-align: center;
  padding: 32px 16px;
}

.stl-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.stl-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 12px;
  background: var(--bg-tertiary);
  border-radius: var(--radius-md);
}

.preview-panel {
  background: var(--bg-secondary);
  border: 1px solid var(--border-primary);
  border-radius: var(--radius-lg);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.preview-container {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.preview-placeholder {
  text-align: center;
}
</style>
