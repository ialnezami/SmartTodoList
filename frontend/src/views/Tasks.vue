<template>
  <div>
    <v-row>
      <v-col cols="12">
        <div class="d-flex justify-space-between align-center">
          <h1 class="text-h4">Tasks</h1>
          <v-btn color="primary" @click="showCreateDialog = true" prepend-icon="mdi-plus">
            Add Task
          </v-btn>
        </div>
      </v-col>
    </v-row>

    <!-- Filters -->
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-text>
            <v-row>
              <v-col cols="12" sm="6" md="3">
                <v-select
                  v-model="filters.status"
                  :items="statusOptions"
                  label="Status"
                  clearable
                />
              </v-col>
              <v-col cols="12" sm="6" md="3">
                <v-select
                  v-model="filters.category"
                  :items="categoryOptions"
                  label="Category"
                  clearable
                />
              </v-col>
              <v-col cols="12" sm="6" md="3">
                <v-select
                  v-model="filters.priority"
                  :items="priorityOptions"
                  label="Priority"
                  clearable
                />
              </v-col>
              <v-col cols="12" sm="6" md="3">
                <v-text-field
                  v-model="filters.search"
                  label="Search"
                  prepend-icon="mdi-magnify"
                  clearable
                />
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Tasks List -->
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title>
            <v-checkbox
              v-model="selectAll"
              @change="toggleSelectAll"
              hide-details
            />
            <span class="ml-2">Tasks ({{ filteredTasks.length }})</span>
            <v-spacer />
            <v-btn
              v-if="selectedTasks.length > 0"
              color="error"
              @click="bulkDelete"
              :loading="loading"
            >
              Delete Selected ({{ selectedTasks.length }})
            </v-btn>
          </v-card-title>
          <v-card-text>
            <v-list v-if="filteredTasks.length > 0">
              <v-list-item
                v-for="task in filteredTasks"
                :key="task.id"
                :class="{ 'overdue': task.is_overdue }"
              >
                <template v-slot:prepend>
                  <v-checkbox
                    v-model="selectedTasks"
                    :value="task.id"
                    hide-details
                  />
                </template>
                
                <v-list-item-title>
                  <div class="d-flex align-center">
                    <span :class="{ 'text-decoration-line-through': task.status === 'completed' }">
                      {{ task.title }}
                    </span>
                    <v-chip
                      v-if="task.is_overdue"
                      color="error"
                      size="small"
                      class="ml-2"
                    >
                      Overdue
                    </v-chip>
                  </div>
                </v-list-item-title>
                
                <v-list-item-subtitle>
                  {{ task.description }}
                  <div class="mt-1">
                    <v-chip size="small" :color="getPriorityColor(task.priority)" class="mr-2">
                      Priority {{ task.priority }}
                    </v-chip>
                    <v-chip size="small" :color="getStatusColor(task.status)" class="mr-2">
                      {{ task.status }}
                    </v-chip>
                    <v-chip size="small" color="grey" class="mr-2">
                      {{ task.category }}
                    </v-chip>
                    <span v-if="task.due_date" class="text-caption">
                      Due: {{ formatDate(task.due_date) }}
                    </span>
                  </div>
                </v-list-item-subtitle>

                <template v-slot:append>
                  <v-menu>
                    <template v-slot:activator="{ props }">
                      <v-btn icon v-bind="props">
                        <v-icon>mdi-dots-vertical</v-icon>
                      </v-btn>
                    </template>
                    <v-list>
                      <v-list-item @click="editTask(task)">
                        <v-list-item-title>Edit</v-list-item-title>
                      </v-list-item>
                      <v-list-item @click="toggleTaskStatus(task)">
                        <v-list-item-title>
                          {{ task.status === 'completed' ? 'Mark Incomplete' : 'Mark Complete' }}
                        </v-list-item-title>
                      </v-list-item>
                      <v-list-item @click="deleteTask(task.id)">
                        <v-list-item-title class="text-error">Delete</v-list-item-title>
                      </v-list-item>
                    </v-list>
                  </v-menu>
                </template>
              </v-list-item>
            </v-list>
            <v-alert v-else type="info">
              No tasks found. Create your first task!
            </v-alert>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Create/Edit Task Dialog -->
    <v-dialog v-model="showCreateDialog" max-width="600px">
      <v-card>
        <v-card-title>
          {{ editingTask ? 'Edit Task' : 'Create New Task' }}
        </v-card-title>
        <v-card-text>
          <v-form @submit.prevent="saveTask">
            <v-text-field
              v-model="taskForm.title"
              label="Task Title"
              required
            />
            <v-textarea
              v-model="taskForm.description"
              label="Description"
              rows="3"
            />
            <v-row>
              <v-col cols="6">
                <v-select
                  v-model="taskForm.category"
                  :items="categories"
                  label="Category"
                />
              </v-col>
              <v-col cols="6">
                <v-select
                  v-model="taskForm.priority"
                  :items="priorities"
                  label="Priority"
                />
              </v-col>
            </v-row>
            <v-text-field
              v-model="taskForm.due_date"
              label="Due Date"
              type="datetime-local"
            />
            <v-text-field
              v-model="taskForm.estimated_duration"
              label="Estimated Duration (minutes)"
              type="number"
            />
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn @click="showCreateDialog = false">Cancel</v-btn>
          <v-btn color="primary" @click="saveTask" :loading="loading">
            {{ editingTask ? 'Update' : 'Create' }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useTasksStore } from '@/stores/tasks'
