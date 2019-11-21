from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from movie.views import MovieViewSet
from comment.views import CommentViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'movies', MovieViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]
