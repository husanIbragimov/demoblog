from rest_framework import serializers

from account.serializers import AccountSerializer
from blog.models import Blog, Comment, BlogCategory


class BlogCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = ('id', 'title')


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ('id', 'title', 'category', 'image', 'description', 'date_created')


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'blog', 'user', 'description', 'date_created')


class CommentListSerializer(serializers.ModelSerializer):
    blog_id = serializers.IntegerField(source='blog.id', read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'blog_id', 'description', 'date_created')
