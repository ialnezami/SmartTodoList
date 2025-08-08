<template>
  <div>
    <v-row>
      <v-col cols="12">
        <h1 class="text-h4 mb-4">AI Insights</h1>
      </v-col>
    </v-row>

    <!-- AI Insights Cards -->
    <v-row>
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title>
            <v-icon color="primary" class="mr-2">mdi-brain</v-icon>
            AI-Generated Insights
          </v-card-title>
          <v-card-text>
            <v-list v-if="insights.length > 0">
              <v-list-item
                v-for="(insight, index) in insights"
                :key="index"
                :title="insight"
              >
                <template v-slot:prepend>
                  <v-icon color="primary">mdi-lightbulb</v-icon>
                </template>
              </v-list-item>
            </v-list>
            <v-alert v-else type="info">
              No insights available yet. Complete more tasks to get personalized insights!
            </v-alert>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="6">
        <v-card>
          <v-card-title>
            <v-icon color="secondary" class="mr-2">mdi-lightbulb</v-icon>
            Task Suggestions
          </v-card-title>
          <v-card-text>
            <v-list v-if="suggestions.length > 0">
              <v-list-item
                v-for="suggestion in suggestions"
                :key="suggestion.title"
                :title="suggestion.title"
                :subtitle="suggestion.category"
              >
                <template v-slot:prepend>
                  <v-icon color="secondary">mdi-plus-circle</v-icon>
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
              No suggestions available yet.
            </v-alert>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- AI Tools -->
    <v-row class="mt-4">
      <v-col cols="12">
        <v-card>
          <v-card-title>AI Tools</v-card-title>
          <v-card-text>
            <v-row>
              <v-col cols="12" md="6">
                <v-card outlined>
                  <v-card-title>Natural Language Task Creation</v-card-title>
                  <v-card-text>
                    <v-textarea
                      v-model="naturalLanguageInput"
                      label="Describe your task in natural language"
                      placeholder="e.g., Buy groceries tomorrow at 2pm"
                      rows="3"
                    />
                    <v-btn
                      color="primary"
                      @click="parseNaturalLanguage"
                      :loading="loading"
                      block
                    >
                      Parse & Create Task
                    </v-btn>
                  </v-card-text>
                </v-card>
              </v-col>

              <v-col cols="12" md="6">
                <v-card outlined>
                  <v-card-title>Task Categorization</v-card-title>
                  <v-card-text>
                    <v-text-field
                      v-model="categorizationInput.title"
                      label="Task Title"
                    />
                    <v-textarea
                      v-model="categorizationInput.description"
                      label="Description (optional)"
                      rows="2"
                    />
                    <v-btn
                      color="secondary"
                      @click="categorizeTask"
                      :loading="loading"
                      block
                    >
                      Categorize Task
                    </v-btn>
                    <v-alert
                      v-if="categorizationResult"
                      :type="categorizationResult.category ? 'success' : 'error'"
                      class="mt-2"
                    >
                      Suggested Category: {{ categorizationResult.category || 'Error' }}
                      <br>
                      Confidence: {{ categorizationResult.confidence_score }}%
                    </v-alert>
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Priority Suggestions -->
    <v-row class="mt-4">
      <v-col cols="12">
        <v-card>
          <v-card-title>Priority Suggestions</v-card-title>
          <v-card-text>
            <v-row>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="priorityInput.title"
                  label="Task Title"
                />
              </v-col>
              <v-col cols="12" md="6">
                <v-textarea
                  v-model="priorityInput.description"
                  label="Description (optional)"
                  rows="2"
                />
              </v-col>
            </v-row>
            <v-btn
              color="info"
              @click="suggestPriority"
              :loading="loading"
            >
              Get Priority Suggestion
            </v-btn>
            <v-alert
              v-if="priorityResult"
              :type="priorityResult.priority ? 'success' : 'error'"
              class="mt-2"
            >
              Suggested Priority: {{ priorityResult.priority || 'Error' }}
              <br>
              Reasoning: {{ priorityResult.reasoning || 'N/A' }}
            </v-alert>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useTasksStore } from '@/stores/tasks'
import axios from 'axios'

const tasksStore = useTasksStore()

const loading = ref(false)
const insights = ref([])
const suggestions = ref([])
const naturalLanguageInput = ref('')
const categorizationInput = ref({
  title: '',
  description: ''
})
const categorizationResult = ref(null)
const priorityInput = ref({
  title: '',
  description: ''
})
const priorityResult = ref(null)

const loadInsights = async () => {
  loading.value = true
  try {
    // Load AI insights
    const insightsResponse = await axios.get('/api/analytics/insights/')
    insights.value = insightsResponse.data.insights || []

    // Load AI suggestions
    const suggestionsResponse = await axios.get('/api/ai/suggestions/')
    suggestions.value = suggestionsResponse.data.suggestions || []
  } catch (error) {
    console.error('Error loading insights:', error)
  } finally {
    loading.value = false
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
      naturalLanguageInput.value = ''
      // Show success message
    }
  } catch (error) {
    console.error('Error parsing natural language:', error)
  } finally {
    loading.value = false
  }
}

const categorizeTask = async () => {
  if (!categorizationInput.value.title) return

  loading.value = true
  try {
    const response = await axios.post('/api/ai/categorize/', {
      title: categorizationInput.value.title,
      description: categorizationInput.value.description
    })
    
    categorizationResult.value = response.data
  } catch (error) {
    console.error('Error categorizing task:', error)
    categorizationResult.value = { error: 'Failed to categorize task' }
  } finally {
    loading.value = false
  }
}

const suggestPriority = async () => {
  if (!priorityInput.value.title) return

  loading.value = true
  try {
    const response = await axios.post('/api/ai/suggest-priority/', {
      title: priorityInput.value.title,
      description: priorityInput.value.description
    })
    
    priorityResult.value = response.data
  } catch (error) {
    console.error('Error suggesting priority:', error)
    priorityResult.value = { error: 'Failed to suggest priority' }
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
    // Remove the suggestion from the list
    const index = suggestions.value.findIndex(s => s.title === suggestion.title)
    if (index !== -1) {
      suggestions.value.splice(index, 1)
    }
  }
}

onMounted(() => {
  loadInsights()
})
</script> 