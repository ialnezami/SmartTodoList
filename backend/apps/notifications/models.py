from mongoengine import Document, StringField, DateTimeField, BooleanField, ReferenceField
from datetime import datetime
from apps.authentication.models import User


class Notification(Document):
    """Notification model for MongoDB using MongoEngine"""
    user = ReferenceField(User, required=True)
    title = StringField(required=True, max_length=200)
    message = StringField(max_length=1000)
    type = StringField(choices=['task_due', 'task_overdue', 'reminder', 'system'], default='reminder')
    is_read = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.utcnow)
    read_at = DateTimeField()
    
    meta = {
        'collection': 'notifications',
        'indexes': [
            'user',
            'type',
            'is_read',
            ('user', 'is_read'),
            ('user', 'created_at'),
        ],
        'ordering': ['-created_at']
    }
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"
    
    def mark_as_read(self):
        self.is_read = True
        self.read_at = datetime.utcnow()
        self.save() 