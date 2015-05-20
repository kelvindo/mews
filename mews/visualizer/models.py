from django.db import models

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField(max_length=200)
    date_published = models.DateField()
    section = models.CharField(max_length=200)
    source = models.CharField(max_length=200)
    abstract = models.TextField()
    location = models.ForeignKey('Location')

    def __str__(self):
        return self.title

class Location(models.Model):
    query = models.CharField(max_length=200)
    lng = models.FloatField()
    lat = models.FloatField()
    name = models.CharField(max_length=200)
    is_valid = models.BooleanField()