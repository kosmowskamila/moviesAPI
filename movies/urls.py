from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from movie.views import MovieViewSet, TopMoviesViewSet
from comment.views import CommentViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'top', TopMoviesViewSet, base_name='top')
router.register(r'movies', MovieViewSet, base_name='movies')
router.register(r'comments', CommentViewSet, base_name='comments')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]
