from django.contrib.auth.models import AbstractUser
from django.db import models
from mongoengine import Document, StringField, EmailField, DateTimeField, BooleanField, ListField, ReferenceField
from datetime import datetime


class User(Document):
    """User model for MongoDB using MongoEngine"""
    username = StringField(required=True, unique=True, max_length=150)
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)
    first_name = StringField(max_length=30, blank=True)
    last_name = StringField(max_length=30, blank=True)
    is_active = BooleanField(default=True)
    is_staff = BooleanField(default=False)
    is_superuser = BooleanField(default=False)
    date_joined = DateTimeField(default=datetime.utcnow)
    last_login = DateTimeField()
    
    meta = {
        'collection': 'users',
        'indexes': [
            'username',
            'email',
        ]
    }
    
    def __str__(self):
        return self.username
    
    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_anonymous(self):
        return False 