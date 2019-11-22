from rest_framework import viewsets
from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter
from django.db.models import F, Q, Count
from django.db.models.expressions import Window
from django.db.models.functions import DenseRank
from django.core.exceptions import ValidationError

from movie.models import Movie
from movie.serializers import MovieSerializer, TopMoviesSerializer


class MovieFilterSet(filters.FilterSet):
    min_year = filters.NumberFilter(field_name='year', lookup_expr='gte')
    max_year = filters.NumberFilter(field_name='year', lookup_expr='lte')
    genre = filters.CharFilter(lookup_expr='icontains')
    actor = filters.CharFilter(field_name='actors', lookup_expr='icontains')
    director = filters.CharFilter(lookup_expr='icontains')
    writer = filters.CharFilter(lookup_expr='icontains')
    language = filters.CharFilter(lookup_expr='icontains')
    country = filters.CharFilter(lookup_expr='icontains')
    min_imdb_rating = filters.CharFilter(field_name='imdb_rating',
                                         lookup_expr='gte')
    max_imdb_rating = filters.CharFilter(field_name='imdb_rating',
                                         lookup_expr='lte')

    class Meta:
        model = Movie
        fields = ['year', 'min_year', 'max_year', 'rated', 'genre', 'actor',
                  'director', 'writer', 'language', 'country', 'min_imdb_rating',
                  'max_imdb_rating', 'title', 'id']


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    ordering_fields = ['year', 'title', 'imdb_rating']
    filter_class = MovieFilterSet


class TopMoviesViewSet(viewsets.ReadOnlyModelViewSet):
    """
    View returning info about the most commented movies in specified
    date range. Parameters "start" and "end" are obligatory to receive
    any data!
    """
    queryset = Movie.objects.all()
    serializer_class = TopMoviesSerializer

    def get_queryset(self):
        start = self.request.query_params.get('start', None)
        end = self.request.query_params.get('end', None)
        if start and end:
            qs = super().get_queryset()
            return qs.annotate(
                total_comments=Count('comments', filter=Q(
                    comments__created__range=[start, end])),
                rank=Window(expression=DenseRank(),
                            order_by=F('total_comments').desc()
                            )
            )
        else:
            raise ValidationError('Please, provide start and end dates.')

