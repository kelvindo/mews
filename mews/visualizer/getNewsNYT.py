import urllib
import requests
import json

def getTopStoriesNYT():
  url = 'http://api.nytimes.com/svc/topstories/v1/home.json?api-key=903cc78251a8120cd1be50993e594000:12:72000218'
  data = requests.get(url).json()
  num_results = data['num_results']
  results = data['results']
  top_stories = []
  for i in range(0, num_results):
    item = results[i]
    if item['item_type'] == "Article":
      article_data = getTopStoriesInfoNYT(item)
      if article_data['location'] != None:
        top_stories.append(article_data)
  return top_stories

def getTopStoriesInfoNYT(item):
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
    url = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + urllib.quote(location)
    url += '&key=AIzaSyDQVm4SWjSOB7fNfHk332pM3Te6IiPSyoM'
    data = requests.get(url).json()
    for result in data['results']:
      latitude = result['geometry']['location']['lat']
      longitude = result['geometry']['location']['lng']
      name = result['formatted_address']
      return {'lat': latitude, 'lng': longitude, 'name': name}
  return None;