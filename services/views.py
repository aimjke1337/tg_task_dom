from django.shortcuts import render
from django.db.models import Count

from .models import Request


def dashboard(request):
    stats = Request.objects.values("status").annotate(total=Count("id"))
    return render(request, "services/dashboard.html", {"stats": stats})
