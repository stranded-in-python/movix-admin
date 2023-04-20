import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _


# Mixins
class TimeStampedMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


# Main
class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_('name'), max_length=255, null=True)
    description = models.TextField(_('description'), blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "content\".\"genre"
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')


class Filmwork(UUIDMixin, TimeStampedMixin):
    title = models.CharField(_('title'), max_length=255, null=True)
    description = models.TextField(_('description'), max_length=255, null=True)
    creation_date = models.DateTimeField(_('creation date'), null=True)
    rating = models.FloatField(_('rating'), validators=[MinValueValidator(0), MaxValueValidator(100)], null=True)
    type = models.CharField(_('type'), max_length=30, choices=(
        ('tv_show', _('tv_show')), ('movie', _('movie'))), null=True)
    file_path = models.CharField(_('file_path'), max_length=255, null=True)
    
    def __str__(self):
        return self.title 
    
    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = _('FilmWork')
        verbose_name_plural = _('FilmWorks')


class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey(Filmwork, on_delete=models.CASCADE, verbose_name=_('film work'), null=True)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, verbose_name=_('genre'), null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = "content\".\"genre_film_work"
        verbose_name = _('GenreFilmWork')
        verbose_name_plural = _('GenreFilmWorks')
        indexes = [
            models.Index(fields=['film_work_id', 'genre_id'], name='film_work_genre'),
        ]
        constraints = [
            models.UniqueConstraint(fields=['film_work_id', 'genre_id'], name='film_work_genre_unique')
        ]

class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField(_('Full Name'), max_length=255, null=True)
    
    class Meta:
        db_table = "content\".\"person"
        verbose_name = _('Person')
        verbose_name_plural = _('Persons')

    def __str__(self):
        return self.full_name


class PersonFilmwork(UUIDMixin):
    film_work = models.ForeignKey(Filmwork, on_delete=models.CASCADE, verbose_name=_('film work'), null=True)
    person = models.ForeignKey(Person, on_delete=models.CASCADE, verbose_name=_('person'), null=True)
    role = models.CharField(_('role'), null=True, choices=(
        ('actor', _('actor')), ('writer', _('writer')), ('director', _('director'))
    ), max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    
    class Meta:
        db_table = "content\".\"person_film_work"
        verbose_name = _('Person/Filmwork')
        verbose_name_plural = _('Persons/Filmworks')
        indexes = [
            models.Index(fields=['film_work_id', 'person_id', 'role'], name='film_work_person_role')
        ]
        constraints= [
            models.UniqueConstraint(fields=['film_work_id', 'person_id', 'role'], name='film_work_person_role_unique')
        ]

    def __str__(self):
        return self.role
