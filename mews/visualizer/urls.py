from django.conf.urls import url

from . import views

urlpatterns = [
    #/ - landing page. currently displays list of articles
    url(r'^$', views.index, name='index'),

    #/map - shows the map
    url(r'^map$', views.map, name='map'),

    #/mapbysection - lists articles by section
    url(r'^mapwithfilters$', views.mapWithFilters, name='mapwithfilters')
    ]