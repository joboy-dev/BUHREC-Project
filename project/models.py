from django.db import models
from django.contrib.auth import get_user_model
from uuid import uuid4
from django_ckeditor_5.fields import CKEditor5Field

from user.countries import get_all_countries
from user.models import CustomUser

User = get_user_model()

# Create your models here.
class Project(models.Model):
    '''Project model'''
    
    id = models.UUIDField(default=uuid4, primary_key=True)
    title = models.CharField(unique=True, max_length=1000, null=False)
    introduction = CKEditor5Field(default='', null=False, blank=True, max_length=5000)
    background = CKEditor5Field(default='', null=False, blank=True, max_length=5000)
    scope_and_limitation = CKEditor5Field(default='', null=False, blank=True, max_length=3000)
    justification = CKEditor5Field(default='', null=False, blank=True, max_length=3000)
    objectives = CKEditor5Field(default='', null=False, blank=True, max_length=3500)
    hypothesis = CKEditor5Field(default='', null=True, blank=True, max_length=2000)
    literature_review = CKEditor5Field(default='', null=False, blank=True, max_length=10000)
    materials_and_methods = CKEditor5Field(default='', null=False, blank=True, max_length=13000)
    procedure = CKEditor5Field(default='', null=False, blank=True, max_length=5000)
    
    approved = models.BooleanField(default=False)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.title} by {self.owner.last_name}, {self.owner.first_name}'
    
    
class Reviewer(models.Model):
    '''Reviewer model'''

    id = models.UUIDField(default=uuid4, primary_key=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    country_domicile = models.CharField(max_length=72, null=False, choices=get_all_countries(), default='NG')
    institution_name = models.CharField(max_length=72, null=False)
    years_of_reviewing = models.IntegerField(null=False, default=0)
    
    # Use project for the assignments
    assignments = models.ManyToManyField(Project, related_name='projects', blank=True)
    completed_assignments = models.ManyToManyField(Project, related_name='completed', blank=True) 
    
    pending_assignments_no = models.IntegerField(null=False, default=0)
    completed_assignments_no = models.IntegerField(null=False, default=0)
    due_assignments_no = models.IntegerField(null=False, default=0)
    overdue_assignments_no = models.IntegerField(null=False, default=0)
    withdrawn_assignments_no = models.IntegerField(null=False, default=0)
    