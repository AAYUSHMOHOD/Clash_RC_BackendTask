from django.db import models

class User(models.Model):
    Name = models.CharField(max_length=50)
    Mobile = models.CharField(max_length=10)
    Email = models.CharField(max_length=50)
    Password = models.CharField(max_length=50)