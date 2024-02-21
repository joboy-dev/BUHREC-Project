from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
import re

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
    
