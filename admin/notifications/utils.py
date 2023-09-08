from django.db import models


def template_path(instance: models.Model, filename: str) -> str:
    return f"templates/{instance.pk}"


def get_file_extension_by_mime_type(mime_type: str) -> str:
    return mime_type.split("/")[1]
