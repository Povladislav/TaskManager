from django.db import models
from rest_framework.exceptions import ValidationError

from authentication.models import User


class Task(models.Model):
    class Statuses(models.TextChoices):
        WAITING_FOR_WORKER = 'waiting_for_worker'
        PROCESSING = 'processing'
        DONE = 'done'

    status = models.CharField(max_length=20, choices=Statuses.choices, default=Statuses.WAITING_FOR_WORKER)
    client = models.ForeignKey(User, on_delete=models.PROTECT, related_name="client_tasks")
    text_of_task = models.CharField(max_length=50, null=True, blank=True)
    worker = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name="worker_tasks")
    report = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    closed_at = models.DateField(auto_now=True)

    def __str__(self):
        return f"Task#{self.pk}"

    def clean(self):
        if self.client.role != User.Roles.CUSTOMER:
            raise ValidationError('Invalid user for client field!')
        if self.worker and self.worker.role not in (User.Roles.WORKER, User.Roles.ADMIN_WORKER):
            raise ValidationError('Invalid user for worker field!')
