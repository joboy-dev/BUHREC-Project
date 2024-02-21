from django import forms

from django_ckeditor_5.widgets import CKEditor5Widget

from .models import Project

class CreateProjectForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["hypothesis"].required = False
        
    
    title = forms.CharField(max_length=25, required=True, widget=forms.TextInput(attrs={'placeholder': 'Project title', 'class': 'input-field'}))
    
    
    class Meta:
        model = Project
        fields = '__all__'
        exclude = ['id', 'approved', 'owner']
        

# class CreateProjectForm(forms.Form):
    
#     title = forms.CharField(max_length=25, required=True, widget=forms.TextInput(attrs={'placeholder': 'Project title', 'class': 'input-field'}))
    
    