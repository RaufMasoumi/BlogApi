from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class CustomUser(AbstractUser):
    slug = models.SlugField(max_length=150, unique=True)
    phone_number = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.username

    def get_safe_password(self):
        return '*' * len(self.password)


for user in CustomUser.objects.all():
    user.slug = user.username
    user.save()
