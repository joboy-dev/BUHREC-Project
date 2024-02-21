from django.db import models
from django.contrib.auth import get_user_model
from uuid import uuid4
from django_ckeditor_5.fields import CKEditor5Field

from user.models import CustomUser

User = get_user_model()

# Create your models here.
class Project(models.Model):
    '''Project model'''
    
    id = models.UUIDField(default=uuid4, primary_key=True)
    title = models.CharField(unique=True, max_length=1000, null=False)
    introduction = CKEditor5Field(default='', null=False, max_length=5000)
    background = CKEditor5Field(default='', null=False, max_length=5000)
    scope_and_limitation = CKEditor5Field(default='', null=False, max_length=3000)
    justification = CKEditor5Field(default='', null=False, max_length=3000)
    objectives = CKEditor5Field(default='', null=False, max_length=3500)
    hypothesis = CKEditor5Field(default='', null=True, max_length=2000)
    literature_review = CKEditor5Field(default='', null=False, max_length=10000)
    materials_and_methods = CKEditor5Field(default='', null=False, max_length=13000)
    procedure = CKEditor5Field(default='', null=False, max_length=5000)
    
    approved = models.BooleanField(default=False)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    
    
class Reviewer(models.Model):
    '''Reviewer model'''
    
    id = models.UUIDField(default=uuid4, primary_key=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    country_domicile = models.CharField(max_length=72, null=False)
    institution_name = models.CharField(max_length=72, null=False)
    years_of_reviewing = models.IntegerField(null=False, default=0)
    
    # Use project for the assignments
    assignments = models.ManyToManyField(Project, related_name='projects', blank=True)
    pending_assignments = models.IntegerField(null=False, default=0)
    completed_assignments = models.IntegerField(null=False, default=0)
    due_assignments = models.IntegerField(null=False, default=0)
    overdue_assignments = models.IntegerField(null=False, default=0)
    withdrawn_assignments = models.IntegerField(null=False, default=0)

