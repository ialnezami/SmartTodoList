<template>
  <div>
    <v-row>
      <v-col cols="12">
        <h1 class="text-h4 mb-4">Analytics</h1>
      </v-col>
    </v-row>

    <!-- Productivity Metrics -->
    <v-row>
      <v-col cols="12" sm="6" md="3">
        <v-card>
          <v-card-text>
            <div class="text-h6">Completion Rate</div>
            <div class="text-h4 text-success">{{ productivityMetrics.completion_rate || 0 }}%</div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" md="3">
        <v-card>
          <v-card-text>
            <div class="text-h6">Avg Completion Time</div>
            <div class="text-h4 text-info">{{ productivityMetrics.avg_completion_time || 0 }} min</div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" md="3">
        <v-card>
          <v-card-text>
            <div class="text-h6">Total Tasks</div>
            <div class="text-h4">{{ productivityMetrics.total_tasks || 0 }}</div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" md="3">
        <v-card>
          <v-card-text>
            <div class="text-h6">Overdue Tasks</div>
            <div class="text-h4 text-error">{{ productivityMetrics.overdue_tasks || 0 }}</div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Charts -->
    <v-row>
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title>Tasks by Category</v-card-title>
          <v-card-text>
            <canvas ref="categoryChart" width="400" height="200"></canvas>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="6">
        <v-card>
          <v-card-title>Tasks by Priority</v-card-title>
          <v-card-text>
            <canvas ref="priorityChart" width="400" height="200"></canvas>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Usage Patterns -->
    <v-row>
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title>Tasks by Day of Week</v-card-title>
          <v-card-text>
            <v-list>
              <v-list-item
                v-for="(count, day) in usagePatterns.day_of_week_pattern"
                :key="day"
                :title="day"
                :subtitle="`${count} tasks`"
              >
                <template v-slot:prepend>
                  <v-icon>mdi-calendar</v-icon>
                </template>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="6">
        <v-card>
          <v-card-title>Most Productive Hours</v-card-title>
          <v-card-text>
            <v-list>
              <v-list-item
                v-for="(hour, index) in usagePatterns.most_productive_hours"
                :key="index"
                :title="`${hour[0]}:00`"
                :subtitle="`${hour[1]} tasks completed`"
              >
                <template v-slot:prepend>
                  <v-icon>mdi-clock</v-icon>
                </template>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- AI Insights -->
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title>
            <v-icon color="primary" class="mr-2">mdi-brain</v-icon>
            AI-Generated Insights
          </v-card-title>
          <v-card-text>
            <v-list v-if="aiInsights.length > 0">
              <v-list-item
                v-for="(insight, index) in aiInsights"
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
    </v-row>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import axios from 'axios'
import Chart from 'chart.js/auto'

const productivityMetrics = ref({})
const usagePatterns = ref({
  day_of_week_pattern: {},
  most_productive_hours: []
})
const aiInsights = ref([])

const categoryChart = ref(null)
const priorityChart = ref(null)

const loadAnalytics = async () => {
  try {
    // Load productivity metrics
    const metricsResponse = await axios.get('/api/analytics/productivity/')
    productivityMetrics.value = metricsResponse.data

    // Load usage patterns
    const patternsResponse = await axios.get('/api/analytics/patterns/')
    usagePatterns.value = patternsResponse.data

    // Load AI insights
    const insightsResponse = await axios.get('/api/analytics/insights/')
    aiInsights.value = insightsResponse.data.insights || []

    // Create charts after data is loaded
    await nextTick()
    createCharts()
  } catch (error) {
    console.error('Error loading analytics:', error)
  }
}

const createCharts = () => {
  // Category Chart
  if (categoryChart.value && productivityMetrics.value.category_breakdown) {
    const categoryCtx = categoryChart.value.getContext('2d')
    new Chart(categoryCtx, {
      type: 'doughnut',
      data: {
        labels: Object.keys(productivityMetrics.value.category_breakdown),
        datasets: [{
          data: Object.values(productivityMetrics.value.category_breakdown),
          backgroundColor: [
            '#FF6384',
            '#36A2EB',
            '#FFCE56',
            '#4BC0C0',
            '#9966FF',
            '#FF9F40',
            '#FF6384',
            '#C9CBCF'
          ]
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            position: 'bottom'
          }
        }
      }
    })
  }

  // Priority Chart
  if (priorityChart.value && productivityMetrics.value.priority_breakdown) {
    const priorityCtx = priorityChart.value.getContext('2d')
    new Chart(priorityCtx, {
      type: 'bar',
      data: {
        labels: Object.keys(productivityMetrics.value.priority_breakdown).map(key => `Priority ${key.split('_')[1]}`),
        datasets: [{
          label: 'Number of Tasks',
          data: Object.values(productivityMetrics.value.priority_breakdown),
          backgroundColor: [
            '#4BC0C0',
            '#36A2EB',
            '#FFCE56',
            '#FF9F40',
            '#FF6384'
          ]
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            display: false
          }
        },
        scales: {
          y: {
            beginAtZero: true
          }
        }
      }
    })
  }
}

onMounted(() => {
  loadAnalytics()
})
</script> 