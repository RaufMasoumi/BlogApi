from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.


class Post(models.Model):
    STATUS_CHOICES = [
        ('p', 'Published'),
        ('d', 'Draft'),
    ]
    title = models.CharField(max_length=50)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=1, default='p')

    def __str__(self):
        return self.title

