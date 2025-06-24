from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView
from services.models import Service, Request
from django.db.models import Count
from .forms import ServiceForm

@login_required
def dashboard(request):
    stats = Request.objects.values('status').annotate(count=Count('id'))
    return render(request, 'dashboard/dashboard.html', {'stats': stats})

class IsSuperUserMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser

class ServiceListView(LoginRequiredMixin, ListView):
    model = Service
    template_name = 'dashboard/services_list.html'

class ServiceCreateView(IsSuperUserMixin, CreateView):
    model = Service
    form_class = ServiceForm
    template_name = 'dashboard/service_form.html'
    success_url = reverse_lazy('services_list')

class ServiceUpdateView(IsSuperUserMixin, UpdateView):
    model = Service
    form_class = ServiceForm
    template_name = 'dashboard/service_form.html'
    success_url = reverse_lazy('services_list')

class RequestListView(LoginRequiredMixin, ListView):
    model = Request
    template_name = 'dashboard/requests_list.html'
    ordering = ['-created_at']
