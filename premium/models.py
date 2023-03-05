from django.db import models
from ingredients.models import Category
from user.models import MyUser

# Create your models here.
class Premium(models.Model):
    name = models.CharField(max_length=100)
    notes = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE) 

    def __str__(self):
        return self.name