from django.db import models


class MimeType(models.TextChoices):
    TEXT_HTML = "text/html"
    TEXT_PLAIN = "text/plain"


class Status(models.TextChoices):
    IN_PROGRESS = "in_progress"
    PENDING = "pending"


class Event(models.TextChoices):
    REGISTERED = "registered"


class NotificationChannels(models.TextChoices):
    EMAIL = "email"
