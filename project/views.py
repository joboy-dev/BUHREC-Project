from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import View, generic
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from datetime import datetime

from project.models import Project, Reviewer, Assignment
from user.permissions import IsReviewer, IsStudentOrResearcher
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


class AboutView(View):
    '''About View'''
    
    def get(self, request):
        context['active_link'] = 'about'
        return render(request, 'about.html', context)
    

class ProjectsView(LoginRequiredMixin, generic.ListView):
    '''View to get all projects'''
    
    login_url = 'user:login'
    
    model = Project
    template_name = 'project/projects.html'
    context_object_name = 'projects'
    
    permission_required = 'user.is_student_or_researcher'
    permission_denied_message = 'Access denied as you are not a student or researcher'
    
    def dispatch(self, request):
        user = request.user
        # check permission
        if not IsStudentOrResearcher.has_permission(request, user):
            messages.error(request, f'{self.permission_denied_message}')
            return redirect(reverse_lazy('project:home'))
        return super().dispatch(request)
    
    def get(self, request):
        projects = Project.objects.filter(owner=self.request.user)
        context['active_link'] = 'projects'
        context['projects'] = projects
        return render(request, self.template_name, context)
    

class CreateProjectView(LoginRequiredMixin, generic.CreateView):
    '''View to create a project'''
    
    login_url = 'user:login'
    
    model = Project
    template_name = 'project/create-project.html'
    form_class = forms.CreateProjectForm
    success_message = 'Project created successfully'
    success_url = reverse_lazy('project:projects')
    
    permission_required = 'user.is_student_or_researcher'
    permission_denied_message = 'Access denied as you are not a student or researcher'
    
    def dispatch(self, request):
        user = request.user
        
        # check permission
        if not IsStudentOrResearcher.has_permission(request, user):
            messages.error(request, f'{self.permission_denied_message}')
            return redirect(reverse_lazy('project:home'))
        return super().dispatch(request)
    
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
            
            project = Project.objects.create(
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
            
            # Create assignment
            Assignment.objects.create(project=project)

            messages.success(request, f'{self.success_message}')
            return redirect(self.success_url)
        
        context['form'] = form
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f'{error}')
        
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
        context['active_link'] = 'projects'
        return render(request, self.template_name, context)
    

class EditProjectView(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    '''View to edit a project'''  
    
    login_url = 'user:login'
    
    model = Project
    template_name = 'project/edit-project.html'
    form_class = forms.EditProjectForm
    success_url = reverse_lazy('project:projects')
    success_message = 'Project updated successfully'
    context_object_name = 'project'
    
    permission_required = 'project.is_project_owner'
    permission_denied_message = 'Access denied as you are not the owner of this project'
    
    def dispatch(self, request, id):
        user = request.user
        
        # check permission
        if not IsStudentOrResearcher.has_permission(request, user):
            messages.error(request, f'{self.permission_denied_message}')
            return redirect(reverse_lazy('project:home'))
        return super().dispatch(request)
    
    def get(self, request, id):
        project = Project.objects.get(id=id)
        form = self.form_class(instance=project)
        context['form'] = form
        context['active_link'] = 'projects'
        return render(request, self.template_name, context)
    
    
#########################################################
#########################################################

# REVIEWER VIEWS

class AssignmentsView(LoginRequiredMixin, View):
    '''View to get all current assignements'''
    
    login_url = 'user:login'
    
    template_name = 'project/assignments.html'
    context_object_name = 'projects'
    
    permission_required = 'user.is_reviewer'
    permission_denied_message = 'Access denied as you are not a reviewer'
    
    def dispatch(self, request):
        user = request.user
        # check permission
        if not IsReviewer.has_permission(request, user):
            messages.error(request, f'{self.permission_denied_message}')
            return redirect(reverse_lazy('project:home'))
        return super().dispatch(request)
    
    def get(self, request):
        reviewer = Reviewer.objects.get(user=request.user)
        # get all assignments
        assignments = Assignment.objects.filter(reviewer=reviewer)
        completed_assignments = Assignment.objects.filter(reviewer=reviewer, is_complete=True)
        
        context['active_link'] = 'assignments'
        context['assignments'] = assignments
        context['completed_assignments'] = completed_assignments
        
        return render(request, self.template_name, context)
    
    
class ToggleApprovalProjectView(LoginRequiredMixin, View):
    '''View to approve a project'''
    
    login_url = 'user:login'
    
    permission_required = 'user.is_reviewer'
    permission_denied_message = 'Access denied as you are not a reviewer'
    
    def dispatch(self, request, id):
        user = request.user
        # check permission
        if not IsReviewer.has_permission(request, user):
            messages.error(request, f'{self.permission_denied_message}')
            return redirect(reverse_lazy('project:home'))
        return super().dispatch(request, id)
    
    def post(self, request, id):
        project= Project.objects.get(id=id)
        reviewer = Reviewer.objects.get(user=request.user)
        assignment = Assignment.objects.get(project=project)
        
        if not project.approved:
            reviewer.completed_assignments_no += 1
            reviewer.pending_assignments_no -= 1
        else:
            reviewer.completed_assignments_no -= 1
            reviewer.pending_assignments_no += 1
        
        # Update project approved status and assignment completion status
        project.approved = not project.approved
        assignment.is_complete = not assignment.is_complete
        
        # Save instances
        project.save()
        reviewer.save()
        assignment.save()
        
        messages.success(request, 'Approval status changed')
        return redirect(reverse_lazy('project:assignments'))
    
    

################################################
################################################

# ADMIN VIEWS
        
class AdminDashboardView(LoginRequiredMixin, View):
    '''View for admin to see their dashboard'''
    
           
    
        