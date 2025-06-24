from django.db import models
from django.conf import settings


class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    form_schema = models.JSONField(blank=True, null=True, default=dict)

    def __str__(self) -> str:
        return self.name


class Client(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    telegram_username = models.CharField(max_length=255, unique=True)
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.full_name


class Request(models.Model):
    class Status(models.TextChoices):
        NEW = "NEW", "new"
        IN_PROGRESS = "IN_PROGRESS", "in_progress"
        DONE = "DONE", "done"

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="requests")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="requests")
    data = models.JSONField(blank=True, null=True)
    executor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.service.name} ({self.client.full_name})"
