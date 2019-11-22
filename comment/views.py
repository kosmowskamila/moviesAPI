from rest_framework import viewsets
from django_filters import rest_framework as filters

from comment.models import Comment
from comment.serializers import CommentSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ['movie']
