import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: () => import('../views/DashboardView.vue')
  },
  {
    path: '/viewer',
    name: 'Viewer',
    component: () => import('../views/ViewerView.vue')
  },
  {
    path: '/segmentation',
    name: 'Segmentation',
    component: () => import('../views/SegmentationView.vue')
  },
  {
    path: '/settings',
    name: 'Settings',
    component: () => import('../views/SettingsView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
