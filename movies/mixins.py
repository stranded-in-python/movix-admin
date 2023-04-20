from uuid import uuid4

from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(verbose_name=_('created'),
                                   auto_now_add=True,
                                   )
    modified = models.DateTimeField(verbose_name=_('modified'),
                                    auto_now=True,
                                    )

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(verbose_name=_('id'),
                          primary_key=True,
                          default=uuid4,
                          editable=False,
                          )

    class Meta:
        abstract = True
