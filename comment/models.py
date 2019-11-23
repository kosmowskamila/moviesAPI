from django.db import models
from movie.models import Movie


class Comment(models.Model):
    """
    Model storing single comment entry.
    Contains foreign key of movie that comment is about,
    text body of the comment and date of creation, that cannot be changed.
    """
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE,
                              related_name='comments')
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
