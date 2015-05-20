import urllib
import requests
import json
from .models import Location, Article

##########################################################################
#                                                                        #
# getTopNYT(), getMostViewedNYT(section, times_to_iterate), and          #
# getByQueryNTY(query) should be the ONLY functions being called outside # 
# this file.                                                             #
#                                                                        #
# All functions return an array of articles, with each article being a   #
# dictionary with the following keys:                                    #
#    - title, url, date_published, section, source, abstract, location   #
#                                                                        #
# getTopNYT() fetches the articles from the front page of the NYTs       #
#                                                                        #
# getMostViewedNYT(section, times_to_iterate) has two parameters:        #
#    - section: string, only fetches articles with same section          #
#    - times_to_iterate: int, gets (20 * times_to_iterate) articles      #
#                                                                        #
# getByQueryNYT(query)                                                   #
#    - query: string over which to look for articles                     #
#                                                                        #
##########################################################################

def getByQueryNYT(query):
  url = 'http://api.nytimes.com/svc/search/v2/articlesearch.json?q=' + urllib.quote(query) + '&api-key=7bc9f44690147072ba0ddbc8aa8a92d0:1:72000218'
  data = requests.get(url).json()
  return getSearchArticlesNYT(data)

def getTopNYT():
  url = 'http://api.nytimes.com/svc/topstories/v1/home.json?api-key=903cc78251a8120cd1be50993e594000:12:72000218'
  data = requests.get(url).json()
  return getTopArticlesNYT(data)

def getTopArticlesNYT(data):
  num_results = data['num_results']
  results = data['results']
  articles = []
  for i in range(0, num_results):
    item = results[i]
    if item['item_type'] == "Article":
      article_data = getArticleInfoNYT(item)
      if article_data['location'] != None:
        articles.append(article_data)
  return articles

def getMostViewedNYT(section, times_to_iterate):
  articles = []
  url = 'http://api.nytimes.com/svc/mostpopular/v2/mostviewed/' + section + '/30.json?api-key=2cb1edcc1d8ca6933ff413e3fb574774:9:72000218'
  data = requests.get(url).json();
  num_results = data['num_results']
  times_to_iterate = getNumIterates(num_results, times_to_iterate)
  for i in range(0, times_to_iterate):
    results_on_page = 20
    is_last_run = (i == times_to_iterate - 1)
    if is_last_run:
      results_on_page = num_results - (20 * i)
      if results_on_page > 20:
        results_on_page = 20
    articles += getMostViewedArticlesNYT(data, results_on_page);
    url = 'http://api.nytimes.com/svc/mostpopular/v2/mostviewed/' + section + '/30.json?api-key=2cb1edcc1d8ca6933ff413e3fb574774:9:72000218&offset=' + str(20 * i)
    if not is_last_run:
      data = requests.get(url).json();
  return articles

def getMostViewedArticlesNYT(data, num_results):
  articles = []
  results = data['results']
  for i in range(0, num_results):
    item = results[i]
    if item['type'] == "Article":
      article_data = getArticleInfoNYT(item)
      if article_data['location'] != None:
        articles.append(article_data)
  return articles

def getSearchArticlesNYT(data):
  articles = []
  results = data['response']['docs']
  for i in range(0, len(results)):
    item = results[i]
    if item['document_type'] == "article":
      article_data = getSearchInfoNYT(item)
      if article_data['location'] != None:
        articles.append(article_data)
  return articles

def getSearchInfoNYT(item):
  title = item['headline']['main']
  url = item['web_url']
  date_published = item['pub_date'][:10]
  section = item['section_name']
  source = "The New York Times"
  abstract = item['snippet']
  location = getSearchLocationNYT(item['keywords'])
  return {'title': title, 'url': url, 'date_published': date_published, 'section': section, 
          'source': source, 'abstract': abstract, 'location': location}


def getArticleInfoNYT(item):
  title = item['title']
  url = item['url']
  date_published = item['published_date'][:10]
  section = item['section']
  source = "The New York Times"
  abstract = item['abstract']
  location = getLocationNYT(item['geo_facet'])
  return {'title': title, 'url': url, 'date_published': date_published, 'section': section, 
          'source': source, 'abstract': abstract, 'location': location}

def getSearchLocationNYT(keywords):
  for i in range(len(keywords)):
    item = keywords[i]
    if item['name'] == "glocations":
      location = item['value']
      db_entry = Location.objects.filter(query=location)
      if not db_entry:
        url = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + urllib.quote(location)
        url += '&key=AIzaSyDQVm4SWjSOB7fNfHk332pM3Te6IiPSyoM'
        data = requests.get(url).json()
        for result in data['results']:
          latitude = result['geometry']['location']['lat']
          longitude = result['geometry']['location']['lng']
          name = result['formatted_address']
          new_location = Location(query=location, lat=latitude, lng=longitude, name=name, is_valid=True)
          new_location.save()
          return {'lat': latitude, 'lng': longitude, 'name': name}
        new_location = Location(query=location, lat=0, lng=0, name="", is_valid=False)
        new_location.save()
      else:
        db_entry = db_entry[0]
        if db_entry.is_valid:
          return {'lat': db_entry.lat, 'lng': db_entry.lng, 'name': db_entry.name}
  return None

def getLocationNYT(locations):
  for i in range(len(locations)):
    location = locations[i]
    db_entry = Location.objects.filter(query=location)
    if not db_entry:
      url = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + urllib.quote(location)
      url += '&key=AIzaSyDQVm4SWjSOB7fNfHk332pM3Te6IiPSyoM'
      data = requests.get(url).json()
      for result in data['results']:
        latitude = result['geometry']['location']['lat']
        longitude = result['geometry']['location']['lng']
        name = result['formatted_address']
        new_location = Location(query=location, lat=latitude, lng=longitude, name=name, is_valid=True)
        new_location.save()
        return {'lat': latitude, 'lng': longitude, 'name': name}
      new_location = Location(query=location, lat=0, lng=0, name="", is_valid=False)
      new_location.save()
    else:
      db_entry = db_entry[0]
      if db_entry.is_valid:
        return {'lat': db_entry.lat, 'lng': db_entry.lng, 'name': db_entry.name}
  return None

def getNumIterates(num_results, times_to_iterate):
  max_times_iterate = (num_results / 20) + 1
  if max_times_iterate % 20 == 0:
    max_times_iterate -= 1
  if times_to_iterate > max_times_iterate:
    times_to_iterate = max_times_iterate
  return times_to_iterate