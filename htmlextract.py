from bs4 import BeautifulSoup as bs
from bs4 import SoupStrainer as ss
import urllib as ul
import urllib.request
import bleach
import re

earl = 'http://www.premier-mountain-properties.net/acreage-properties-gunnison-county/'
breakdown = re.sub('\W+',' ', earl)
breakdown = re.sub( r"([A-Z])", r" \1", breakdown)
breakdown = breakdown.split()
print(breakdown)
a = 0
item = breakdown[0]
while item != 'net':
    breakdown.remove(breakdown[0])
    item = breakdown[0]
if breakdown[0] == 'net': breakdown.remove(breakdown[0])
print(breakdown)
with ul.request.urlopen(earl) as response:
    html = response.read()

articles = ss('article')

soup = bs(html, "lxml", parse_only=articles)
article = soup.find_all('article')
thing = bleach.clean(str(article), strip=True)
thing = re.sub('\W+',' ', thing)
thing = re.sub( r"([A-Z])", r" \1", thing).split()
print(thing)

#TODO: count words in keyterm
#TODO: pull first x words of completed string as keyterm