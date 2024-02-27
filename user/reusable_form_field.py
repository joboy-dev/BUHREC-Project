from django import forms

def form_text_field(field, widget, placeholder, readonly=False, max_length=2000):
    '''Form text field '''
    
    return field(max_length=max_length, required=True, widget=widget(attrs={'placeholder': placeholder, 'readonly': readonly}))

def form_select_field(choices):
    '''Form select field '''
    
    return forms.CharField(max_length=200, required=True, widget=forms.Select(choices=choices))