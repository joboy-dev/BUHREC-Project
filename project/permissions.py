from django.contrib.auth.models import Permission

class IsProjectOwner(Permission):
    '''Permission to check if current logged in user is the owner of the project'''
    
    name = 'Is project owner'
    codename = 'is_project_owner'
    
    @staticmethod
    def has_permission(request, obj):
        return obj.owner.user == request.user
        