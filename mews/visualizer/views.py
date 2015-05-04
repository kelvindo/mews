from django.shortcuts import render
from django.http import HttpResponse
from .models import Article, Location
import getNewsNYT as NYTNews

# Create your views here.
def index(request):

    locations = Location.objects.all()
    print locations
    articles = NYTNews.getTopStoriesNYT()
    context = {'articles': articles, 'locations': locations}

    return render(request, 'visualizer/index.html', context)
