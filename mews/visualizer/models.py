from django.db import models

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=200)
    URL = models.URLField(max_length=200)
    abstract = models.TextField()

class Location(models.Model):
    query = models.CharField(max_length=200)
    lng = models.FloatField()
    lat = models.FloatField()
    name = models.CharField(max_length=200)
    is_valid = models.BooleanField()