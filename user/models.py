from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class MyUser(AbstractUser):
    username = models.CharField(max_length=50)
    email = models.EmailField(verbose_name='Email Adres', max_length=300, unique=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.username

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
