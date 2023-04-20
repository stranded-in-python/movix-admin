from django.contrib import admin
from .models import (
    Genre, Filmwork, Person, GenreFilmwork, PersonFilmwork
)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'created',
        'modified',
    )
    search_fields = (
        'name',
    )


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = (
        'full_name',
        'created',
        'modified',
    )
    list_filter  = ('gender',)
    search_fields = (
        'full_name',
    )


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork
    autocomplete_fields = ('genre',) 


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork
    autocomplete_fields = ('person',) 


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmworkInline,
               PersonFilmworkInline,)
    list_display = ('title',
                    'type',
                    'get_genres',
                    'creation_date',
                    'rating',
                    'created',
                    'modified',
                    )
    list_prefetch_related = ('genres',)
    list_filter  = ('type',)
    search_fields = ('title',
                     'description',
                     'id',
                     )

    def get_queryset(self, request):
        queryset = (super()
                    .get_queryset(request)
                    .prefetch_related(*self.list_prefetch_related)
        )
        return queryset

    def get_genres(self, obj):
        return ', '.join([genre.name for genre in obj.genres.all()])

    get_genres.short_description = 'Жанры фильма'
