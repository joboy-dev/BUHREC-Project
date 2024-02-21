from django.shortcuts import render
from django.urls import reverse_lazy
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
    
    model = Project
    template_name = 'project/projects.html'
    context_object_name = 'projects'
    
    def get(self, request):
        context['active_link'] = 'projects'
        return render(request, self.template_name, context)
    

class CreateProjectView(LoginRequiredMixin, generic.CreateView):
    '''View to create a project'''
    
    model = Project
    template_name = 'project/create-project.html'
    form_class = forms.CreateProjectForm
    success_message = 'Project created successfully'
    success_url = reverse_lazy('project:projects')
    
    def get(self, request):
        context['active_link'] = 'projects'
        context['form'] = self.form_class()
        return render(request, self.template_name, context)
    