from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

# Create your models here.
class UserManager(BaseUserManager, models.Manager):
    def create_user(self, email, password, username, is_active=True, is_admin=False, is_staff=False, is_superuser=False):
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            is_active = is_active,
            is_admin = is_admin,
            is_staff = is_staff,
            is_superuser=is_superuser
        )
        user.set_password(password)
        user.save(using=self.db)
        return user 

    def create_superuser(self, email, password, is_active=True, is_admin=True, is_staff=True, is_superuser=True):
        user = self.model(
            email = self.normalize_email(email),
            is_active = is_active,
            is_admin = is_admin,
            is_staff = is_staff,
            is_superuser=is_superuser
        )
        user.set_password(password)
        user.save(using=self.db)
        return user 


class MyUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50)
    email = models.EmailField(verbose_name='Email Adres', max_length=300, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()
    
    def __str__(self):
        return self.username

    
