from django.contrib import admin
from comment.models import Comment


@admin.register(Comment)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('id', 'movie', 'created')