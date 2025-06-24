from django import forms
from services.models import Service

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'description', 'price', 'form_schema']
        widgets = {
            'form_schema': forms.Textarea(attrs={'rows':4, 'cols':40}),
        }
