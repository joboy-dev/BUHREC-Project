from django import forms

from user.reusable_form_field import form_text_field

from .models import Project, Remark

class CreateProjectForm(forms.ModelForm):
    '''Form to create a project'''
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["hypothesis"].required = False
        
    
    title = form_text_field(forms.CharField, forms.TextInput, 'Project title', max_length=25)
    
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
        
    title = form_text_field(forms.CharField, forms.TextInput, 'Project title', max_length=25)

    class Meta:
        model = Project
        fields = '__all__'
        exclude = ['id', 'approved', 'owner', 'payment_approved', 'track_id']


###############################################################################
###############################################################################
###############################################################################

# REMARK

class AddRemarkForm(forms.ModelForm):
    '''Form to add remark '''
    
    class Meta:
        model = Remark
        fields = '__all__'
        exclude = ['id', 'project', 'reviewer']
        

class EditRemarkForm(forms.ModelForm):
    '''Form to edit remark '''
    
    class Meta:
        model = Remark
        fields = '__all__'
        exclude = ['id', 'project', 'reviewer']
    


###############################################################################
###############################################################################
###############################################################################

# CONTACT

class ContactForm(forms.Form):
    '''Contact form'''
    
    name = form_text_field(forms.CharField, forms.TextInput, 'Full name')
    email = form_text_field(forms.CharField, forms.TextInput, 'Email')
    message = form_text_field(forms.CharField, forms.Textarea, 'Message')