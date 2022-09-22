from django.db import models
from django.contrib.auth.models import User, AbstractUser


# Create your models here.
class User(AbstractUser):
    image = models.ImageField(upload_to='user_photo/', blank=True)

    def __str__(self):
        return self.username

class Categories(models.Model):
    url = models.TextField()
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title

class Product(models.Model):
    categorie = models.ForeignKey(Categories, on_delete=models.CASCADE, null=True)
    photo = models.ImageField(upload_to='product_photo/')
    name = models.CharField(max_length=200)
    price = models.FloatField(default=0)
    description = models.TextField()

    def __str__(self):
        return self.name


class Busket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)