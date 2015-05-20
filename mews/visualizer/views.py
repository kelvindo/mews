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

def collect_articles(request):
    locations = Location.objects.all()
    topArticles = NYTNews.getTopNYT()
    mostViewedArticlesAll = NYTNews.getMostViewedNYT('all-sections', 3)
    mostViewedArticlesWorld = NYTNews.getMostViewedNYT('world', 10)
    onlineArticles = topArticles + mostViewedArticlesAll + mostViewedArticlesWorld
    newArticles = []
    oldArticles = []

    for article in onlineArticles:
        existingArticle = Article.objects.filter(url=article['url'])
        if existingArticle:
            oldArticles.append(article)
        else:
            newArticles.append(article)
            #TODO: Put in real location
            exampleLocation = Location.objects.get(id=1)
            newArticle = Article(title=article['title'], 
                                 url=article['url'], 
                                 date_published=article['date_published'], 
                                 section=article['section'], 
                                 source=article['source'], 
                                 abstract=article['abstract'], 
                                 location=article['location'])
            newArticle.save()

    articles = Article.objects.all()

    context = {'articles': articles, 'newArticles': newArticles, 'oldArticles': oldArticles, 'locations': locations}
    return render(request, 'visualizer/collect.html', context)

def map(request):
    # topArticles = NYTNews.getTopNYT()
    # mostViewedArticlesAll = NYTNews.getMostViewedNYT('all-sections', 1)
    # mostViewedArticlesWorld = NYTNews.getMostViewedNYT('world', 1)
    # articles = topArticles + mostViewedArticlesAll + mostViewedArticlesWorld
    articles = Article.objects.all()
    locations = Location.objects.all()
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
