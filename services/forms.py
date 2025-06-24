from django import forms
from .models import Request


class ServiceRequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ["service", "client", "data", "status"]
