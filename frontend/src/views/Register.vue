<template>
  <v-container fluid fill-height class="register-container">
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="4">
        <v-card class="elevation-12">
          <v-toolbar color="primary" dark flat>
            <v-toolbar-title>Register for Smart TodoList</v-toolbar-title>
          </v-toolbar>
          <v-card-text>
            <v-form @submit.prevent="handleRegister">
              <v-text-field
                v-model="form.username"
                label="Username"
                name="username"
                prepend-icon="mdi-account"
                type="text"
                required
              />
              <v-text-field
                v-model="form.email"
                label="Email"
                name="email"
                prepend-icon="mdi-email"
                type="email"
                required
              />
              <v-text-field
                v-model="form.first_name"
                label="First Name"
                name="first_name"
                prepend-icon="mdi-account-details"
                type="text"
              />
              <v-text-field
                v-model="form.last_name"
                label="Last Name"
                name="last_name"
                prepend-icon="mdi-account-details"
                type="text"
              />
              <v-text-field
                v-model="form.password"
                label="Password"
                name="password"
                prepend-icon="mdi-lock"
                type="password"
                required
              />
            </v-form>
          </v-card-text>
          <v-card-actions>
            <v-spacer />
            <v-btn color="primary" @click="handleRegister" :loading="loading">
              Register
            </v-btn>
          </v-card-actions>
          <v-card-text class="text-center">
            <router-link to="/login">Already have an account? Login here</router-link>
          </v-card-text>
        </v-card>
        <v-alert v-if="error" type="error" class="mt-4">
          {{ error }}
        </v-alert>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const form = ref({
  username: '',
  email: '',
  first_name: '',
  last_name: '',
  password: ''
})

const loading = ref(false)
const error = ref('')

const handleRegister = async () => {
  if (!form.value.username || !form.value.email || !form.value.password) {
    error.value = 'Please fill in all required fields'
    return
  }

  loading.value = true
  error.value = ''

  const result = await authStore.register(form.value)
  
  if (result.success) {
    router.push('/')
  } else {
    error.value = result.error
  }
  
  loading.value = false
}
</script>

<style scoped>
.register-container {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
</style> 