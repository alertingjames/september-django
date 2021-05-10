from django.db import models

# Create your models here.

class Member(models.Model):
    name=models.CharField(max_length=50)
    email = models.CharField(max_length=80)
    password = models.CharField(max_length=30)
    photo_url = models.CharField(max_length=500)
    phone_number = models.CharField(max_length=50)

class Product(models.Model):
    user_id = models.CharField(max_length=11)
    title=models.CharField(max_length=50)
    brand = models.CharField(max_length=50)
    image_url = models.CharField(max_length=500)
    gender = models.CharField(max_length=20)
    price = models.CharField(max_length=10)
    category = models.CharField(max_length=20)
    sale_url = models.CharField(max_length=500)
    keyword = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)