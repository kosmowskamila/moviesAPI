from django.contrib import admin
from movie.models import Movie, Rating


class RatingInline(admin.TabularInline):
    model = Rating
    fk_name = 'movie'


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'year', 'genre')
    inlines = [RatingInline]
