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
            password = form.cleaned_data['password']
            role = form.cleaned_data['role']
            
            # pop unnecessary data
            form.cleaned_data.pop('confirm_password')
            
            # Sign up and login logic
            user = User.objects.create(
                **form.cleaned_data
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
    

class UserDetailsView(LoginRequiredMixin, View):
    '''View to get user details'''
    
    login_url = 'user:login'
    
    def get(self, request):
        user = request.user
        
        change_picture_form = forms.ChangeProfilePictureForm()
        change_detail_form = forms.ChangeDetailsForm(instance=user)
        change_email_form = forms.ChangeEmailForm(instance=user)
        change_password_form = forms.ChangePasswordForm()
        
        context['change_picture_form'] = change_picture_form
        context['change_detail_form'] = change_detail_form
        context['change_email_form'] = change_email_form
        context['change_password_form'] = change_password_form
        
        if user.role == 'student' or user.role == 'researcher':
            context['student_researcher'] = StudentOrResearcher.objects.get(user=user)
        elif user.role == 'reviewer':
            context['reviewer'] = Reviewer.objects.get(user=user)
        elif user.role == 'admin':
            context['admin'] = Admin.objects.get(user=user)
            
        return render(request, 'user/profile.html', context)
    

class ChangeProfilePictureView(LoginRequiredMixin, View):
    '''View to update profile picture for a user'''
    
    login_url = 'user:login'
    
    def post(self, request):    
        change_picture_form = forms.ChangeProfilePictureForm(request.POST, request.FILES)
        
        if change_picture_form.is_valid():
            profile_pic = change_picture_form.cleaned_data['profile_pic']

            # Save changes
            request.user.profile_pic = profile_pic
            request.user.save()
            
            messages.success(request, 'Profile picture updated successfully')
            return redirect(reverse_lazy('user:profile'))
            
        
        context['change_picture_form'] = change_picture_form
        for field, errors in change_picture_form.errors.items():
            for error in errors:
                messages.error(request, f'{error}')
                
        return render(request, 'user/profile.html', context)
    

class ChangeEmailView(LoginRequiredMixin, View):
    '''View to change a user's email'''
    
    login_url = 'user:login'
    
    def post(self, request):    
        change_email_form = forms.ChangeEmailForm(request.POST)
        
        if change_email_form.is_valid():
            email = change_email_form.cleaned_data['email']

            # Save changes
            request.user.email = email
            request.user.save()
            
            messages.success(request, 'Email updated successfully')
            return redirect(reverse_lazy('user:profile'))
            
        
        context['change_email_form'] = change_email_form
        for field, errors in change_email_form.errors.items():
            for error in errors:
                messages.error(request, f'{error}')
                
        return render(request, 'user/profile.html', context)
    

class ChangeDetailsView(LoginRequiredMixin, View):
    '''View to change a user's first and last name details'''
    
    login_url = 'user:login'
    
    
    def post(self, request):    
        change_detail_form = forms.ChangeDetailsForm(request.POST)
        
        if change_detail_form.is_valid():
            first_name = change_detail_form.cleaned_data['first_name']
            last_name = change_detail_form.cleaned_data['last_name']

            # Save changes
            request.user.first_name = first_name
            request.user.last_name = last_name
            request.user.save()
            
            messages.success(request, 'Details updated successfully')
            return redirect(reverse_lazy('user:profile'))
            
        context['change_detail_form'] = change_detail_form
        for field, errors in change_detail_form.errors.items():
            for error in errors:
                messages.error(request, f'{field.capitalize()}: {error}')
                
        return render(request, 'user/profile.html', context)
        

class ChangePasswordView(LoginRequiredMixin, View):
    '''View to change a user's email'''
    
    login_url = 'user:login'
    
    def post(self, request):    
        change_password_form = forms.ChangePasswordForm(request.POST)
        
        if change_password_form.is_valid():
            old_password = change_password_form.cleaned_data['old_password']
            new_password = change_password_form.cleaned_data['new_password']
            
            # Check if user credentials match
            user = authenticate(request, email=request.user.email, password=old_password) 
            if user is None:
                messages.error(request, 'Invalid credentials. Check your old password.')
                return render(request, 'user/profile.html', context)

            # Save changes
            user.set_password(new_password)
            user.save()
            
            messages.success(request, 'Password updated successfully. Please login again with your new password for changes to take full effect.')
            return redirect(reverse_lazy('user:profile'))
            
        
        context['change_password_form'] = change_password_form
        for field, errors in change_password_form.errors.items():
            for error in errors:
                messages.error(request, f'{error}')
                
        return render(request, 'user/profile.html', context)

def logout_view(request):
    '''View to logout a user'''

    logout_url = reverse('user:login')

    current_user = request.user
    logout(request)

    messages.success(request, f'See you soon, {current_user.first_name}')
    return redirect(logout_url)