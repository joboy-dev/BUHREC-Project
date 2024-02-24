from django.urls import path
from . import views

app_name = 'project'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('projects/', views.ProjectsView.as_view(), name='projects'),
    path('projects/create/', views.CreateProjectView.as_view(), name='create-project'),
    path('project/<uuid:id>/', views.GetProjectDetail.as_view(), name='detail'),
    path('project/<uuid:id>/edit/', views.EditProjectView.as_view(), name='edit-project'),
    
    # REVIEWER
    path('assignments/', views.AssignmentsView.as_view(), name='assignments'),
    path('project/<uuid:id>/toggle-approval/', views.ToggleApprovalProjectView.as_view(), name='toggle-approval'),
    
    # ADMIN
    path('dashboard/', views.AdminDashboardView.as_view(), name='admin-dashboard'),
]