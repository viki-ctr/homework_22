from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    username = None  # Отключаем username
    email = models.EmailField('Email', unique=True)
    phone = models.CharField('Телефон', max_length=20, blank=True, null=True)
    country = models.CharField('Страна', max_length=100, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
