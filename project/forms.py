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
        exclude = ['id', 'approved', 'owner', 'payment_approved', 'track_id']
        
    def clean(self):
        cleaned_data = super().clean()  # Call parent's clean method first

        title = cleaned_data.get('title')
        
        # Password checks
        if Project.objects.filter(title=title).exists():
            raise forms.ValidationError('This project title already exists!')
        
        return cleaned_data
    
    
    
class EditProjectForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["hypothesis"].required = False
        
    
    title = forms.CharField(max_length=25, required=True, widget=forms.TextInput(attrs={'placeholder': 'Project title', 'class': 'input-field'}))
    
    class Meta:
        model = Project
        fields = '__all__'
        exclude = ['id', 'approved', 'owner', 'payment_approved', 'track_id']
                
    def clean(self):
        cleaned_data = super().clean()  # Call parent's clean method first

        title = cleaned_data.get('title')
        
        # Password checks
        if Project.objects.filter(title=title).exists():
            raise forms.ValidationError('This project title already exists!')
        
        return cleaned_data
    