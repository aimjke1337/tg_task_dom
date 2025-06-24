from django.contrib import admin
from .models import Service, ServiceRequest


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "price")


@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ("service", "full_name", "status", "executor", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("full_name", "address", "phone")
