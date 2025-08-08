<template>
  <v-app>
    <v-navigation-drawer v-model="drawer" app>
      <v-list>
        <v-list-item
          prepend-avatar="https://randomuser.me/api/portraits/men/85.jpg"
          :title="user?.first_name || user?.username || 'User'"
          :subtitle="user?.email || ''"
        ></v-list-item>
      </v-list>

      <v-divider></v-divider>

      <v-list density="compact" nav>
        <v-list-item
          prepend-icon="mdi-view-dashboard"
          title="Dashboard"
          value="dashboard"
          to="/"
        ></v-list-item>
        <v-list-item
          prepend-icon="mdi-format-list-checks"
          title="Tasks"
          value="tasks"
          to="/tasks"
        ></v-list-item>
        <v-list-item
          prepend-icon="mdi-brain"
          title="AI Insights"
          value="insights"
          to="/insights"
        ></v-list-item>
        <v-list-item
          prepend-icon="mdi-chart-line"
          title="Analytics"
          value="analytics"
          to="/analytics"
        ></v-list-item>
        <v-list-item
          prepend-icon="mdi-bell"
          title="Notifications"
          value="notifications"
          to="/notifications"
        ></v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-app-bar app>
      <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
      <v-toolbar-title>Smart AI TodoList</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn icon @click="logout">
        <v-icon>mdi-logout</v-icon>
      </v-btn>
    </v-app-bar>

    <v-main>
      <v-container fluid>
        <router-view />
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const drawer = ref(true)
const router = useRouter()
const authStore = useAuthStore()

const user = computed(() => authStore.user)

const logout = async () => {
  await authStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.v-navigation-drawer {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.v-list-item {
  color: white;
}

.v-list-item:hover {
  background-color: rgba(255, 255, 255, 0.1);
}
</style> 