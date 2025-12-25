<script setup>
import { ref } from 'vue'

const backendUrl = ref(import.meta.env.VITE_BACKEND_URL || 'https://api.v3di-slicer.com')
const awsRegion = ref('eu-west-2')
</script>

<template>
  <div class="settings-page">
    <div class="page-header">
      <h1>Settings</h1>
      <p class="text-muted">Configure V3Di 3D Slicer</p>
    </div>
    
    <div class="settings-grid">
      <!-- Backend Configuration -->
      <div class="card">
        <div class="card-header">
          <span class="card-title">Backend Configuration</span>
        </div>
        
        <div class="form-group">
          <label class="form-label">Backend URL</label>
          <input type="text" class="form-input" v-model="backendUrl" />
        </div>
        
        <div class="form-group">
          <label class="form-label">AWS Region</label>
          <select class="form-input form-select" v-model="awsRegion">
            <option value="eu-west-2">EU (London)</option>
            <option value="us-east-1">US East (N. Virginia)</option>
            <option value="us-west-2">US West (Oregon)</option>
          </select>
        </div>
        
        <button class="btn btn-primary">Save Configuration</button>
      </div>
      
      <!-- About -->
      <div class="card">
        <div class="card-header">
          <span class="card-title">About</span>
        </div>
        
        <div class="about-info">
          <div class="about-row">
            <span class="about-label">Version</span>
            <span class="about-value">1.0.0</span>
          </div>
          <div class="about-row">
            <span class="about-label">3D Slicer</span>
            <span class="about-value">5.6.x</span>
          </div>
          <div class="about-row">
            <span class="about-label">nnU-Net</span>
            <span class="about-value">2.x</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.settings-page {
  padding: 24px;
  max-width: 800px;
}

.page-header {
  margin-bottom: 24px;
}

.page-header h1 {
  margin-bottom: 4px;
}

.settings-grid {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.about-info {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.about-row {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  border-bottom: 1px solid var(--border-primary);
}

.about-row:last-child {
  border-bottom: none;
}

.about-label {
  color: var(--text-muted);
}

.about-value {
  font-weight: 600;
  color: var(--text-primary);
}
</style>
