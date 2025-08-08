from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .services import AIService
from apps.tasks.models import Task


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def categorize_task(request):
    """Categorize a task using AI"""
    title = request.data.get('title', '')
    description = request.data.get('description', '')
    
    if not title:
        return Response({'error': 'Title is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    ai_service = AIService()
    result = ai_service.categorize_task(title, description)
    
    return Response(result)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def suggest_priority(request):
    """Suggest priority for a task using AI"""
    title = request.data.get('title', '')
    description = request.data.get('description', '')
    due_date = request.data.get('due_date')
    
    if not title:
        return Response({'error': 'Title is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    ai_service = AIService()
    result = ai_service.suggest_priority(title, description, due_date)
    
    return Response(result)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def parse_natural_language(request):
    """Parse natural language input to extract task details"""
    text = request.data.get('text', '')
    
    if not text:
        return Response({'error': 'Text is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    ai_service = AIService()
    result = ai_service.parse_natural_language(text)
    
    return Response(result)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_suggestions(request):
    """Get AI-powered task suggestions"""
    # Get user's recent tasks
    user_tasks = Task.objects.filter(user=request.user).order_by('-created_at')[:50]
    
    # Convert to list of dictionaries
    tasks_data = []
    for task in user_tasks:
        tasks_data.append({
            'title': task.title,
            'description': task.description,
            'category': task.category,
            'priority': task.priority,
            'status': task.status,
            'estimated_duration': task.estimated_duration,
            'due_date': task.due_date,
        })
    
    ai_service = AIService()
    suggestions = ai_service.get_task_suggestions(tasks_data)
    
    return Response({'suggestions': suggestions})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def optimize_schedule(request):
    """Optimize task schedule"""
    task_ids = request.data.get('task_ids', [])
    
    if not task_ids:
        return Response({'error': 'task_ids is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Get tasks
    tasks = Task.objects.filter(user=request.user, id__in=task_ids)
    
    # Convert to list of dictionaries
    tasks_data = []
    for task in tasks:
        tasks_data.append({
            'id': str(task.id),
            'title': task.title,
            'description': task.description,
            'category': task.category,
            'priority': task.priority,
            'status': task.status,
            'estimated_duration': task.estimated_duration,
            'due_date': task.due_date,
        })
    
    ai_service = AIService()
    optimized_schedule = ai_service.optimize_schedule(tasks_data)
    
    return Response({'optimized_schedule': optimized_schedule})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def estimate_duration(request):
    """Estimate task duration"""
    title = request.data.get('title', '')
    description = request.data.get('description', '')
    
    if not title:
        return Response({'error': 'Title is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    ai_service = AIService()
    duration = ai_service.estimate_duration(title, description)
    
    return Response({'estimated_duration': duration}) 