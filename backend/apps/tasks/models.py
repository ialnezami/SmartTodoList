from mongoengine import Document, StringField, DateTimeField, IntField, ListField, ReferenceField, BooleanField, DictField
from datetime import datetime
from apps.authentication.models import User


class Task(Document):
    """Task model for MongoDB using MongoEngine"""
    title = StringField(required=True, max_length=200)
    description = StringField(max_length=1000)
    category = StringField(max_length=50, default='personal')
    priority = IntField(min_value=1, max_value=5, default=3)
    status = StringField(choices=['pending', 'in_progress', 'completed'], default='pending')
    due_date = DateTimeField()
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    user = ReferenceField(User, required=True)
    
    # AI-related fields
    ai_metadata = DictField(default={})
    confidence_score = IntField(min_value=0, max_value=100, default=0)
    suggested_category = StringField(max_length=50)
    estimated_duration = IntField(min_value=1, default=30)  # in minutes
    complexity_score = IntField(min_value=1, max_value=10, default=5)
    
    # Additional fields
    tags = ListField(StringField(max_length=50), default=[])
    dependencies = ListField(ReferenceField('self'), default=[])
    attachments = ListField(StringField(), default=[])
    is_recurring = BooleanField(default=False)
    recurrence_pattern = StringField(max_length=100)  # e.g., "daily", "weekly", "monthly"
    
    meta = {
        'collection': 'tasks',
        'indexes': [
            'user',
            'status',
            'category',
            'due_date',
            ('user', 'status'),
            ('user', 'category'),
            ('user', 'due_date'),
        ],
        'ordering': ['-created_at']
    }
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.updated_at = datetime.utcnow()
        return super().save(*args, **kwargs)
    
    @property
    def is_overdue(self):
        if self.due_date and self.status != 'completed':
            return datetime.utcnow() > self.due_date
        return False
    
    @property
    def days_until_due(self):
        if self.due_date:
            delta = self.due_date - datetime.utcnow()
            return delta.days
        return None 