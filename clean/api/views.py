from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from blog.models import Post
from .serializers import PostSerializer

class PostViewSet(ModelViewSet):
    queryset = Post.objects.filter(is_published=True)
    serializer_class = PostSerializer


