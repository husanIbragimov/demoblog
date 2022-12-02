from django.contrib import admin
from .models import Comment, Blog, BlogCategory


admin.site.register(Blog)
admin.site.register(Comment)
admin.site.register(BlogCategory)
