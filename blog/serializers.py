from rest_framework import serializers

from account.serializers import AccountSerializer
from blog.models import Blog, Comment, BlogCategory


class BlogCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = ('id', 'title')


class BlogSerializer(serializers.ModelSerializer):
    owner = AccountSerializer(read_only=True)

    class Meta:
        model = Blog
        fields = ('id', 'title', 'category', 'image', 'description', 'date_created', 'owner')


class BlogCreateSerializer(serializers.ModelSerializer):
    owner = AccountSerializer(read_only=True)

    class Meta:
        model = Blog
        fields = ('id', 'title', 'category', 'image', 'description', 'date_created', 'owner')


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'blog', 'description', 'date_created')


class CommentListSerializer(serializers.ModelSerializer):
    user = AccountSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'user', 'description', 'date_created')
