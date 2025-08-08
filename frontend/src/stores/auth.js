import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const token = ref(localStorage.getItem('token') || null)
  const refreshToken = ref(localStorage.getItem('refreshToken') || null)

  const isAuthenticated = computed(() => !!token.value)

  // Set up axios defaults
  if (token.value) {
    axios.defaults.headers.common['Authorization'] = `Bearer ${token.value}`
  }

  const login = async (credentials) => {
    try {
      const response = await axios.post('/api/auth/login/', credentials)
      const { user: userData, tokens } = response.data
      
      user.value = userData
      token.value = tokens.access
      refreshToken.value = tokens.refresh
      
      localStorage.setItem('token', tokens.access)
      localStorage.setItem('refreshToken', tokens.refresh)
      
      axios.defaults.headers.common['Authorization'] = `Bearer ${tokens.access}`
      
      return { success: true }
    } catch (error) {
      return { success: false, error: error.response?.data?.error || 'Login failed' }
    }
  }

  const register = async (userData) => {
    try {
      const response = await axios.post('/api/auth/register/', userData)
      const { user: newUser, tokens } = response.data
      
      user.value = newUser
      token.value = tokens.access
      refreshToken.value = tokens.refresh
      
      localStorage.setItem('token', tokens.access)
      localStorage.setItem('refreshToken', tokens.refresh)
      
      axios.defaults.headers.common['Authorization'] = `Bearer ${tokens.access}`
      
      return { success: true }
    } catch (error) {
      return { success: false, error: error.response?.data?.error || 'Registration failed' }
    }
  }

  const logout = async () => {
    try {
      if (refreshToken.value) {
        await axios.post('/api/auth/logout/', { refresh_token: refreshToken.value })
      }
    } catch (error) {
      console.error('Logout error:', error)
    } finally {
      user.value = null
      token.value = null
      refreshToken.value = null
      
      localStorage.removeItem('token')
      localStorage.removeItem('refreshToken')
      
      delete axios.defaults.headers.common['Authorization']
    }
  }

  const refreshAuth = async () => {
    try {
      const response = await axios.post('/api/auth/refresh/', { refresh: refreshToken.value })
      const { access } = response.data
      
      token.value = access
      localStorage.setItem('token', access)
      axios.defaults.headers.common['Authorization'] = `Bearer ${access}`
      
      return true
    } catch (error) {
      await logout()
      return false
    }
  }

  const loadUser = async () => {
    try {
      const response = await axios.get('/api/auth/profile/')
      user.value = response.data
      return true
    } catch (error) {
      if (error.response?.status === 401) {
        const refreshed = await refreshAuth()
        if (refreshed) {
          return await loadUser()
        }
      }
      return false
    }
  }

  return {
    user,
    token,
    refreshToken,
    isAuthenticated,
    login,
    register,
    logout,
    refreshAuth,
    loadUser
  }
}) 