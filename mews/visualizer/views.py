from django.shortcuts import render
from django.http import HttpResponse
from .models import Article, Location
import getNewsNYT as NYTNews

# Create your views here.
def index(request):
    locations = Location.objects.all()
    topArticles = NYTNews.getTopNYT()
    mostViewedArticles = NYTNews.getMostPopularViewedNYT()
    context = {'topArticles': topArticles, 'mostViewedArticles': mostViewedArticles, 'locations': locations}

    return render(request, 'visualizer/index.html', context)

def map(request):
    locations = Location.objects.all()
    topArticles = NYTNews.getTopNYT()
    mostViewedArticlesAll = NYTNews.getMostViewedNYT('all-sections', 1)
    mostViewedArticlesWorld = NYTNews.getMostViewedNYT('world', 1)
    articles = topArticles + mostViewedArticlesAll + mostViewedArticlesWorld
    context = {'articles': articles, 'locations': locations}

    return render(request, 'visualizer/map.html', context)