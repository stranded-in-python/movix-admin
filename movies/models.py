from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from .choices import TypeFilmWork, Gender, ProfessionType
from .mixins import TimeStampedMixin, UUIDMixin


class Genre(TimeStampedMixin, UUIDMixin):
    name        = models.CharField(verbose_name=_('name'),
                                   max_length=255,
                                   )
    description = models.TextField(verbose_name=_('description'),
                                   blank=True,
                                   null=True,
                                   )

    class Meta:
        db_table = "content\".\"genre"
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')
        indexes = [
            models.Index(fields=['id', ], name='genre_idx'),
            models.Index(fields=['name', 'id', ], name='name_genre_idx'),
        ]
        constraints = [
            models.UniqueConstraint(fields=['name', ],
                                    name="unique-genre-name",
                                    )
        ]

    def __str__(self):
        return str(self.name)


class Person(TimeStampedMixin, UUIDMixin):
    full_name   = models.CharField(verbose_name=_('full_name'),
                                   max_length=255,
                                   )
    gender      = models.TextField(_('gender'),
                                   choices=Gender.choices,
                                   null=True,
                                   )

    class Meta:
        db_table = "content\".\"person"
        verbose_name = _('Person')
        verbose_name_plural = _('People')
        indexes = [
            models.Index(fields=['id'], name='person_idx'),
            models.Index(fields=['full_name', 'id'],
                         name='full_name_person_idx'),
        ]

    def __str__(self):
        return str(self.full_name)


class Filmwork(TimeStampedMixin, UUIDMixin):
    title           = models.TextField('title',)
    description     = models.TextField(verbose_name=_('description'), null=True,)
    creation_date   = models.DateField(verbose_name=_('creation_date'), null=True,)
    rating          = models.FloatField(verbose_name=_('rating'),
                                        null=True,
                                        blank=True,
                                        validators=[MinValueValidator(0),
                                                    MaxValueValidator(100)],
                                        )
    type            = models.TextField(verbose_name=_('type'),
                                       choices=TypeFilmWork.choices,
                                       )
    certificate     = models.CharField(_('certificate'),
                                       max_length=512,
                                       blank=True,
                                       null=True,
                                       )
    file_path       = models.FileField(_('file'),
                                       blank=True,
                                       null=True,
                                       upload_to='movies/',
                                       )
    genres          = models.ManyToManyField(to=Genre,
                                             through='GenreFilmwork',
                                             )
    persons         = models.ManyToManyField(to=Person,
                                             through='PersonFilmwork',
                                             )

    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = _('Filmwork')
        verbose_name_plural = _('Filmworks')
        indexes = [
            models.Index(fields=['id',],
                         name='film_work_idx'),
            models.Index(fields=['title', 'id',],
                         name='title_film_work_idx',),
            models.Index(fields=['creation_date', 'id',],
                         name='creation_date_film_work_idx'),
            models.Index(fields=['rating', 'id'],
                         name='rating_film_work_idx'),
            models.Index(fields=['type', 'id'],
                         name='type_film_work_idx'),                         
        ]

    def __str__(self):
        return str(self.title)


class GenreFilmwork(UUIDMixin):
    film_work   = models.ForeignKey(to=Filmwork,
                                    on_delete=models.CASCADE,
                                    )
    genre       = models.ForeignKey(to=Genre,
                                    on_delete=models.CASCADE,
                                    )
    created     = models.DateTimeField(auto_now_add=True,)

    class Meta:
        db_table = "content\".\"genre_film_work"
        indexes = [
            models.Index(fields=['film_work', 'genre_id'],
                         name='film_work_genre_idx'),
            models.Index(fields=['genre_id', 'film_work'], 
                         name='genre_film_work_idx'),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['film_work', 'genre',],
                name='unique-GenreFilmwork-filmwork-genre')
        ]


class PersonFilmwork(UUIDMixin):
    film_work   = models.ForeignKey(to=Filmwork,
                                    on_delete=models.CASCADE,
                                    )
    person      = models.ForeignKey(to=Person,
                                    on_delete=models.CASCADE,)
    # В БД источинке в поле "роль" хранятся значения профессии.
    # А понятие роль используется для актёров. Поэтому добавил
    # поле 'profession' с выбором значений 
    role        = models.TextField(verbose_name=_('role'),
                                   null=True,
                                   )
    profession  = models.TextField(_('profession'),
                                   choices=ProfessionType.choices,
                                   null=True,
                                   )
    created     = models.DateTimeField(auto_now_add=True,)

    class Meta:
        db_table = "content\".\"person_film_work"
        indexes = [
            models.Index(fields=['person', 'film_work'],
                         name='person_film_work_idx'),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['film_work', 'person', 'profession'],
                name='unique-PersonFilmwork-filmwork-person')
        ]
