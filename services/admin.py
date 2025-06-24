from django.contrib import admin
from .models import Service, Request, Client


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "price")


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("full_name", "telegram_username")


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ("service", "client", "status", "executor", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("client__full_name",)
