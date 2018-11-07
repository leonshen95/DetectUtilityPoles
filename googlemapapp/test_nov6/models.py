from django.db import models

# Create your models here.
class Users(models.Model):
    username = models.CharField(primary_key=True,max_length=12)
    password = models.CharField(null=False,max_length=12)
    def __str__(self):
        return self.username