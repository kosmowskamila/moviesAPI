from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=50)
    year = models.IntegerField(blank=True, null=True)
    rated = models.CharField(max_length=5, blank=True, null=True)
    released = models.DateField(blank=True, null=True)
    runtime = models.CharField(max_length=10, blank=True, null=True)
    genre = models.CharField(max_length=200, blank=True, null=True)
    director = models.CharField(max_length=100, blank=True, null=True)
    writer = models.TextField(blank=True, null=True)
    actors = models.TextField(blank=True, null=True)
    plot = models.TextField(blank=True, null=True)
    language = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=20, blank=True, null=True)
    awards = models.TextField(blank=True, null=True)
    poster = models.CharField(max_length=200, blank=True, null=True)
    metascore = models.CharField(max_length=50, blank=True, null=True)
    imdb_rating = models.FloatField(blank=True, null=True)
    imdb_votes = models.IntegerField(blank=True, null=True)
    imdb_id = models.CharField(max_length=15, blank=True, null=True)
    type = models.CharField(max_length=10, blank=True, null=True)
    dvd = models.DateField(blank=True, null=True)
    box_office = models.CharField(max_length=100, blank=True, null=True)
    production = models.CharField(max_length=200, blank=True, null=True)
    website = models.CharField(max_length=300, blank=True, null=True)


class Rating(models.Model):
    source = models.CharField(max_length=100)
    value = models.CharField(max_length=10)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='ratings')
