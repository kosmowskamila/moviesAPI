from django.db import models
from movie.models import Movie


class Comment(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True, editable=False)