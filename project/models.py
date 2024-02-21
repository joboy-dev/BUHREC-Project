from django.db import models
from django.contrib.auth import get_user_model
from uuid import uuid4

User = get_user_model()

# Create your models here.
class Project(models.Model):
    '''Project model'''
    
    id = models.UUIDField(default=uuid4, primary_key=True)
    title = models.CharField(unique=True, max_length=25, null=False)
    
    
