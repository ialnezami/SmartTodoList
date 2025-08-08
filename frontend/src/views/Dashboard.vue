<template>
  <div>
    <v-row>
      <v-col cols="12">
        <h1 class="text-h4 mb-4">Dashboard</h1>
      </v-col>
    </v-row>

    <!-- Statistics Cards -->
    <v-row>
      <v-col cols="12" sm="6" md="3">
        <v-card>
          <v-card-text>
            <div class="text-h6">Total Tasks</div>
            <div class="text-h4">{{ statistics.total_tasks || 0 }}</div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" md="3">
        <v-card>
          <v-card-text>
            <div class="text-h6">Completed</div>
            <div class="text-h4 text-success">{{ statistics.completed_tasks || 0 }}</div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" md="3">
        <v-card>
          <v-card-text>
            <div class="text-h6">Pending</div>
            <div class="text-h4 text-warning">{{ statistics.pending_tasks || 0 }}</div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" md="3">
        <v-card>
          <v-card-text>
            <div class="text-h6">Overdue</div>
            <div class="text-h4 text-error">{{ statistics.overdue_tasks || 0 }}</div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Quick Actions -->
    <v-row class="mt-4">
      <v-col cols="12">
        <v-card>
          <v-card-title>Quick Actions</v-card-title>
          <v-card-text>
            <v-row>
              <v-col cols="12" sm="6" md="3">
                <v-btn
                  block
                  color="primary"
                  @click="showCreateTaskDialog = true"
                  prepend-icon="mdi-plus"
                >
                  Add Task
                </v-btn>
              </v-col>
              <v-col cols="12" sm="6" md="3">
                <v-btn
                  block
                  color="secondary"
                  @click="showNaturalLanguageDialog = true"
                  prepend-icon="mdi-brain"
                >
                  AI Task
                </v-btn>
              </v-col>
              <v-col cols="12" sm="6" md="3">
                <v-btn
                  block
                  color="info"
                  @click="$router.push('/tasks')"
                  prepend-icon="mdi-format-list-checks"
                >
                  View All Tasks
                </v-btn>
              </v-col>
              <v-col cols="12" sm="6" md="3">
                <v-btn
                  block
                  color="success"
                  @click="$router.push('/analytics')"
                  prepend-icon="mdi-chart-line"
                >
                  Analytics
                </v-btn>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Recent Tasks -->
    <v-row class="mt-4">
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title>Recent Tasks</v-card-title>
          <v-card-text>
            <v-list v-if="recentTasks.length > 0">
              <v-list-item
                v-for="task in recentTasks"
                :key="task.id"
                :title="task.title"
                :subtitle="task.category"
              >
                <template v-slot:prepend>
                  <v-icon :color="getPriorityColor(task.priority)">
                    mdi-flag
                  </v-icon>
                </template>
                <template v-slot:append>
                  <v-chip :color="getStatusColor(task.status)" size="small">
                    {{ task.status }}
                  </v-chip>
                </template>
              </v-list-item>
            </v-list>
            <v-alert v-else type="info">
              No tasks yet. Create your first task!
            </v-alert>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="6">
        <v-card>
          <v-card-title>AI Suggestions</v-card-title>
          <v-card-text>
            <v-list v-if="aiSuggestions.length > 0">
              <v-list-item
                v-for="suggestion in aiSuggestions"
                :key="suggestion.title"
                :title="suggestion.title"
                :subtitle="suggestion.category"
              >
                <template v-slot:prepend>
                  <v-icon color="primary">mdi-lightbulb</v-icon>
                </template>
                <template v-slot:append>
                  <v-btn
                    size="small"
                    color="primary"
                    @click="createTaskFromSuggestion(suggestion)"
                  >
                    Add
                  </v-btn>
                </template>
              </v-list-item>
            </v-list>
            <v-alert v-else type="info">
              No AI suggestions available yet.
            </v-alert>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Create Task Dialog -->
    <v-dialog v-model="showCreateTaskDialog" max-width="500px">
      <v-card>
        <v-card-title>Create New Task</v-card-title>
        <v-card-text>
          <v-form @submit.prevent="createTask">
            <v-text-field
              v-model="newTask.title"
              label="Task Title"
              required
            />
            <v-textarea
              v-model="newTask.description"
              label="Description"
              rows="3"
            />
            <v-select
              v-model="newTask.category"
              :items="categories"
              label="Category"
            />
            <v-select
              v-model="newTask.priority"
              :items="priorities"
              label="Priority"
            />
            <v-text-field
              v-model="newTask.due_date"
              label="Due Date"
              type="datetime-local"
            />
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn @click="showCreateTaskDialog = false">Cancel</v-btn>
          <v-btn color="primary" @click="createTask" :loading="loading">
            Create
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Natural Language Dialog -->
    <v-dialog v-model="showNaturalLanguageDialog" max-width="500px">
      <v-card>
        <v-card-title>Create Task with AI</v-card-title>
        <v-card-text>
          <v-textarea
            v-model="naturalLanguageInput"
            label="Describe your task in natural language"
            placeholder="e.g., Buy groceries tomorrow at 2pm"
            rows="3"
          />
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn @click="showNaturalLanguageDialog = false">Cancel</v-btn>
          <v-btn color="primary" @click="parseNaturalLanguage" :loading="loading">
            Parse & Create
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useTasksStore } from '@/stores/tasks'
import axios from 'axios'

