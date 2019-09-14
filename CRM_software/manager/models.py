from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100, blank=True)
    price =models.CharField(max_length=100, blank=True)
    description = models.CharField(max_length=1000, blank=True)


