from .base import *

# Development-specific settings
DEBUG = True

# Allow all hosts in development
ALLOWED_HOSTS = ['*']

# CORS settings for development
CORS_ALLOW_ALL_ORIGINS = True

# Logging for development
LOGGING['root']['level'] = 'DEBUG'

# Email backend for development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Static files serving in development
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage' 