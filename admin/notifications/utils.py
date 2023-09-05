from django.db import models


def template_path(instance: models.Model, filename: str) -> str:
    return f"templates/{instance.pk}"
