from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View, generic

from datetime import datetime

from project.models import Project

context = {
    'year': datetime.now().year
}

# Create your views here.
class HomeView(View):
    '''Home View'''
    
    def get(self, request):
        context['active_link'] = 'home'
        return render(request, 'index.html', context)
    

class ProjectsView(generic.ListView):
    '''View to get all projects'''
    
    model = Project
    template_name = 'project/projects.html'
    context_object_name = 'projects'
    
    def get(self, request):
        context['active_link'] = 'projects'
        return render(request, self.template_name, context)
        