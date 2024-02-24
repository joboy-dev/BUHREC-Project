from django import forms

from .models import Project, Remark

class CreateProjectForm(forms.ModelForm):
    '''Form to create a project'''
    
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
    '''Form to edit a project '''
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["hypothesis"].required = False
        
    title = forms.CharField(max_length=25, required=True, widget=forms.TextInput(attrs={'placeholder': 'Project title', 'class': 'input-field'}))
        
    class Meta:
        model = Project
        fields = '__all__'
        exclude = ['id', 'approved', 'owner', 'payment_approved', 'track_id']


# REMARK

class AddRemarkForm(forms.ModelForm):
    '''Form to add remark '''
    
    # message = forms.CharField(max_length=25, required=True, widget=forms.Textarea(attrs={'class': 'textarea-field'}))
    
    class Meta:
        model = Remark
        fields = '__all__'
        exclude = ['id', 'project', 'reviewer']
        

class EditRemarkForm(forms.ModelForm):
    '''Form to add remark '''
    
    # message = forms.CharField(max_length=25, required=True, widget=forms.Textarea(attrs={'class': 'textarea-field'}))
    
    class Meta:
        model = Remark
        fields = '__all__'
        exclude = ['id', 'project', 'reviewer']
    