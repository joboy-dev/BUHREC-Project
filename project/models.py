from datetime import datetime
from django.db import models
from django.contrib.auth import get_user_model
from uuid import uuid4
from django_ckeditor_5.fields import CKEditor5Field

from user.countries import get_all_countries
from user.models import CustomUser, StudentOrResearcher

User = get_user_model()

# Create your models here.
class Project(models.Model):
    '''Project model'''
    
    id = models.UUIDField(default=uuid4, primary_key=True)
    title = models.CharField(max_length=1000, null=False)
    introduction = CKEditor5Field(config_name='extends', default='', null=False, blank=True, max_length=50000)
    background = CKEditor5Field(config_name='extends', default='', null=False, blank=True, max_length=50000)
    scope_and_limitation = CKEditor5Field(config_name='extends', default='', null=False, blank=True, max_length=50000)
    justification = CKEditor5Field(config_name='extends', default='', null=False, blank=True, max_length=50000)
    objectives = CKEditor5Field(config_name='extends', default='', null=False, blank=True, max_length=35000)
    hypothesis = CKEditor5Field(config_name='extends', default='', null=True, blank=True, max_length=20000)
    literature_review = CKEditor5Field(config_name='extends', default='', null=False, blank=True, max_length=100000)
    materials_and_methods = CKEditor5Field(config_name='extends', default='', null=False, blank=True, max_length=150000)
    procedure = CKEditor5Field(config_name='extends', default='', null=False, blank=True, max_length=50000)
    
    approved = models.BooleanField(default=False)
    payment_approved = models.BooleanField(default=False)
    track_id = models.UUIDField(null=True, unique=True)
    
    owner = models.ForeignKey(StudentOrResearcher, on_delete=models.CASCADE, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.title} by {self.owner.user.last_name}, {self.owner.user.first_name}'
    

class Reviewer(models.Model):
    '''Reviewer model'''

    id = models.UUIDField(default=uuid4, primary_key=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    country_domicile = models.CharField(max_length=72, null=False, choices=get_all_countries(), default='NG')
    institution_name = models.CharField(max_length=72, null=False)
    years_of_reviewing = models.IntegerField(null=False, default=0)
    pending_assignments_no = models.IntegerField(null=False, default=0)
    completed_assignments_no = models.IntegerField(null=False, default=0)
    due_assignments_no = models.IntegerField(null=False, default=0)
    overdue_assignments_no = models.IntegerField(null=False, default=0)
    withdrawn_assignments_no = models.IntegerField(null=False, default=0)
    
    def __str__(self):
        return self.user.email
    

class Assignment(models.Model):
    '''Assignment model'''
    
    id = models.UUIDField(default=uuid4, primary_key=True)
    is_complete = models.BooleanField(default=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    reviewer = models.ForeignKey(Reviewer, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return f'Assignment for {self.project.title}'
    
    
class Remark(models.Model):
    '''Remark model'''
    
    id = models.UUIDField(default=uuid4, primary_key=True)
    message = models.TextField(max_length=1000, null=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    reviewer = models.ForeignKey(Reviewer, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'Remark for {self.project.title} from {self.reviewer.user.last_name}'
    
    class Meta:
        ordering = ['-created_at']
