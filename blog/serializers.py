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
        fields = ('id', 'blog', 'description', 'date_created')


class CommentListSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    def get_full_name(self, obj):
        return obj.user.full_name

    class Meta:
        model = Comment
        fields = ('id', 'full_name', 'description', 'date_created')
