from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
import re

from project.models import Reviewer
from user.countries import get_all_countries

from .models import StudentOrResearcher, Admin

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
    
# For reusablility
def form_text_field(field, widget, placeholder):
    '''Form text field '''
    
    return field(max_length=200, required=True, widget=widget(attrs={'placeholder': placeholder}))

def form_select_field(choices):
    '''Form select field '''
    
    return forms.CharField(max_length=200, required=True, widget=forms.Select(choices=choices))


############################################################################
############################################################################

class UserChangeForm(UserChangeForm):
    class Meta:
        fields = ["email",]

class UserCreationForm(UserCreationForm):
    class Meta:
        fields = ["email",]
        

############################################################################
############################################################################
############################################################################

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
    
    first_name = form_text_field(forms.CharField, forms.TextInput, 'First name')
    last_name = form_text_field(forms.CharField, forms.TextInput, 'Last name')
    email = form_text_field(forms.EmailField, forms.EmailInput, 'Email')
    password = form_text_field(forms.CharField, forms.PasswordInput, 'Password')
    confirm_password = form_text_field(forms.CharField, forms.PasswordInput, 'Confirm Password')
    role = form_select_field(roles)
    
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
    
    email = form_text_field(forms.EmailField, forms.EmailInput, 'Email')
    password = form_text_field(forms.CharField, forms.PasswordInput, 'Password')


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
    
    country_domicile = form_select_field(get_all_countries())    
    institution_name = form_text_field(forms.CharField, forms.TextInput, 'Institution name')
    years_of_reviewing = form_text_field(forms.CharField, forms.NumberInput, 'Years of reviewing')
    
    class Meta:
        model = Reviewer
        fields = ['country_domicile', 'institution_name', 'years_of_reviewing']
    
    
class AdminForm(forms.ModelForm):
    '''Form to set up admin profile'''
    
    class Meta:
        model = Admin
        fields = '__all__'
        exclude = ['id', 'user']
        

class ChangeProfilePictureForm(forms.ModelForm):
    '''Form to change profile picture'''
    
    class Meta:
        model = User
        fields = ['profile_pic']
        

class ChangeEmailForm(forms.Form):
    '''Form to change email'''
    
    email = form_text_field(forms.EmailField, forms.EmailInput, 'Email')
        
    def clean(self):
        cleaned_data = super().clean()  # Call parent's clean method first

        email = cleaned_data.get('email')
        
        # Email uniqueness
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already exists!')
        
        return cleaned_data
        

class ChangeDetailsForm(forms.Form):
    '''Form to change user details'''
    
    first_name = form_text_field(forms.CharField, forms.TextInput, 'First name')
    last_name = form_text_field(forms.CharField, forms.TextInput, 'Last name')
        

class ChangePasswordForm(forms.Form):
    '''Form to change profile picture'''
    
    email = form_text_field(forms.EmailField, forms.EmailInput, 'Email')
    password = form_text_field(forms.CharField, forms.PasswordInput, 'Password')
    confirm_password = form_text_field(forms.CharField, forms.PasswordInput, 'Confirm Password')
    
    def clean(self):
        cleaned_data = super().clean()  # Call parent's clean method first

        password = cleaned_data.get('password')
        password2 = cleaned_data.get('confirm_password')
        
        # Password checks
        if password != password2:
            raise forms.ValidationError('Passwords do not match!')

        if not is_valid_password(password):
            raise forms.ValidationError('Password should have uppercase, lowercase, special character and should have at least 8 characters')
        
        return cleaned_data
    
    
