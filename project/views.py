from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import View, generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model

from uuid import uuid4
from datetime import datetime

from project.models import Project, Reviewer, Assignment, Remark
from project.permissions import IsProjectOwner
from user.models import Admin, StudentOrResearcher
from user.permissions import IsAdmin, IsAsstChairAdmin, IsChairAdmin, IsReviewer, IsStudentOrResearcher
from . import forms

context = {
    'year': datetime.now().year
}

User = get_user_model()

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
        project = get_object_or_404(Project, id=id)
        
        # get all remarks for a project
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
            
            # Permission check for reviewer to create a remark
            if not IsReviewer.has_permission(request, user):
                messages.error(request, f'{self.permission_denied_message}')
            else:
                # create remark
                project = get_object_or_404(Project, id=id)
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
                
    

class EditProjectView(LoginRequiredMixin, generic.UpdateView):
    '''View to edit a project'''  
    
    login_url = 'user:login'
    
    model = Project
    template_name = 'project/edit-project.html'
    form_class = forms.EditProjectForm
    success_url = reverse_lazy('project:projects')
    success_message = 'Project updated successfully'
    context_object_name = 'project'
    
    permission_required = 'project.is_project_owner'
    permission_denied_message = 'You do not have access to this project'
    
    def dispatch(self, request, id):
        # check permission
        if not IsProjectOwner.has_permission(request, get_object_or_404(Project, id=id)):
            messages.error(request, f'{self.permission_denied_message}')
            return redirect(reverse_lazy('project:home'))
        return super().dispatch(request, id)
    
    def get(self, request, id):
        project = get_object_or_404(Project, id=id)
        form = self.form_class(instance=project)
        context['form'] = form
        context['active_link'] = 'projects'
        return render(request, self.template_name, context)
    
    def post(self, request, id):
        form = self.form_class(request.POST)
        
        if form.is_valid():
            Project.objects.filter(id=id).update(**form.cleaned_data)

            messages.success(request, f'{self.success_message}')
            return redirect(self.success_url)
        
        context['form'] = form
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f'{error}')
        
        return render(request, self.template_name, context)
    
    
class DeleteProjectView(LoginRequiredMixin, generic.DeleteView):
    '''View to delete a project'''
    
    login_url = 'user:login'
    model = Project
    success_message = 'Project deleted successfully'
    success_url = reverse_lazy('project:projects')
    
    def post(self, request, id):
        user = request.user
        
        # check permission
        if not IsProjectOwner.has_permission(request, get_object_or_404(Project, id=id)):
            messages.error(request, 'You cannot delete another user\'s project')
            return redirect(reverse_lazy('project:home'))
        
        get_object_or_404(Project, id=id).delete()
        messages.success(request, f'{self.success_message}')
        
        return redirect(self.success_url)
    
    
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
        project = get_object_or_404(Project, id=id)
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
    
    login_url = 'user:login'
    
    permission_required = 'user.is_admin'
    permission_denied_message = 'Access denied as you are not n admin'
    
    def dispatch(self, request):
        user = request.user
        # check permission
        if not IsAdmin.has_permission(request, user):
            messages.error(request, f'{self.permission_denied_message}')
            return redirect(reverse_lazy('project:home'))
        return super().dispatch(request)
    
    def get(self, request):
        admin = Admin.objects.get(user=request.user)
        assignments = Assignment.objects.all()
        projects = Project.objects.all()
        unassigned_projects = Project.objects.filter(track_id=None)
        reviewers = Reviewer.objects.all()
        
        context['active_link'] = 'dashboard'
        context['admin'] = admin
        context['assignments'] = assignments
        context['projects'] = projects
        context['unassigned_projects'] = unassigned_projects
        context['reviewers'] = reviewers
        return render(request, 'admin/admin-dashboard.html', context)
    

class AssignProjectTrackIdView(LoginRequiredMixin, View):
    '''View for admin asst chair to assign a track id to a project'''
    
    login_url = 'user:login'
    
    def post(self, request, id):
        admin = Admin.objects.get(user=request.user)
        if not IsAsstChairAdmin.has_permission(request, admin):
            messages.error(request, 'Access denied as you are not an assistant chair admin')
            return redirect(reverse_lazy('project:home'))
        
        project = get_object_or_404(Project, id=id)
        # Assign track id to the project using uuid4
        project.track_id = uuid4()
        project.save()
        
        messages.success(request, 'Track id assigned successfully')
        return redirect(reverse_lazy('project:admin-dashboard'))
        
    
class GiveAssignmentView(LoginRequiredMixin, View):
    '''View for admin chair to give assignments from a reviewer'''
    
    login_url = 'user:login'
    
    def post(self, request, id):
        admin = Admin.objects.get(user=request.user)
        if not IsChairAdmin.has_permission(request, admin):
            messages.error(request, 'Access denied as you are not a chair admin')
            return redirect(reverse_lazy('project:home'))
        
        assignment = get_object_or_404(Assignment, id=id)
        
        # Get reviewer email from form select field and strip it down
        reviewer_email = request.POST['reviewer'].strip()
        
        # Check if user selected a reviewer
        if reviewer_email == 'none':
            messages.error(request, 'Select a reviewer')
            return redirect(reverse_lazy('project:admin-dashboard'))
        
        # user = User.objects.get(email=reviewer_email)
        
        # Get user based on the email gotten from the form
        user = get_object_or_404(User, email=reviewer_email)
        
        # Get reviewer based on the user object
        reviewer = get_object_or_404(Reviewer, user=user)
        
        # Update reviewer data
        reviewer.pending_assignments_no += 1
        # Assign reviewer object to the assignment
        assignment.reviewer = reviewer
        
        assignment.save()
        reviewer.save()
        
        messages.success(request, f"Reviewer '{reviewer.user}' assigned to project '{assignment.project.title}'.")
        return redirect(reverse_lazy('project:admin-dashboard'))
        
        
class WithdrawAssignmentView(LoginRequiredMixin, View):
    '''View for admin chair to withdraw assignments from a reviewer'''
    
    login_url = 'user:login'
    
    def post(self, request, id):
        admin = Admin.objects.get(user=request.user)
        if not IsChairAdmin.has_permission(request, admin):
            messages.error(request, 'Access denied as you are not a chair admin')
            return redirect(reverse_lazy('project:home'))
        
        assignment = get_object_or_404(Assignment, id=id)
        
        # Get reviewer based on the reviewer linked to assignment
        reviewer = get_object_or_404(Reviewer, id=assignment.reviewer.id)
        
        # Update reviewer data
        reviewer.pending_assignments_no -= 1
        reviewer.withdrawn_assignments_no += 1 
        # Assign reviewer object to the assignment
        assignment.reviewer = None
        
        assignment.save()
        reviewer.save()
        
        messages.success(request, f"Reviewer '{reviewer.user}' removed from project '{assignment.project.title}'.")
        return redirect(reverse_lazy('project:admin-dashboard'))


class SearchProjectsView(LoginRequiredMixin, View):
    '''View to search for projects'''
    
    login_url = 'user:login'
    
    def post(self, request):
        search_term = request.POST['search']
        projects = Project.objects.filter(title=search_term)
        
        context['searched_projetcs'] = projects
        
        if len(projects) == 0:
            messages.error(request, 'No results found.')
        else:
            messages.success(request, f'{len(projects)} result(s) found.')
            
        return render(request, 'admin/admin-dashboard.html', context)
    