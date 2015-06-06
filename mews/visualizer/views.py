from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Article, Location, TopStories
import getNewsNYT as NYTNews
import articleFilter as aFilter

# Create your views here.
def index(request):
    articles = Article.objects.all()
    locations = Location.objects.all()
    numArticles = len(articles)
    context = {'articles': articles, 'locations': locations, 'numArticles': numArticles}

    return render(request, 'visualizer/index.html', context)

def collect_articles(request):
    locations = Location.objects.all()
    topArticles = NYTNews.getTopNYT()
    mostViewedArticlesAll = NYTNews.getMostViewedNYT('all-sections', 3)
    mostViewedArticlesWorld = NYTNews.getMostViewedNYT('world', 3)
    onlineArticles = topArticles + mostViewedArticlesAll + mostViewedArticlesWorld
    mostViewedTop = NYTNews.getMostViewedNYT('world', 1)
    mapTopStories = topArticles + mostViewedTop
    newArticles = []
    oldArticles = []
    newTopStories = []

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

    articles = Article.objects.order_by('-id')
    numArticles = len(articles)

    context = {'articles': articles, 'newArticles': newArticles, 'oldArticles': oldArticles, 'locations': locations, 'numArticles': numArticles}
    return render(request, 'visualizer/collect.html', context)

def remove_dups(request):
    for row in Article.objects.all():
        if Article.objects.filter(url=row.url).count() > 1:
            row.delete()

    return redirect('collect_articles')



def map(request):
    articles = Article.objects.all()
    locations = Location.objects.all()
    numArticles = len(articles)
    context = {'articles': articles, 'locations': locations, 'numArticles': numArticles}


    return render(request, 'visualizer/map.html', context)

def mapWithFilters(request):
    mostViewedArticles = Article.objects.all()
    articlesBySection = aFilter.filterBySection(mostViewedArticles)
    articlesByDate = aFilter.filterByDate(mostViewedArticles)
    context = {'articlesBySection': articlesBySection, 'articlesByDate': articlesByDate}

    return render(request, 'visualizer/mapwithfilters.html', context)

def mapTopStories(request):
    articles = TopStories.objects.all()
    context = {'articles': articles}

    return render(request, 'visualizer/maptopstories.html', context)
