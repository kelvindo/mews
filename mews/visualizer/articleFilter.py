from datetime import datetime, date

##########################################################################
#                                                                        #
# The two filter functions, filterBySection and filterByDate, each take  #
# an array of articles to sort as the paramter.                          #
#                                                                        #
# filterBySection(articles):                                             #
#    Returns a dictionary. Key = section.                                #
#    Value = array of articles with that section.                        #
#                                                                        #
# filterByDate(articles):                                                #
#    Returns a dictionary with the (string) keys: '1', '7', '30'         #
#    Value = array of articles published within that many days           #
#                                                                        #
##########################################################################

def filterBySection(articles):
  sectionMap = {};
  for article in articles:
    section = article.section
    if section in sectionMap:
      articleArray = sectionMap[section]
      articleArray.append(article)
      sectionMap[section] = articleArray
    else:
      articleArray = []
      articleArray.append(article)
      sectionMap[section] = articleArray
  return sectionMap

def filterByDate(articles):
  oneDayArticles = []
  sevenDayArticles = []
  thirtyDayArticles = []
  for article in articles:
    articleDate = article.date_published
    todayDate = date.today()
    daysDifference = (todayDate - articleDate).days
    if daysDifference <= 1:
      oneDayArticles.append(article)
    if daysDifference <= 7:
      sevenDayArticles.append(article)
    if daysDifference <= 30:
      thirtyDayArticles.append(article)
  dateMap = {'1': oneDayArticles, '7': sevenDayArticles, '30': thirtyDayArticles}
  return dateMap
