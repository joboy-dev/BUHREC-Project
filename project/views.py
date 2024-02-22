from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.views import View, generic
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from datetime import datetime

from project.models import Project
from . import forms

context = {
    'year': datetime.now().year
}

# Create your views here.
class HomeView(View):
    '''Home View'''
    
    def get(self, request):
        context['active_link'] = 'home'
        return render(request, 'index.html', context)
    

class ProjectsView(LoginRequiredMixin, generic.ListView):
    '''View to get all projects'''
    
    login_url = 'user:login'
    
    model = Project
    template_name = 'project/projects.html'
    context_object_name = 'projects'
    
    def get(self, request):
        context['active_link'] = 'projects'
        
        projects = Project.objects.filter(owner=self.request.user)
        context['projects'] = projects
        return render(request, self.template_name, context)
    

class GetProjectDetail(LoginRequiredMixin, generic.DetailView):
    '''View to get details about a particular project'''
    
    login_url = 'user:login'
    
    model = Project
    template_name = 'project/project-detail.html'
    context_object_name = 'project'
    
    def get(self, request, id):
        project = self.model.objects.get(id=id)
        context['project'] = project
        return render(request, self.template_name, context)    
    

class CreateProjectView(LoginRequiredMixin, generic.CreateView):
    '''View to create a project'''
    
    login_url = 'user:login'
    
    model = Project
    template_name = 'project/create-project.html'
    form_class = forms.CreateProjectForm
    success_message = 'Project created successfully'
    success_url = reverse_lazy('project:projects')
    
    def get(self, request):
        context['active_link'] = 'projects'
        context['form'] = self.form_class()
        return render(request, self.template_name, context)
    
    def post(self, request):
        form = self.form_class(request.POST)
        
        if form.is_valid():
            title = form.cleaned_data['title']
            introduction = form.cleaned_data['introduction']
            background = form.cleaned_data['background']
            scope_and_limitation = form.cleaned_data['scope_and_limitation']
            justification = form.cleaned_data['justification']
            objectives = form.cleaned_data['objectives']
            hypothesis = form.cleaned_data['hypothesis']
            literature_review = form.cleaned_data['literature_review']
            materials_and_methods = form.cleaned_data['materials_and_methods']
            procedure = form.cleaned_data['procedure']
            
            Project.objects.create(
                title=title,              
                introduction=introduction,              
                background=background,                
                scope_and_limitation=scope_and_limitation,                
                justification=justification,                
                objectives=objectives,                
                hypothesis=hypothesis,                
                literature_review=literature_review,                
                materials_and_methods=materials_and_methods,                
                procedure=procedure,        
                owner=request.user        
            )

            messages.success(request, f'{self.success_message}')
            return redirect(self.success_url)
        
        context['form'] = form
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f'{error}')
        
        return render(request, self.template_name, context)
            
            
