# from django.db.models import Q
from rest_framework import generics, status
# from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response

from blog.models import Blog, BlogCategory, Comment
from account.permissions import IsAuthenticated
from .serializers import BlogSerializer, BlogCategorySerializer, CommentCreateSerializer, CommentListSerializer


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


class BlogCreateAPIView(generics.CreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = (IsAuthenticated,)


class BlogDestroyAPIView(generics.DestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = (IsAuthenticated,)


class BlogListAPIView(generics.ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer


class BlogRetrieveAPIView(generics.RetrieveUpdateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    lookup_field = 'slug'


class CommentCreateAPIView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = CommentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)


class CommentListAPIView(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentListSerializer
    # search_fields = ['name']
    # filter_backends = [SearchFilter, OrderingFilter]
    #
    # def get_queryset(self, *args, **kwargs):
    #     queryset_list = Comment.objects.all()
    #     query = self.request.GET.get('q')
    #     if query:
    #         queryset_list = queryset_list.filter(
    #             Q(name_icontains=query)
    #         )
    #     return queryset_list


class CommentRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentListSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'pk'
