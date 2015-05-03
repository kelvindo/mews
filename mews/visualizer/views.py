from django.shortcuts import render
from django.http import HttpResponse
from .models import Article

# Create your views here.
def index(request):
    articles = Article.objects.all()
    context = {'articles': articles}

    return render(request, 'visualizer/index.html', context)
