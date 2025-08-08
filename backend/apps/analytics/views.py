from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.tasks.models import Task
from datetime import datetime, timedelta


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def productivity_metrics(request):
    """Get productivity metrics for the user"""
    user_tasks = Task.objects.filter(user=request.user)
    
    # Calculate metrics
    total_tasks = user_tasks.count()
    completed_tasks = user_tasks.filter(status='completed').count()
    pending_tasks = user_tasks.filter(status='pending').count()
    in_progress_tasks = user_tasks.filter(status='in_progress').count()
    
    # Completion rate
    completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
    
    # Average completion time
    completed_tasks_with_duration = user_tasks.filter(status='completed', estimated_duration__gt=0)
    avg_completion_time = 0
    if completed_tasks_with_duration.count() > 0:
        total_duration = sum(task.estimated_duration for task in completed_tasks_with_duration)
        avg_completion_time = total_duration / completed_tasks_with_duration.count()
    
    # Tasks by priority
    priority_breakdown = {}
    for priority in range(1, 6):
        priority_breakdown[f'priority_{priority}'] = user_tasks.filter(priority=priority).count()
    
    # Tasks by category
    category_breakdown = {}
    for task in user_tasks:
        category = task.category or 'uncategorized'
        if category not in category_breakdown:
            category_breakdown[category] = 0
        category_breakdown[category] += 1
    
    return Response({
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'in_progress_tasks': in_progress_tasks,
        'completion_rate': round(completion_rate, 2),
        'avg_completion_time': round(avg_completion_time, 2),
        'priority_breakdown': priority_breakdown,
        'category_breakdown': category_breakdown,
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def usage_patterns(request):
    """Get usage patterns for the user"""
    user_tasks = Task.objects.filter(user=request.user)
    
    # Tasks created by day of week
    day_of_week_pattern = {}
    for task in user_tasks:
        day = task.created_at.strftime('%A')
        if day not in day_of_week_pattern:
            day_of_week_pattern[day] = 0
        day_of_week_pattern[day] += 1
    
    # Tasks completed by hour of day
    hour_of_day_pattern = {}
    completed_tasks = user_tasks.filter(status='completed')
    for task in completed_tasks:
        hour = task.updated_at.hour
        if hour not in hour_of_day_pattern:
            hour_of_day_pattern[hour] = 0
        hour_of_day_pattern[hour] += 1
    
    # Most productive hours
    most_productive_hours = sorted(hour_of_day_pattern.items(), key=lambda x: x[1], reverse=True)[:3]
    
    return Response({
        'day_of_week_pattern': day_of_week_pattern,
        'hour_of_day_pattern': hour_of_day_pattern,
        'most_productive_hours': most_productive_hours,
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ai_insights(request):
    """Get AI-generated insights"""
    user_tasks = Task.objects.filter(user=request.user)
    
    insights = []
    
    # Analyze completion patterns
    completed_tasks = user_tasks.filter(status='completed')
    if completed_tasks.count() > 0:
        avg_priority = sum(task.priority for task in completed_tasks) / completed_tasks.count()
        if avg_priority > 4:
            insights.append("You tend to complete high-priority tasks effectively. Consider focusing on medium-priority tasks to improve overall productivity.")
        elif avg_priority < 2:
            insights.append("You often complete low-priority tasks. Try to prioritize important tasks to maximize your productivity.")
    
    # Analyze overdue tasks
    overdue_tasks = [task for task in user_tasks if task.is_overdue]
    if overdue_tasks:
        insights.append(f"You have {len(overdue_tasks)} overdue tasks. Consider reviewing and reprioritizing them.")
    
    # Analyze category distribution
    categories = {}
    for task in user_tasks:
        category = task.category or 'uncategorized'
        if category not in categories:
            categories[category] = 0
        categories[category] += 1
    
    if categories:
        most_common_category = max(categories.items(), key=lambda x: x[1])[0]
        insights.append(f"Your most common task category is '{most_common_category}'. Consider diversifying your task types for better work-life balance.")
    
    # Analyze task duration
    tasks_with_duration = user_tasks.filter(estimated_duration__gt=0)
    if tasks_with_duration.count() > 0:
        avg_duration = sum(task.estimated_duration for task in tasks_with_duration) / tasks_with_duration.count()
        if avg_duration > 120:
            insights.append("Your tasks tend to be long-duration. Consider breaking them down into smaller, more manageable tasks.")
        elif avg_duration < 30:
            insights.append("Your tasks are typically short. Consider batching similar tasks together for better efficiency.")
    
    return Response({
        'insights': insights,
        'total_insights': len(insights),
    }) 