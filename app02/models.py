from django.db import models

# Create your models here.
class School(models.Model):
    title=models.CharField(max_length=64)
    detail=models.CharField(max_length=128)