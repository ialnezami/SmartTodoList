<template>
  <div>
    <v-row>
      <v-col cols="12">
        <div class="d-flex justify-space-between align-center">
          <h1 class="text-h4">Notifications</h1>
          <v-btn
            v-if="notifications.length > 0"
            color="primary"
            @click="markAllAsRead"
            :loading="loading"
          >
            Mark All as Read
          </v-btn>
        </div>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-text>
            <v-list v-if="notifications.length > 0">
              <v-list-item
                v-for="notification in notifications"
                :key="notification.id"
                :class="{ 'unread': !notification.is_read }"
              >
                <template v-slot:prepend>
                  <v-icon :color="getNotificationColor(notification.type)">
                    {{ getNotificationIcon(notification.type) }}
                  </v-icon>
                </template>
                
                <v-list-item-title>
                  {{ notification.title }}
                </v-list-item-title>
                
                <v-list-item-subtitle>
                  {{ notification.message }}
                  <div class="text-caption mt-1">
                    {{ formatDate(notification.created_at) }}
                  </div>
                </v-list-item-subtitle>

                <template v-slot:append>
                  <v-btn
                    v-if="!notification.is_read"
                    size="small"
                    color="primary"
                    @click="markAsRead(notification.id)"
                  >
                    Mark Read
                  </v-btn>
                </template>
              </v-list-item>
            </v-list>
            <v-alert v-else type="info">
              No notifications yet.
            </v-alert>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { format } from 'date-fns'

const notifications = ref([])
const loading = ref(false)

const loadNotifications = async () => {
  loading.value = true
  try {
    const response = await axios.get('/api/notifications/')
    notifications.value = response.data
  } catch (error) {
    console.error('Error loading notifications:', error)
  } finally {
    loading.value = false
  }
}

const markAsRead = async (notificationId) => {
  try {
    await axios.post(`/api/notifications/${notificationId}/read/`)
    const notification = notifications.value.find(n => n.id === notificationId)
    if (notification) {
      notification.is_read = true
    }
  } catch (error) {
    console.error('Error marking notification as read:', error)
  }
}

const markAllAsRead = async () => {
  loading.value = true
  try {
    const unreadNotifications = notifications.value.filter(n => !n.is_read)
    for (const notification of unreadNotifications) {
      await markAsRead(notification.id)
    }
  } catch (error) {
    console.error('Error marking all notifications as read:', error)
  } finally {
    loading.value = false
  }
}

const getNotificationColor = (type) => {
  const colors = {
    task_due: 'warning',
    task_overdue: 'error',
    reminder: 'info',
    system: 'primary'
  }
  return colors[type] || 'grey'
}

const getNotificationIcon = (type) => {
  const icons = {
    task_due: 'mdi-clock-alert',
    task_overdue: 'mdi-alert-circle',
    reminder: 'mdi-bell',
    system: 'mdi-cog'
  }
  return icons[type] || 'mdi-bell'
}

const formatDate = (date) => {
  if (!date) return ''
  return format(new Date(date), 'MMM dd, yyyy HH:mm')
}

onMounted(() => {
  loadNotifications()
})
</script>

<style scoped>
.unread {
  background-color: rgba(33, 150, 243, 0.1);
}
</style> 