import urllib
import requests
import json
from .models import Location

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

# 20 is the max number of results on a page for NYT, each iteration gets 20 results
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
  return None;

def getNumIterates(num_results, times_to_iterate):
  max_times_iterate = (num_results / 20) + 1
  if max_times_iterate % 20 == 0:
    max_times_iterate -= 1
  if times_to_iterate > max_times_iterate:
    times_to_iterate = max_times_iterate
  return times_to_iterate