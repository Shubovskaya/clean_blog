from rest_framework.serializers import ModelSerializer

from blog.models import Post
from slugify import slugify


class PostSerializer(ModelSerializer):

    def create(self, validated_data):
        post = Post(**validated_data | {'slug': slugify(validated_data.get('title') + validated_data.get('subtitle'))})
        post.save()
        return post

    class Meta:
        model = Post
        fields = ('id', 'title', 'subtitle', 'text', 'author', 'image')

