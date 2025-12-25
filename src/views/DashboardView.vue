<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAppStore } from '../stores/app'

const router = useRouter()
const store = useAppStore()

const recentStudies = ref([
  { id: 1, patientName: 'Sample Patient', date: '2024-12-25', type: 'CBCT', status: 'completed' },
])

const quickActions = [
  { icon: 'upload', label: 'Upload DICOM', action: () => {} },
  { icon: 'segment', label: 'Start Segmentation', action: () => router.push('/segmentation') },
  { icon: 'viewer', label: 'Open Viewer', action: () => router.push('/viewer') },
]
</script>

<template>
  <div class="dashboard">
    <div class="dashboard-header">
      <h1>Dashboard</h1>
      <p class="text-muted">Welcome to V3Di 3D Slicer</p>
    </div>
    
    <!-- Stats Cards -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon" style="background: var(--primary-soft); color: var(--primary-light);">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
            <polyline points="14 2 14 8 20 8"></polyline>
          </svg>
        </div>
        <div class="stat-content">
          <span class="stat-value">{{ recentStudies.length }}</span>
          <span class="stat-label">Studies</span>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon" style="background: rgba(16, 185, 129, 0.15); color: var(--secondary);">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path>
          </svg>
        </div>
        <div class="stat-content">
          <span class="stat-value">{{ store.stlFiles.length }}</span>
          <span class="stat-label">STL Files</span>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon" style="background: rgba(245, 158, 11, 0.15); color: var(--accent);">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"></circle>
            <polyline points="12 6 12 12 16 14"></polyline>
          </svg>
        </div>
        <div class="stat-content">
          <span class="stat-value">0</span>
          <span class="stat-label">Pending Jobs</span>
        </div>
      </div>
    </div>
    
    <!-- Quick Actions -->
    <div class="section">
      <h3>Quick Actions</h3>
      <div class="actions-grid">
        <button v-for="action in quickActions" :key="action.label" class="action-card" @click="action.action">
          <div class="action-icon">
            <svg v-if="action.icon === 'upload'" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
              <polyline points="17 8 12 3 7 8"></polyline>
              <line x1="12" y1="3" x2="12" y2="15"></line>
            </svg>
            <svg v-if="action.icon === 'segment'" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path>
            </svg>
            <svg v-if="action.icon === 'viewer'" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
              <circle cx="12" cy="12" r="3"></circle>
            </svg>
          </div>
          <span>{{ action.label }}</span>
        </button>
      </div>
    </div>
    
    <!-- Recent Studies -->
    <div class="section">
      <h3>Recent Studies</h3>
      <div class="studies-table">
        <table>
          <thead>
            <tr>
              <th>Patient</th>
              <th>Date</th>
              <th>Type</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="study in recentStudies" :key="study.id">
              <td>{{ study.patientName }}</td>
              <td>{{ study.date }}</td>
              <td>{{ study.type }}</td>
              <td><span :class="['badge', 'badge-' + study.status]">{{ study.status }}</span></td>
              <td>
                <button class="btn btn-secondary" style="padding: 6px 12px; font-size: 12px;">Open</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<style scoped>
.dashboard {
  padding: 24px;
  max-width: 1200px;
}

.dashboard-header {
  margin-bottom: 24px;
}

.dashboard-header h1 {
  margin-bottom: 4px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
  margin-bottom: 32px;
}

.stat-card {
  background: var(--bg-secondary);
  border: 1px solid var(--border-primary);
  border-radius: var(--radius-lg);
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 16px;
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-content {
  display: flex;
  flex-direction: column;
}

.stat-value {
  font-size: 24px;
  font-weight: 700;
  color: var(--text-primary);
}

.stat-label {
  font-size: 12px;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.section {
  margin-bottom: 32px;
}

.section h3 {
  margin-bottom: 16px;
  color: var(--text-muted);
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.1em;
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 12px;
}

.action-card {
  background: var(--bg-secondary);
  border: 1px solid var(--border-primary);
  border-radius: var(--radius-lg);
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  transition: all var(--transition-fast);
  color: var(--text-primary);
}

.action-card:hover {
  background: var(--bg-tertiary);
  border-color: var(--primary);
  transform: translateY(-2px);
}

.action-icon {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-md);
  background: var(--primary-soft);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--primary-light);
}

.studies-table {
  background: var(--bg-secondary);
  border: 1px solid var(--border-primary);
  border-radius: var(--radius-lg);
  overflow: hidden;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 12px 16px;
  text-align: left;
}

th {
  background: var(--bg-tertiary);
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-muted);
  font-weight: 600;
}

td {
  border-top: 1px solid var(--border-primary);
  color: var(--text-secondary);
}

.badge-completed {
  background: rgba(16, 185, 129, 0.2);
  color: var(--secondary-light);
}
</style>
