import os

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy
from uuid import uuid4

from .manager import CustomUserManager

# Create your models here.
class CustomUser(AbstractBaseUser, PermissionsMixin):
    '''Custom user model'''
    
    def upload_image(model, filename):
        '''Function to upload image and save in a folder for each object'''
        extension = filename.split('.')[-1]
        return os.path.join('user', str(model.id), f'user_pic.{extension}')
    
    # Roles
    STUDENT = 'student'
    RESEARCHER = 'researcher'
    REVIEWER = 'reviewer'
    ADMIN = 'admin'
    
    roles = [
        (STUDENT, 'Student'),
        (RESEARCHER, 'Researcher'),
        (REVIEWER, 'Reviewer'),
        (ADMIN, 'Admin'),
    ]

    id = models.UUIDField(default=uuid4, primary_key=True)
    email = models.EmailField(gettext_lazy('email address'), unique=True, null=False)
    first_name = models.CharField(max_length=128, null=False)
    last_name = models.CharField(max_length=128, null=False)
    profile_pic = models.ImageField(default='user/default.png', upload_to=upload_image, null=True)
    role = models.CharField(choices=roles, default=STUDENT, null=False, max_length=10)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    

class StudentOrResearcher(models.Model):
    '''Student/Researcher model'''
    
    # Degrees
    UG = 'undergraduate'
    PG = 'postgraduate'
    IND = 'independent'
    
    degrees = [
        (UG, 'Undergraduate'),
        (PG, 'Postgraduate'),
        (IND, 'Independent'),
    ]
    
    # PG Degrees
    PHD = 'phd'
    PGD = 'pgd'
    MSC = 'msc'
    
    pg_degrees = [
        (PHD, 'PhD'),
        (MSC, 'MSc'),
        (PGD, 'PGD'),
    ]
    
    # Programmes
    CS = 'computer science'
    ES = 'environmental science'
    SCI = 'science'
    HEA = 'health'
    MGMT = 'mamagement'
    HUM = 'humanities'
    
    programmes = [
        (CS, 'Computer Science'),
        (ES, 'Environmental Science'),
        (SCI, 'Science'),
        (HEA, 'Health'),
        (MGMT, 'Management'),   
        (HUM, 'Humanities'),
    ]
    
    id = models.UUIDField(default=uuid4, primary_key=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    degree = models.CharField(choices=degrees, default=UG, null=False, max_length=13)
    pg_degree = models.CharField(choices=pg_degrees, null=True, max_length=3)
    programme = models.CharField(choices=programmes, default=SCI, null=False, max_length=30)
    
    def __str__(self):
        return self.user.email
    

class Admin(models.Model):
    '''Admin model'''
    
    # Roles
    CHAIR = 'chair'
    ASST_CHAIR = 'asst chair'
    STAFF = 'staff'
    
    roles = [
        (CHAIR, 'Chair'),
        (ASST_CHAIR, 'Assistant chair'),
        (STAFF, 'Staff'),
    ]
    
    id = models.UUIDField(default=uuid4, primary_key=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    role = models.CharField(choices=roles, default=STAFF, null=False, max_length=10)
    