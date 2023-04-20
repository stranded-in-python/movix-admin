from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q, Count
from django.http import JsonResponse
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView

from movies.models import Filmwork
from movies.choices import ProfessionType

class MoviesApiMixin:
    model = Filmwork
    http_method_names = ['get']

    def get_queryset(self, **kwargs):
        return self.model.objects.filter(**kwargs)

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)


class MoviesListApi(MoviesApiMixin, BaseListView):
    model = Filmwork
    http_method_names = ['get']
    paginate_by = 50

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = self.get_queryset().prefetch_related(
            'genres', 'persons',
        ).values(
            'id', 'title', 'description',
            'creation_date', 'rating', 'type',
        ).annotate(
            genres=ArrayAgg('genres__name', distinct=True,),
            actors=ArrayAgg(
                'personfilmwork__person__full_name',
                filter=Q(personfilmwork__profession=ProfessionType.ACTOR),
                distinct=True,
            ),
            directors=ArrayAgg(
                'personfilmwork__person__full_name',
                filter=Q(personfilmwork__profession=ProfessionType.DIRECTOR),
                distinct=True,
            ),
            writers=ArrayAgg(
                'personfilmwork__person__full_name',
                filter=Q(personfilmwork__profession=ProfessionType.WRITER),
                distinct=True,
            ),
        )
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            queryset,
            self.paginate_by
        )
        context = {
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            'prev': page.previous_page_number() if page.has_previous() else None,
            'next': page.next_page_number() if page.has_next() else None,
            'results': list(queryset),
        }
        return context


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):
    def get_context_data(self, *, object_list=None, **kwargs):
        return self.get_queryset(id=self.kwargs['pk']).prefetch_related(
            'genres', 'persons',
        ).values(
            'id', 'title', 'description',
            'creation_date', 'rating', 'type',
        ).values(
            'id', 'title', 'description',
            'creation_date', 'rating', 'type',
        ).annotate(
            genres=ArrayAgg('genres__name', distinct=True, ),
            actors=ArrayAgg(
                'personfilmwork__person__full_name',
                filter=Q(personfilmwork__profession=ProfessionType.ACTOR),
                distinct=True,
            ),
            directors=ArrayAgg(
                'personfilmwork__person__full_name',
                filter=Q(personfilmwork__profession=ProfessionType.DIRECTOR),
                distinct=True,
            ),
            writers=ArrayAgg(
                'personfilmwork__person__full_name',
                filter=Q(personfilmwork__profession=ProfessionType.WRITER),
                distinct=True,
            ),
        )[0]

