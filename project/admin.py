from django.contrib import admin

from project.models import Project, Reviewer, Assignment

# Register your models here.
admin.site.register(Project)
admin.site.register(Reviewer)
admin.site.register(Assignment)
