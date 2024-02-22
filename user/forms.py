from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
import re

from project.models import Reviewer
from user.countries import get_all_countries

from .models import StudentOrResearcher

User = get_user_model()

def is_valid_password(password):
    '''Function to check if password is valid'''
    
    # Regular expression for a valid password
    # Password must contain at least 8 characters, including one uppercase letter, one lowercase letter, one digit, and one special character.
    password_regex = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
    
    if re.match(password_regex, password):
        return True
    else:
        return False

class UserChangeForm(UserChangeForm):
    class Meta:
        fields = ["email",]

class UserCreationForm(UserCreationForm):
    class Meta:
        fields = ["email",]
        

# Custom forms
class SignUpForm(forms.Form):
    '''Sign up form'''
    
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
    
    first_name = forms.CharField(max_length=200, required=True, widget=forms.TextInput(attrs={'placeholder': 'First name', 'class': 'input-field'}))
    last_name = forms.CharField(max_length=200, required=True, widget=forms.TextInput(attrs={'placeholder': 'Last name', 'class': 'input-field'}))
    email = forms.EmailField(max_length=200, required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'input-field'}))
    password = forms.CharField(max_length=200, min_length=8, required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'input-field'}))
    confirm_password = forms.CharField(max_length=200, min_length=8, required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password', 'class': 'input-field'}))
    role = forms.CharField(max_length=200, required=True, widget=forms.Select(choices=roles))
    
    
    def clean(self):
        cleaned_data = super().clean()  # Call parent's clean method first

        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('confirm_password')
        
        # Password checks
        if password != password2:
            raise forms.ValidationError('Passwords do not match!')

        if not is_valid_password(password):
            raise forms.ValidationError('Password should have uppercase, lowercase, special character and should have at least 8 characters')
        
        # Email uniqueness
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already exists!')
        
        return cleaned_data


class LoginForm(forms.Form):
    '''Login form'''
    
    email = forms.EmailField(max_length=200, required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'input-field'}))
    password = forms.CharField(max_length=200, min_length=8, required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'input-field'}))


class StudentResearcherForm(forms.ModelForm):
    '''Form to set up student and researcher profile'''
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["pg_degree"].required = False
    
    class Meta:
        model = StudentOrResearcher
        fields = '__all__'
        exclude = ['id', 'user']
        
    def clean(self):
        cleaned_data = super().clean()  # Call parent's clean method first

        degree = cleaned_data.get('degree')
        pg_degree = cleaned_data.get('pg_degree')
        
        if degree == 'pg' and pg_degree is None:
            raise forms.ValidationError('Select a postgraduate degree')
        
        return cleaned_data
    
    
class ReviewerForm(forms.ModelForm):
    '''Form to set up reviewer profile'''
    
    country_domicile = forms.CharField(max_length=200, required=True, widget=forms.Select(choices=get_all_countries()))
    institution_name = forms.CharField(max_length=200, required=True, widget=forms.TextInput(attrs={'placeholder': 'Institution name', 'class': 'input-field'}))
    years_of_reviewing = forms.CharField(max_length=200, required=True, widget=forms.NumberInput(attrs={'placeholder': 'Years of reviewing', 'class': 'input-field'}))
    
    class Meta:
        model = Reviewer
        fields = ['country_domicile', 'institution_name', 'years_of_reviewing']
    