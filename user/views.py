from datetime import datetime
import re

from django.shortcuts import render, redirect
from django.views import generic, View
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model

from . import forms

def is_valid_password(password):
    '''Function to check if password is valid'''
    
    # Regular expression for a valid password
    # Password must contain at least 8 characters, including one uppercase letter, one lowercase letter, one digit, and one special character.
    password_regex = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
    
    if re.match(password_regex, password):
        return True
    else:
        return False

User = get_user_model()

context = {
     'year': datetime.now().year
}

class SignUpView(generic.CreateView):
    '''View to register users'''
    
    model = User
    template_name = 'user/signup.html'
    form_class = forms.SignUpForm
    success_url = reverse_lazy('project:home')
    
    def get(self, request):
        form = self.form_class()
        context['active_link'] = 'signup'
        context['form'] = form
        return render(request, self.template_name, context)
    
    def post(self, request):
        form = self.form_class(request.POST)
        
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            # password2 = form.cleaned_data['confirm_password']
            role = form.cleaned_data['role']
            
            # Sign up and login logic
            user = User.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
                role=role,
            )
                    
            user.set_password(password)
            user.save()
                    
            # Login user
            login(request, user)
                    
            messages.success(request, f'Account created successfully. Welcome, {first_name}')
            return redirect(self.success_url)
        
        context['form'] = form
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f'{error}')
                
        return render(request, self.template_name, context)
        

class LoginView(View):
    '''View to log in users'''
    
    def get(self, request):
        form = forms.LoginForm()
        context['active_link'] = 'login'
        context['form'] = form
        return render(request, 'user/login.html', context)
    
    def post(self, request):
        form = forms.LoginForm(request.POST)
        
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            user = authenticate(request, email=email, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name}') 
                return redirect(reverse_lazy('project:home'))
            else:
                messages.error(request, 'Invalid credentials. Try again.')
                context['form'] = form
                return render(request, 'user/login.html', context)
        
        messages.error(request, 'An error occured')
        return render(request, 'user/login.html', context)
        
        