from datetime import datetime
import re

from django.shortcuts import render, redirect
from django.views import generic, View
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model

from project.models import Reviewer

from . import forms
from .models import Admin, CustomUser, StudentOrResearcher

User = get_user_model()

context = {
     'year': datetime.now().year
}

class SignUpView(generic.CreateView):
    '''View to register users'''
    
    model = User
    template_name = 'user/signup.html'
    form_class = forms.SignUpForm
    success_url = reverse_lazy('user:student-researcher-signup')
    
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
            
            if role == 'reviewer':
                self.success_url = reverse_lazy('user:reviewer-signup')
            if role == 'admin':
                self.success_url = reverse_lazy('user:admin-signup')
            return redirect(self.success_url)
        
        context['form'] = form
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f'{error}')
                
        return render(request, self.template_name, context)
    

class StudentResearcherSignUpView(generic.CreateView):
    '''View to set up studnt and researcher profile'''
    
    model = StudentOrResearcher
    template_name = 'user/student-researcher-signup.html'
    form_class = forms.StudentResearcherForm
    success_url = reverse_lazy('project:home')
    
    def get(self, request):
        form = self.form_class()
        context['active_link'] = 'account'
        context['form'] = form
        return render(request, self.template_name, context)
    
    def post(self, request):
        form = self.form_class(request.POST)
        
        if form.is_valid():
            degree = form.cleaned_data['degree']
            pg_degree = form.cleaned_data['pg_degree']
            programme = form.cleaned_data['programme']
            
            # Sign up and login logic
            StudentOrResearcher.objects.create(
                degree=degree,
                pg_degree=pg_degree,
                programme=programme,
                user=request.user,
            )
            
            user = User.objects.get(id=request.user.id)
            user.is_verified = True
            user.save()
                    
            messages.success(request, f'Profile saved')
            return redirect(self.success_url)
        
        context['form'] = form
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f'{error}')
                
        return render(request, self.template_name, context)
    

class ReviewerSignUpView(generic.CreateView):
    '''View to set up studnt and researcher profile'''
    
    model = Reviewer
    template_name = 'user/reviewer-signup.html'
    form_class = forms.ReviewerForm
    success_url = reverse_lazy('project:home')
    
    def get(self, request):
        form = self.form_class()
        context['active_link'] = 'account'
        context['form'] = form
        return render(request, self.template_name, context)
    
    def post(self, request):
        form = self.form_class(request.POST)
        
        if form.is_valid():
            country_domicile = form.cleaned_data['country_domicile']
            institution_name = form.cleaned_data['institution_name']
            years_of_reviewing = form.cleaned_data['years_of_reviewing']
            
            # Sign up and login logic
            Reviewer.objects.create(
                country_domicile=country_domicile,
                institution_name=institution_name,
                years_of_reviewing=years_of_reviewing,
                user=request.user,
            )
            
            user = User.objects.get(id=request.user.id)
            user.is_verified = True
            user.save()
                    
            messages.success(request, f'Profile saved')
            return redirect(self.success_url)
        
        context['form'] = form
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f'{error}')
                
        return render(request, self.template_name, context)
        
        

class AdminSignUpView(generic.CreateView):
    '''View to set up studnt and researcher profile'''
    
    model = Admin
    template_name = 'user/admin-signup.html'
    form_class = forms.AdminForm
    success_url = reverse_lazy('project:home')
    
    def get(self, request):
        form = self.form_class()
        context['active_link'] = 'account'
        context['form'] = form
        return render(request, self.template_name, context)
    
    def post(self, request):
        form = self.form_class(request.POST)
        
        if form.is_valid():
            role = form.cleaned_data['role']
            
            # Sign up and login logic
            Admin.objects.create(
                role=role,
                user=request.user,
            )
            
            user = User.objects.get(id=request.user.id)
            user.is_verified = True
            user.save()
                    
            messages.success(request, f'Profile saved')
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
        

def logout_view(request):
    '''View to logout a user'''

    logout_url = reverse('user:login')

    current_user = request.user
    logout(request)

    messages.success(request, f'See you soon, {current_user.first_name}')
    return redirect(logout_url)