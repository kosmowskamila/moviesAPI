from rest_framework import serializers
from movie.models import Movie, Rating
from omdb import OMDBClient
from django.conf import settings
import datetime


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'


class MovieSerializer(serializers.ModelSerializer):
    ratings = RatingSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = ['id', 'title', 'year', 'rated', 'released', 'runtime',
                  'genre', 'director', 'writer', 'actors', 'plot', 'language',
                  'country', 'awards', 'poster', 'metascore',
                  'imdb_rating', 'imdb_votes', 'imdb_id', 'type',
                  'dvd', 'box_office', 'production', 'website', 'ratings']

    def create(self, validated_data):
        client = OMDBClient(apikey=settings.API_KEY)
        title = validated_data.get('title', None)
        if title:
            fetched_data = client.get(title=title)

            if not fetched_data:
                raise serializers.ValidationError('Invalid title.')

            if fetched_data['type'] != 'movie':
                raise serializers.ValidationError('Only movies avaliable.')

            fetched_data.pop('response')
            ratings = fetched_data.pop('ratings')

            released = fetched_data.pop('released')
            released_date = datetime.datetime.strptime(released, '%d %b %Y').date()

            dvd = fetched_data.pop('dvd')
            dvd_date = datetime.datetime.strptime(dvd, '%d %b %Y').date()

            imdb_votes = fetched_data.pop('imdb_votes')

            movie = Movie.objects.create(**fetched_data,
                                         released=released_date,
                                         dvd=dvd_date,
                                         imdb_votes=imdb_votes.replace(',', ''))

            for rating in ratings:
                Rating.objects.create(**rating, movie=movie)

            return movie
        else:
            raise serializers.ValidationError('Invalid request data!')
