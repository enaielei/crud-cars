from django.db import models

# Create your models here.
# class CarOrder(models.Model):
#     pass

class Car(models.Model):
    name = models.CharField(max_length=100, unique=True)
    color = models.CharField(max_length=20)
    order = models.IntegerField(default=0)