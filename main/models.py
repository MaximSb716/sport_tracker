from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Voting(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    question = models.CharField(max_length=200)
    options = models.CharField(max_length=2000)
    votes = models.CharField(max_length=2000)