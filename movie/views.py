from datetime import datetime

from rest_framework import viewsets
from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter
from django.db.models import F, Q, Count
from django.db.models.expressions import Window
from django.db.models.functions import DenseRank

from movie.models import Movie
from movie.serializers import MovieSerializer, TopMoviesSerializer
from movie.exceptions import InvalidDateException, NoDateRangeException,\
    InvalidRangeException


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

    @staticmethod
    def validate_dates(start_string, end_string):
        """
        Method for date range validation. Checking whether correct dates have
        been submitted and if start date is smaller than end date.
        :param start_string: start date provided by the user
        :param end_string: end date provided by the user
        :raise: InvalidRangeException or InvalidDateException
        """
        try:
            start = datetime.strptime(start_string, '%Y-%m-%d')
            end = datetime.strptime(end_string, '%Y-%m-%d')
            if start > end:
                raise InvalidRangeException
        except ValueError:
            raise InvalidDateException

    def get_queryset(self):
        """
        Overriden get_queryset function, for two purporses:
        - validating date range
        - applying total_comment and rank info to queryset.
        :return:
        """
        start = self.request.query_params.get('start', None)
        end = self.request.query_params.get('end', None)

        if not start or not end:
            raise NoDateRangeException
        self.validate_dates(start, end)

        qs = super().get_queryset()
        return qs.annotate(total_comments=Count(
            'comments', filter=Q(comments__created__range=[start, end])),
            rank=Window(expression=DenseRank(),
                        order_by=F('total_comments').desc())
        )


