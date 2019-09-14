from django.db import models
from manager.models import Product
from django.contrib.auth.models import User
# Create your models here.


class employee_customer(models.Model):
    e = models.ForeignKey(User, on_delete = models.CASCADE)
    c_name = models.CharField(max_length = 100)
    product = models.ForeignKey(Product, on_delete = models.CASCADE,default='-1')
    r_date = models.DateField(null = False, blank=False, auto_now = True)
