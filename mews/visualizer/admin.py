from django.contrib import admin
from .models import Article, Location, TopStories

admin.site.register(Article)
admin.site.register(Location)
admin.site.register(TopStories)