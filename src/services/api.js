import axios from 'axios'

const API_BASE = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8001'

const api = axios.create({
  baseURL: API_BASE,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Health check
export const checkHealth = async () => {
  const response = await api.get('/health')
  return response.data
}

// Upload DICOM
export const uploadDicom = async (file, onProgress) => {
  const formData = new FormData()
  formData.append('file', file)
  
  const response = await api.post('/upload-dicom', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
    onUploadProgress: (progressEvent) => {
      if (onProgress) {
        const percent = Math.round((progressEvent.loaded * 100) / progressEvent.total)
        onProgress(percent)
      }
    }
  })
  
  return response.data
}

// Start segmentation
export const startSegmentation = async (studyId, modelType = 'teeth') => {
  const response = await api.post('/segment', {
    study_id: studyId,
    model_type: modelType
  })
  return response.data
}

// Get job status
export const getJobStatus = async (jobId) => {
  const response = await api.get(`/status/${jobId}`)
  return response.data
}

// List jobs
export const listJobs = async () => {
  const response = await api.get('/jobs')
  return response.data
}

// Download STL - returns URL
export const getStlDownloadUrl = (jobId, filename) => {
  return `${API_BASE}/download/stl/${jobId}/${filename}`
}

// Poll job status until complete
export const pollJobStatus = async (jobId, onProgress, intervalMs = 2000) => {
  return new Promise((resolve, reject) => {
    const poll = async () => {
      try {
        const status = await getJobStatus(jobId)
        
        if (onProgress) {
          onProgress(status)
        }
        
        if (status.status === 'completed') {
          resolve(status)
        } else if (status.status === 'failed') {
          reject(new Error(status.message || 'Job failed'))
        } else {
          setTimeout(poll, intervalMs)
        }
      } catch (error) {
        reject(error)
      }
    }
    
    poll()
  })
}

export default api
