import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'

export const useTasksStore = defineStore('tasks', () => {
  const tasks = ref([])
  const loading = ref(false)
  const error = ref(null)

  const pendingTasks = computed(() => tasks.value.filter(task => task.status === 'pending'))
  const inProgressTasks = computed(() => tasks.value.filter(task => task.status === 'in_progress'))
  const completedTasks = computed(() => tasks.value.filter(task => task.status === 'completed'))
  const overdueTasks = computed(() => tasks.value.filter(task => task.is_overdue))

  const fetchTasks = async () => {
    loading.value = true
    error.value = null
    try {
      const response = await axios.get('/api/tasks/')
      tasks.value = response.data.results || response.data
    } catch (err) {
      error.value = err.response?.data?.error || 'Failed to fetch tasks'
    } finally {
      loading.value = false
    }
  }

  const createTask = async (taskData) => {
    loading.value = true
    error.value = null
    try {
      const response = await axios.post('/api/tasks/', taskData)
      tasks.value.unshift(response.data)
      return { success: true, task: response.data }
    } catch (err) {
      error.value = err.response?.data?.error || 'Failed to create task'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  const updateTask = async (taskId, taskData) => {
    loading.value = true
    error.value = null
    try {
      const response = await axios.put(`/api/tasks/${taskId}/`, taskData)
      const index = tasks.value.findIndex(task => task.id === taskId)
      if (index !== -1) {
        tasks.value[index] = response.data
      }
      return { success: true, task: response.data }
    } catch (err) {
      error.value = err.response?.data?.error || 'Failed to update task'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  const deleteTask = async (taskId) => {
    loading.value = true
    error.value = null
    try {
      await axios.delete(`/api/tasks/${taskId}/`)
      const index = tasks.value.findIndex(task => task.id === taskId)
      if (index !== -1) {
        tasks.value.splice(index, 1)
      }
      return { success: true }
    } catch (err) {
      error.value = err.response?.data?.error || 'Failed to delete task'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  const bulkUpdateTasks = async (taskIds, updateData) => {
    loading.value = true
    error.value = null
    try {
      await axios.post('/api/tasks/bulk-update/', {
        task_ids: taskIds,
        update_data: updateData
      })
      await fetchTasks()
      return { success: true }
    } catch (err) {
      error.value = err.response?.data?.error || 'Failed to update tasks'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  const bulkDeleteTasks = async (taskIds) => {
    loading.value = true
    error.value = null
    try {
      await axios.delete('/api/tasks/bulk-delete/', {
        data: { task_ids: taskIds }
      })
      tasks.value = tasks.value.filter(task => !taskIds.includes(task.id))
      return { success: true }
    } catch (err) {
      error.value = err.response?.data?.error || 'Failed to delete tasks'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  const getTaskStatistics = async () => {
    try {
      const response = await axios.get('/api/tasks/statistics/')
      return response.data
    } catch (err) {
      error.value = err.response?.data?.error || 'Failed to fetch statistics'
      return null
    }
  }

  return {
    tasks,
    loading,
    error,
    pendingTasks,
    inProgressTasks,
    completedTasks,
    overdueTasks,
    fetchTasks,
    createTask,
    updateTask,
    deleteTask,
    bulkUpdateTasks,
    bulkDeleteTasks,
    getTaskStatistics
  }
}) 