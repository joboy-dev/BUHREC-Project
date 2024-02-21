from django.urls import path
from . import views

app_name = 'project'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('projects/', views.ProjectsView.as_view(), name='projects'),
    path('projects/create/', views.CreateProjectView.as_view(), name='create-project'),
]