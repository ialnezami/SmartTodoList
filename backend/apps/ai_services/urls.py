from django.urls import path
from .views import (
    categorize_task, suggest_priority, parse_natural_language,
    get_suggestions, optimize_schedule, estimate_duration
)

urlpatterns = [
    path('categorize/', categorize_task, name='categorize-task'),
    path('suggest-priority/', suggest_priority, name='suggest-priority'),
    path('parse-natural/', parse_natural_language, name='parse-natural'),
    path('suggestions/', get_suggestions, name='get-suggestions'),
    path('optimize-schedule/', optimize_schedule, name='optimize-schedule'),
    path('estimate-duration/', estimate_duration, name='estimate-duration'),
] 