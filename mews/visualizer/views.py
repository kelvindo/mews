from django.shortcuts import render
from django.http import HttpResponse
from .models import Article, Location
import getNewsNYT as NYTNews
import articleFilter as aFilter

# Create your views here.
def index(request):
    locations = Location.objects.all()
    articles = NYTNews.getTopNYT()
    context = {'articles': articles, 'locations': locations}

    return render(request, 'visualizer/index.html', context)

def map(request):
    locations = Location.objects.all()
    topArticles = NYTNews.getTopNYT()
    mostViewedArticlesAll = NYTNews.getMostViewedNYT('all-sections', 1)
    mostViewedArticlesWorld = NYTNews.getMostViewedNYT('world', 1)
    articles = topArticles + mostViewedArticlesAll + mostViewedArticlesWorld
    context = {'articles': articles, 'locations': locations}

    return render(request, 'visualizer/map.html', context)

def mapWithFilters(request):
    topArticles = NYTNews.getTopNYT()
    mostViewedArticles = NYTNews.getMostViewedNYT('all-sections', 1)
    articlesBySection = aFilter.filterBySection(topArticles)
    articlesByDate = aFilter.filterByDate(mostViewedArticles)
    context = {'articlesBySection': articlesBySection, 'articlesByDate': articlesByDate}

    return render(request, 'visualizer/mapwithfilters.html', context)

def mapTopStories(request):
    topArticles = NYTNews.getTopNYT()
    mostViewedArticlesWorld = NYTNews.getMostViewedNYT('world', 1)
    articles = topArticles + mostViewedArticlesWorld
    context = {'articles': articles}

    return render(request, 'visualizer/maptopstories.html', context)