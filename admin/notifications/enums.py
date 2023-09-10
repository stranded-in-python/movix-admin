from django.db import models
from django.utils.translation import gettext_lazy as _


class MimeType(models.TextChoices):
    TEXT_HTML = (_("HTML"), "text/html")
    TEXT_PLAIN = (_("Text"), "text/plain")


class Status(models.TextChoices):
    IN_PROGRESS = (_("In progress"), "in_progress")
    PENDING = (_("Pending"), "pending")


class Event(models.TextChoices):
    REGISTERED = (_("Registered"), "registered")


class NotificationChannels(models.TextChoices):
    EMAIL = (_("Email"), "email")


class ContextVariables(models.TextChoices):
    FIRST_NAME = (_("First name"), "first_name")
    LAST_NAME = (_("Last name"), "last_name")
    EMAIL = (_("Email"), "email")
    USERNAME = (_("Username"), "username")