const tasksStore = useTasksStore()

const statistics = ref({})
const aiSuggestions = ref([])
const recentTasks = ref([])
const loading = ref(false)
const showCreateTaskDialog = ref(false)
const showNaturalLanguageDialog = ref(false)

const newTask = ref({
  title: '',
  description: '',
  category: 'personal',
  priority: 3,
  due_date: ''
})

const naturalLanguageInput = ref('')

const categories = [
  'personal', 'work', 'health', 'shopping', 'finance', 'education', 'travel', 'home'
]

const priorities = [
  { title: 'Very Low', value: 1 },
  { title: 'Low', value: 2 },
  { title: 'Medium', value: 3 },
  { title: 'High', value: 4 },
  { title: 'Very High', value: 5 }
]

const getPriorityColor = (priority) => {
  const colors = ['', 'grey', 'blue', 'orange', 'red', 'purple']
  return colors[priority] || 'grey'
}

const getStatusColor = (status) => {
  const colors = {
    pending: 'warning',
    in_progress: 'info',
    completed: 'success'
  }
  return colors[status] || 'grey'
}

const loadDashboard = async () => {
  loading.value = true
  try {
    // Load statistics
    const statsResponse = await axios.get('/api/tasks/statistics/')
    statistics.value = statsResponse.data

    // Load recent tasks
    const tasksResponse = await axios.get('/api/tasks/?ordering=-created_at&limit=5')
    recentTasks.value = tasksResponse.data.results || tasksResponse.data

    // Load AI suggestions
    const suggestionsResponse = await axios.get('/api/ai/suggestions/')
    aiSuggestions.value = suggestionsResponse.data.suggestions || []
  } catch (error) {
    console.error('Error loading dashboard:', error)
  } finally {
    loading.value = false
  }
}

const createTask = async () => {
  if (!newTask.value.title) return

  const result = await tasksStore.createTask(newTask.value)
  if (result.success) {
    showCreateTaskDialog.value = false
    newTask.value = {
      title: '',
      description: '',
      category: 'personal',
      priority: 3,
      due_date: ''
    }
    await loadDashboard()
  }
}

const parseNaturalLanguage = async () => {
  if (!naturalLanguageInput.value) return

  loading.value = true
  try {
    const response = await axios.post('/api/ai/parse-natural/', {
      text: naturalLanguageInput.value
    })
    
    const parsedTask = response.data
    const result = await tasksStore.createTask(parsedTask)
    
    if (result.success) {
      showNaturalLanguageDialog.value = false
      naturalLanguageInput.value = ''
      await loadDashboard()
    }
  } catch (error) {
    console.error('Error parsing natural language:', error)
  } finally {
    loading.value = false
  }
}

const createTaskFromSuggestion = async (suggestion) => {
  const taskData = {
    title: suggestion.title,
    category: suggestion.category,
    priority: suggestion.priority,
    estimated_duration: suggestion.estimated_duration
  }
  
  const result = await tasksStore.createTask(taskData)
  if (result.success) {
    await loadDashboard()
  }
}

onMounted(() => {
  loadDashboard()
})
</script> 