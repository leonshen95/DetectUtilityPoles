from django.db import models

# Create your models here.
class Coordinates(models.Model):
    longitude = models.CharField(max_length=32)
    latitude = models.CharField(max_length=32)
