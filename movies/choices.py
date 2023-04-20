from django.db import models
from django.utils.translation import gettext_lazy as _


class TypeFilmWork(models.TextChoices):
    MOVIE       = 'movie', _('movie')
    TV_SHOW     = 'tv_show', _('tv_show')


class Gender(models.TextChoices):
    MALE        = 'male', _('male')
    FEMALE      = 'female', _('female')


class ProfessionType(models.TextChoices):
    ACTOR       = 'actor', _('actor')
    WRITER      = 'writer', _('writer')
    DIRECTOR    = 'director', _('director')
