from django.db import models


class Contact(models.Model):
    title = models.CharField(max_length=221, null=True)
    phone_number = models.CharField(max_length=13, null=True)
    email = models.EmailField()
    description = models.TextField()
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

