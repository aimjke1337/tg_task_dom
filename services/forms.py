from django import forms
from .models import ServiceRequest


class ServiceRequestForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ["service", "full_name", "address", "phone", "extra_data"]
