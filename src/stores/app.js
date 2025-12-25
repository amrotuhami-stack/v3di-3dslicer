import { defineStore } from 'pinia'

export const useAppStore = defineStore('app', {
  state: () => ({
    // API Configuration
    backendUrl: import.meta.env.VITE_BACKEND_URL || 'https://api.v3di-slicer.com',
    
    // User session
    user: null,
    
    // Active study/series
    currentStudy: null,
    currentSeries: null,
    
    // Processing state
    isProcessing: false,
    processingJob: null,
    processingProgress: 0,
    processingMessage: '',
    
    // Available STL files
    stlFiles: [],
    
    // UI state
    sidebarCollapsed: false,
    activePanel: 'viewer'
  }),
  
  getters: {
    hasActiveStudy: (state) => !!state.currentStudy,
    hasStlFiles: (state) => state.stlFiles.length > 0
  },
  
  actions: {
    setStudy(study, series) {
      this.currentStudy = study
      this.currentSeries = series
    },
    
    clearStudy() {
      this.currentStudy = null
      this.currentSeries = null
      this.stlFiles = []
    },
    
    setProcessing(isProcessing, message = '') {
      this.isProcessing = isProcessing
      this.processingMessage = message
      if (!isProcessing) {
        this.processingProgress = 0
        this.processingJob = null
      }
    },
    
    updateProgress(progress, message) {
      this.processingProgress = progress
      if (message) this.processingMessage = message
    },
    
    addStlFile(file) {
      this.stlFiles.push(file)
    },
    
    clearStlFiles() {
      this.stlFiles = []
    },
    
    toggleSidebar() {
      this.sidebarCollapsed = !this.sidebarCollapsed
    }
  }
})
