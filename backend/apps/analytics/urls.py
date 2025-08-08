from django.urls import path
from .views import productivity_metrics, usage_patterns, ai_insights

urlpatterns = [
    path('productivity/', productivity_metrics, name='productivity-metrics'),
    path('patterns/', usage_patterns, name='usage-patterns'),
    path('insights/', ai_insights, name='ai-insights'),
] 