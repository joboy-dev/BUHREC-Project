from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import View, generic
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from datetime import datetime

from project.models import Project, Reviewer, Assignment, Remark
from user.models import Admin, StudentOrResearcher
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
        projects = Project.objects.filter(
            owner=StudentOrResearcher.objects.get(user=request.user)
        )
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
            project = Project.objects.create(
                **form.cleaned_data,       
                owner=StudentOrResearcher.objects.get(user=request.user)
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
    

class GetProjectDetail(LoginRequiredMixin, View):
    '''View to get details about a particular project'''
    
    login_url = 'user:login'
    
    model = Project
    template_name = 'project/project-detail.html'
    context_object_name = 'project'
    success_message = 'Remark sent successfully'
    
    permission_required = 'user.is_reviewer'
    permission_denied_message = 'Access denied as you are not a reviewer'
    
    def get(self, request, id):
        project = self.model.objects.get(id=id)
        
        # get all remarks
        remarks = Remark.objects.filter(project=project)
        # get reviewer for project through assignments
        project_reviewer = Assignment.objects.get(project=project).reviewer
        
        context['form'] = forms.AddRemarkForm()
        context['project'] = project
        context['remarks'] = remarks
        context['project_reviewer'] = project_reviewer
        
        if request.user.role == 'student':
            context['active_link'] = 'projects'
        elif request.user.role == 'reviewer':
            context['active_link'] = 'assignments'
            
        return render(request, self.template_name, context)
    
    def post(self, request, id):
        form = forms.AddRemarkForm(request.POST)
        
        if form.is_valid():
            message = form.cleaned_data['message']
            user = request.user
            
            # Permission check
            if not IsReviewer.has_permission(request, user):
                messages.error(request, f'{self.permission_denied_message}')
            else:
                # create remark
                project = Project.objects.get(id=id)
                reviewer = Reviewer.objects.get(user=user)
                Remark.objects.create(
                    message=message,
                    project=project,
                    reviewer=reviewer,
                )
                messages.success(request, f'{self.success_message}')
                return redirect(reverse_lazy('project:assignments'))
                        
        context['form'] = form
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f'{error}')
        
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
        return super().dispatch(request, id)
    
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
        assignments = Assignment.objects.filter(reviewer=reviewer, is_complete=False)
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
    
    def get(self, request):
        admin = Admin.objects.get(user=request.user)
        projects = Project.objects.all()
        context['active_link'] = 'dashboard'
        context['admin'] = admin
        context['projects'] = projects
        return render(request, 'admin/admin-dashboard.html', context)
    
        