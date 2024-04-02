from datetime import datetime
import re
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

# PAYMENT

class ProcessPaymentForm(forms.Form):
    '''Form to pay for a project'''
    
    card_number = form_text_field(forms.CharField, widget=forms.TextInput, placeholder='Card number', max_length=25)
    expiry_date = form_text_field(forms.CharField, widget=forms.TextInput, placeholder='Card expiry date e.g. 02/24', max_length=5)
    cvv = form_text_field(forms.CharField, widget=forms.NumberInput, placeholder='CVV e.g. 123', max_length=3)
    
    def clean(self):
        cleaned_data =  super().clean()
        
        current_date = datetime.now()
        current_month = current_date.month
        # Get the last two digits of the current year
        current_year = current_date.year % 100
        
        
        if not re.match(r"^(0[1-9]|1[0-2])\/(2[0-9])$", cleaned_data.get('expiry_date')):
            raise forms.ValidationError('Enter a valid expiry date. It must be in this pattern 02/24 or 11/24')
        else:
            user_entered_date = cleaned_data.get('expiry_date')
            # Convert user entered date to a list
            user_date_list = user_entered_date.split('/')
            
            # Check if date is in the past
            if int(user_date_list[1]) < current_year:
                raise forms.ValidationError('Date cannot be in the past')
            elif (int(user_date_list[1]) == current_year) and (int(user_date_list[0]) < current_month):
                raise forms.ValidationError('Date cannot be in the past')
        
        if not re.match(r"^\d+$", cleaned_data.get('card_number')):
            raise forms.ValidationError('Enter a valid card number')
            
        return cleaned_data

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
    
    