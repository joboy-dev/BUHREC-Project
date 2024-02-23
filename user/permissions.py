from django.contrib.auth.models import Permission

class IsStudentOrResearcher(Permission):
    '''Permission to check is a user's role is a student or researcher'''
    
    name = 'Is student or researcher'
    codename = 'is_student_or_researcher'
    
    @staticmethod
    def has_permission(request, obj):
        return obj.role == 'student' or obj.role == 'researcher'
    

class IsReviewer(Permission):
    '''Permission to check is a user's role is a reviewer'''
    
    name = 'Is reviewer'
    codename = 'is_reviewer'
    
    @staticmethod
    def has_permission(request, obj):
        return obj.role == 'reviewer'