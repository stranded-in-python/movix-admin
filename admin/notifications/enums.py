from django.db import models
from django.utils.translation import gettext_lazy as _


class MimeType(models.TextChoices):
    TEXT_HTML = "text/html", _("HTML")
    TEXT_PLAIN = "text/plain", _("Text")


class Status(models.TextChoices):
    STALE = "stale", _("To be deleted")
    PENDING = "pending", _("Pending")


class Event(models.TextChoices):
    REGISTERED = "registered", _("Registered")


class NotificationChannels(models.TextChoices):
    EMAIL = "email", _("Email")


class ContextVariables(models.TextChoices):
    FIRST_NAME = "first_name", _("First name")
    LAST_NAME = "last_name", _("Last name")
    EMAIL = "email", _("Email")
    USERNAME = "username", _("Username")
