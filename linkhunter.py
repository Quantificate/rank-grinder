from bs4 import BeautifulSoup as bs
from bs4 import SoupStrainer as ss
import urllib as ul
import urllib.request
import bleach
import re

with ul.request.urlopen('http://www.premier-mountain-properties.net/sitemap/') as response:
    html = response.read()

articles = ss('a')
linklist=[]
soup = bs(html, "lxml", parse_only=articles)
for link in soup.find_all('a', href=True):
    linklist.append(link['href'])

print(linklist)
clearflags = ['/', '/rss','#weatherinline','/happenings/','/sitemap']
clearlist = [x for x in linklist if '.' not in x]
clearlinks = [y for y in clearlist if y not in clearflags]
print(clearlinks)

finallinks = []
a=0
while a < len(clearlinks):
    fulllink = 'http://www.premier-mountain-properties.net' + clearlinks[a]
    finallinks.append(fulllink)
    a=a+1
print(finallinks)