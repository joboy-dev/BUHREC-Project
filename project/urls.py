from django.urls import path
from . import views

app_name = 'project'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('send-message', views.ProcessContactFormView.as_view(), name='send-message'),
    path('projects/', views.ProjectsView.as_view(), name='projects'),
    path('projects/create/', views.CreateProjectView.as_view(), name='create-project'),
    path('project/<uuid:id>/', views.GetProjectDetail.as_view(), name='detail'),
    path('project/<uuid:id>/edit/', views.EditProjectView.as_view(), name='edit-project'),
    path('project/<uuid:id>/delete/', views.DeleteProjectView.as_view(), name='delete-project'),
    path('project/<uuid:id>/payment/', views.ProcessPaymentView.as_view(), name='pay-for-project'),
    
    # REVIEWER
    path('assignments/', views.AssignmentsView.as_view(), name='assignments'),
    path('project/<uuid:id>/toggle-approval/', views.ToggleApprovalProjectView.as_view(), name='toggle-approval'),
    
    # ADMIN
    path('dashboard/', views.AdminDashboardView.as_view(), name='admin-dashboard'),
    path('project/<uuid:id>/assign-track-id/', views.AssignProjectTrackIdView.as_view(), name='assign-track-id'),
    path('assignment/<uuid:id>/assign-reviewer/', views.GiveAssignmentView.as_view(), name='assign-reviewer'),
    path('assignment/<uuid:id>/withdraw/', views.WithdrawAssignmentView.as_view(), name='withdraw-assignment'),
    
    path('project/search/', views.SearchProjectsView.as_view(), name='search-project'),
    path('project/search/<uuid:track_id>/', views.SearchResultsView.as_view(), name='search-results'),
]