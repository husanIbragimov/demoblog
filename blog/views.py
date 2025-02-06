from rest_framework import generics, status
from rest_framework.response import Response

from blog.models import Blog, BlogCategory, Comment
from account.permissions import IsAuthenticated
from .serializers import BlogSerializer, BlogCategorySerializer, CommentCreateSerializer, CommentListSerializer, \
    BlogCreateSerializer


class BlogCategoryCreateAPIview(generics.CreateAPIView):
    queryset = BlogCategory.objects.all()
    serializer_class = BlogCategorySerializer
    permission_classes = (IsAuthenticated,)


class BlogCategoryDestroyAPIview(generics.DestroyAPIView):
    queryset = BlogCategory.objects.all()
    serializer_class = BlogCategorySerializer
    permission_classes = (IsAuthenticated,)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()


class BlogCategoryListAPIView(generics.ListAPIView):
    queryset = BlogCategory.objects.filter(is_active=True).order_by('-id')
    serializer_class = BlogCategorySerializer


class BlogCategoryRetrieveAPIView(generics.RetrieveUpdateAPIView):
    queryset = BlogCategory.objects.all()
    serializer_class = BlogCategorySerializer
    permission_classes = (IsAuthenticated,)


class BlogCreateAPIView(generics.CreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogCreateSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(owner=user)


class BlogDestroyAPIView(generics.DestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = (IsAuthenticated,)


class BlogListAPIView(generics.ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

    def get_queryset(self):
        return Blog.objects.select_related('category', 'owner')


class BlogRetrieveAPIView(generics.RetrieveUpdateAPIView):
    queryset = Blog.objects.all().select_related('category', 'owner')
    serializer_class = BlogCreateSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'pk'


class CommentCreateAPIView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)


class CommentListAPIView(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentListSerializer

    def get_queryset(self, *args, **kwargs):
        blog_id = self.request.query_params.get('blog_id')
        if blog_id:
            queryset = Comment.objects.filter(blog_id=blog_id).select_related('user')
        else:
            queryset = Comment.objects.all().select_related('user')
        return queryset


class CommentRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Comment.objects.all().select_related("user")
    serializer_class = CommentListSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'pk'


class MyBlogsAPIView(generics.ListAPIView):
    serializer_class = BlogSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return Blog.objects.filter(owner=user).select_related('category', 'owner')