import { format } from 'date-fns'

const tasksStore = useTasksStore()

const loading = ref(false)
const showCreateDialog = ref(false)
const editingTask = ref(null)
const selectedTasks = ref([])

const filters = ref({
  status: '',
  category: '',
  priority: '',
  search: ''
})

const taskForm = ref({
  title: '',
  description: '',
  category: 'personal',
  priority: 3,
  due_date: '',
  estimated_duration: 30
})

const statusOptions = [
  { title: 'Pending', value: 'pending' },
  { title: 'In Progress', value: 'in_progress' },
  { title: 'Completed', value: 'completed' }
]

const categoryOptions = [
  'personal', 'work', 'health', 'shopping', 'finance', 'education', 'travel', 'home'
]

const priorityOptions = [
  { title: 'Very Low', value: 1 },
  { title: 'Low', value: 2 },
  { title: 'Medium', value: 3 },
  { title: 'High', value: 4 },
  { title: 'Very High', value: 5 }
]

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

const filteredTasks = computed(() => {
  let filtered = tasksStore.tasks

  if (filters.value.status) {
    filtered = filtered.filter(task => task.status === filters.value.status)
  }

  if (filters.value.category) {
    filtered = filtered.filter(task => task.category === filters.value.category)
  }

  if (filters.value.priority) {
    filtered = filtered.filter(task => task.priority === filters.value.priority)
  }

  if (filters.value.search) {
    const search = filters.value.search.toLowerCase()
    filtered = filtered.filter(task =>
      task.title.toLowerCase().includes(search) ||
      task.description.toLowerCase().includes(search) ||
      task.category.toLowerCase().includes(search)
    )
  }

  return filtered
})

const selectAll = computed({
  get() {
    return filteredTasks.value.length > 0 && selectedTasks.value.length === filteredTasks.value.length
  },
  set(value) {
    if (value) {
      selectedTasks.value = filteredTasks.value.map(task => task.id)
    } else {
      selectedTasks.value = []
    }
  }
})

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

const formatDate = (date) => {
  if (!date) return ''
  return format(new Date(date), 'MMM dd, yyyy HH:mm')
}

const toggleSelectAll = () => {
  if (selectAll.value) {
    selectedTasks.value = filteredTasks.value.map(task => task.id)
  } else {
    selectedTasks.value = []
  }
}

const editTask = (task) => {
  editingTask.value = task
  taskForm.value = {
    title: task.title,
    description: task.description || '',
    category: task.category,
    priority: task.priority,
    due_date: task.due_date ? format(new Date(task.due_date), "yyyy-MM-dd'T'HH:mm") : '',
    estimated_duration: task.estimated_duration || 30
  }
  showCreateDialog.value = true
}

const saveTask = async () => {
  if (!taskForm.value.title) return

  loading.value = true
  try {
    if (editingTask.value) {
      await tasksStore.updateTask(editingTask.value.id, taskForm.value)
    } else {
      await tasksStore.createTask(taskForm.value)
    }
    
    showCreateDialog.value = false
    editingTask.value = null
    taskForm.value = {
      title: '',
      description: '',
      category: 'personal',
      priority: 3,
      due_date: '',
      estimated_duration: 30
    }
  } catch (error) {
    console.error('Error saving task:', error)
  } finally {
    loading.value = false
  }
}

const toggleTaskStatus = async (task) => {
  const newStatus = task.status === 'completed' ? 'pending' : 'completed'
  await tasksStore.updateTask(task.id, { status: newStatus })
}

const deleteTask = async (taskId) => {
  if (confirm('Are you sure you want to delete this task?')) {
    await tasksStore.deleteTask(taskId)
  }
}

const bulkDelete = async () => {
  if (confirm(`Are you sure you want to delete ${selectedTasks.value.length} tasks?`)) {
    await tasksStore.bulkDeleteTasks(selectedTasks.value)
    selectedTasks.value = []
  }
}

onMounted(() => {
  tasksStore.fetchTasks()
})

watch(filters, () => {
  selectedTasks.value = []
}, { deep: true })
</script>

<style scoped>
.overdue {
  background-color: rgba(244, 67, 54, 0.1);
}
</style> 