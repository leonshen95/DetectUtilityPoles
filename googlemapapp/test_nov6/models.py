from django.db import models


# Create your models here.
class Users(models.Model):
    username = models.CharField(primary_key=True,max_length=12)
    password = models.CharField(max_length=12)
    email = models.CharField(max_length=254)
    def __str__(self):
        return self.username

class Locations(models.Model):
    time = models.CharField(primary_key=True,max_length=64)
    lat = models.CharField(max_length=24)
    lng = models.CharField(max_length=24)
    def __str__(self):
        return self.time
'''
class 
'''