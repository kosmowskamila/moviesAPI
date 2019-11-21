from rest_framework import serializers
from comment.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        queryset = Comment.objects.all()
        fields = ['__all__']
