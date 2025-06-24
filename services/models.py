from django.db import models


class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return self.name


class ServiceRequest(models.Model):
    class Status(models.TextChoices):
        NEW = "NEW", "New"
        IN_PROGRESS = "IN_PROGRESS", "In progress"
        DONE = "DONE", "Done"

    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="requests")
    full_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    extra_data = models.JSONField(blank=True, null=True)
    executor = models.ForeignKey(
        "auth.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="service_requests",
    )
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.service.name} ({self.full_name})"
