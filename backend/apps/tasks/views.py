from rest_framework import status, generics, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Task
from .serializers import TaskSerializer, TaskListSerializer, BulkTaskSerializer


class TaskListView(generics.ListCreateAPIView):
    """List and create tasks"""
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'category', 'priority']
    search_fields = ['title', 'description', 'tags']
    ordering_fields = ['created_at', 'due_date', 'priority', 'title']
    ordering = ['-created_at']
    
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TaskListSerializer
        return TaskSerializer


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, and delete a task"""
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer
    lookup_field = 'id'
    
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def bulk_create_tasks(request):
    """Bulk create tasks"""
    serializer = BulkTaskSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        result = serializer.save()
        return Response({
            'message': f'{len(result["tasks"])} tasks created successfully',
            'tasks': TaskSerializer(result['tasks'], many=True).data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def bulk_update_tasks(request):
    """Bulk update tasks"""
    task_ids = request.data.get('task_ids', [])
    update_data = request.data.get('update_data', {})
    
    if not task_ids:
        return Response({'error': 'task_ids is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    tasks = Task.objects.filter(user=request.user, id__in=task_ids)
    updated_count = 0
    
    for task in tasks:
        for field, value in update_data.items():
            if hasattr(task, field):
                setattr(task, field, value)
        task.save()
        updated_count += 1
    
    return Response({
        'message': f'{updated_count} tasks updated successfully'
    }, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def bulk_delete_tasks(request):
    """Bulk delete tasks"""
    task_ids = request.data.get('task_ids', [])
    
    if not task_ids:
        return Response({'error': 'task_ids is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    tasks = Task.objects.filter(user=request.user, id__in=task_ids)
    deleted_count = tasks.count()
    tasks.delete()
    
    return Response({
        'message': f'{deleted_count} tasks deleted successfully'
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def task_statistics(request):
    """Get task statistics for the user"""
    user_tasks = Task.objects.filter(user=request.user)
    
    total_tasks = user_tasks.count()
    completed_tasks = user_tasks.filter(status='completed').count()
    pending_tasks = user_tasks.filter(status='pending').count()
    in_progress_tasks = user_tasks.filter(status='in_progress').count()
    overdue_tasks = sum(1 for task in user_tasks if task.is_overdue)
    
    # Category breakdown
    categories = {}
    for task in user_tasks:
        category = task.category or 'uncategorized'
        if category not in categories:
            categories[category] = 0
        categories[category] += 1
    
    # Priority breakdown
    priorities = {}
    for task in user_tasks:
        priority = task.priority
        if priority not in priorities:
            priorities[priority] = 0
        priorities[priority] += 1
    
    return Response({
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'in_progress_tasks': in_progress_tasks,
        'overdue_tasks': overdue_tasks,
        'completion_rate': (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0,
        'categories': categories,
        'priorities': priorities,
    }) 