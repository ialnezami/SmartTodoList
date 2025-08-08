from rest_framework import serializers
from .models import Task
from apps.authentication.models import User


class TaskSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    title = serializers.CharField(max_length=200)
    description = serializers.CharField(max_length=1000, required=False, allow_blank=True)
    category = serializers.CharField(max_length=50, required=False, default='personal')
    priority = serializers.IntegerField(min_value=1, max_value=5, required=False, default=3)
    status = serializers.ChoiceField(choices=['pending', 'in_progress', 'completed'], required=False, default='pending')
    due_date = serializers.DateTimeField(required=False, allow_null=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    user = serializers.CharField(read_only=True)
    
    # AI-related fields
    ai_metadata = serializers.DictField(required=False, default=dict)
    confidence_score = serializers.IntegerField(min_value=0, max_value=100, required=False, default=0)
    suggested_category = serializers.CharField(max_length=50, required=False, allow_blank=True)
    estimated_duration = serializers.IntegerField(min_value=1, required=False, default=30)
    complexity_score = serializers.IntegerField(min_value=1, max_value=10, required=False, default=5)
    
    # Additional fields
    tags = serializers.ListField(child=serializers.CharField(max_length=50), required=False, default=list)
    dependencies = serializers.ListField(child=serializers.CharField(), required=False, default=list)
    attachments = serializers.ListField(child=serializers.CharField(), required=False, default=list)
    is_recurring = serializers.BooleanField(required=False, default=False)
    recurrence_pattern = serializers.CharField(max_length=100, required=False, allow_blank=True)
    
    def create(self, validated_data):
        user = self.context['request'].user
        task = Task(
            user=user,
            **validated_data
        )
        task.save()
        return task
    
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class TaskListSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    title = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    category = serializers.CharField(read_only=True)
    priority = serializers.IntegerField(read_only=True)
    status = serializers.CharField(read_only=True)
    due_date = serializers.DateTimeField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    is_overdue = serializers.BooleanField(read_only=True)
    days_until_due = serializers.IntegerField(read_only=True)
    tags = serializers.ListField(read_only=True)
    estimated_duration = serializers.IntegerField(read_only=True)
    complexity_score = serializers.IntegerField(read_only=True)


class BulkTaskSerializer(serializers.Serializer):
    tasks = TaskSerializer(many=True)
    
    def create(self, validated_data):
        user = self.context['request'].user
        tasks_data = validated_data['tasks']
        created_tasks = []
        
        for task_data in tasks_data:
            task = Task(user=user, **task_data)
            task.save()
            created_tasks.append(task)
        
        return {'tasks': created_tasks} 