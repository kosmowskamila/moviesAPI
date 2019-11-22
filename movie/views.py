from rest_framework import viewsets, generics
from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter

from movie.models import Movie
from movie.serializers import MovieSerializer


class MovieFilterSet(filters.FilterSet):
    min_year = filters.NumberFilter(field_name='year', lookup_expr='gte')
    max_year = filters.NumberFilter(field_name='year', lookup_expr='lte')
    genre = filters.CharFilter(lookup_expr='contains')
    actor = filters.CharFilter(field_name='actors', lookup_expr='contains')
    director = filters.CharFilter(lookup_expr='contains')
    writer = filters.CharFilter(lookup_expr='contains')
    language = filters.CharFilter(lookup_expr='contains')
    country = filters.CharFilter(lookup_expr='contains')
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


class TopMovies(generics.ListAPIView):
    queryset = Movie.objects.all()
