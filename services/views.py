from django.shortcuts import render
from django.db.models import Count

from .models import ServiceRequest


def dashboard(request):
    stats = ServiceRequest.objects.values("status").annotate(total=Count("id"))
    return render(request, "services/dashboard.html", {"stats": stats})
