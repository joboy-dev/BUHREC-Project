from django.db import models
from django.contrib.auth import get_user_model
from uuid import uuid4

User = get_user_model()

# Create your models here.
class Project(models.Model):
    '''Project model'''
    
    id = models.UUIDField(default=uuid4, primary_key=True)
    title = models.CharField(unique=True, max_length=1000, null=False)
    introduction = models.CharField(null=False, max_length=5000)
    background = models.CharField(null=False, max_length=5000)
    scope_and_limitation = models.CharField(null=False, max_length=3000)
    justification = models.CharField(null=False, max_length=3000)
    objectives = models.CharField(null=False, max_length=3500)
    hypothesis = models.CharField(null=True, max_length=2000)
    literature_review = models.CharField(null=True, max_length=10000)
    materials_and_methods = models.CharField(null=True, max_length=13000)
    procedure = models.CharField(null=True, max_length=5000)
