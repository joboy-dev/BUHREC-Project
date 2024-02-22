from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('student-researcher/save/', views.StudentResearcherSignUpView.as_view(), name='student-researcher-signup'),
    path('reviewer/save/', views.ReviewerSignUpView.as_view(), name='reviewer-signup'),
    
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout')
]