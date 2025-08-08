from django.urls import path
from .views import (
    TaskListView, TaskDetailView, bulk_create_tasks, 
    bulk_update_tasks, bulk_delete_tasks, task_statistics
)

urlpatterns = [
    path('', TaskListView.as_view(), name='task-list'),
    path('<str:id>/', TaskDetailView.as_view(), name='task-detail'),
    path('bulk-create/', bulk_create_tasks, name='bulk-create-tasks'),
    path('bulk-update/', bulk_update_tasks, name='bulk-update-tasks'),
    path('bulk-delete/', bulk_delete_tasks, name='bulk-delete-tasks'),
    path('statistics/', task_statistics, name='task-statistics'),
] 