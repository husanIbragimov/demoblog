from django.db import models

from django.urls import reverse


class BlogCategory(models.Model):
    title = models.CharField(max_length=221)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Blog(models.Model):
    title = models.CharField(max_length=221, null=True)
    slug = models.SlugField(null=True, blank=True, max_length=221)
    category = models.ForeignKey('BlogCategory', on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='blog/', null=True)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    date_created = models.DateField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('blog_detail', args=[self.slug])

    def __str__(self):
        return self.title


class Comment(models.Model):
    blog = models.ForeignKey('Blog', on_delete=models.CASCADE, null=True)
    user = models.ForeignKey('account.Account', on_delete=models.CASCADE, null=True)
    description = models.TextField()
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'comment of {self.blog}'

