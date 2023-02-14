from django.urls import path

from blog.views import BlogCategoryListAPIView, BlogCategoryRetrieveAPIView, BlogListAPIView, BlogRetrieveAPIView, \
    CommentCreateAPIView, CommentListAPIView, CommentRetrieveAPIView, BlogCategoryDestroyAPIview, \
    BlogCategoryCreateAPIview, BlogCreateAPIView, BlogDestroyAPIView

urlpatterns = [
    # category
    path('category/', BlogCategoryListAPIView.as_view()),
    path('category/<int:pk>/', BlogCategoryRetrieveAPIView.as_view()),
    path('category/create/', BlogCategoryCreateAPIview.as_view()),
    path('category/delete/<int:pk>/', BlogCategoryDestroyAPIview.as_view()),

    # blog
    path('list/', BlogListAPIView.as_view()),
    path('create/', BlogCreateAPIView.as_view()),
    path('destroy/<int:pk>/', BlogDestroyAPIView.as_view()),
    path('retrieve/<int:pk>/', BlogRetrieveAPIView.as_view()),

    # comment
    path('comment/post/', CommentCreateAPIView.as_view()),
    path('comment/list/', CommentListAPIView.as_view()),
    path('comment/list/<int:pk>/', CommentRetrieveAPIView.as_view()),

]
