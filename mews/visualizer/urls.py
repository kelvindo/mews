from django.conf.urls import url

from . import views

urlpatterns = [
    #/ - landing page. currently displays list of articles
    url(r'^$', views.index, name='index'),

    #/collect_articles - collect articles
    url(r'^collect_articles$', views.collect_articles, name='collect_articles'),

    #/remove_dups - removes duplicate articles
    url(r'^remove_dups$', views.remove_dups, name='remove_dups'),

    #/map - shows the map
    url(r'^map$', views.map, name='map'),

    #/mapbysection - lists articles by section
    url(r'^mapwithfilters$', views.mapWithFilters, name='mapwithfilters'),

    #/maptopstories - bubbles by popularity
    url(r'^maptopstories$', views.mapTopStories, name='maptopstories')
    ]