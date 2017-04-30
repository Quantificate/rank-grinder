from bs4 import BeautifulSoup as bs
from bs4 import SoupStrainer as ss
import urllib as ul
import urllib.request
import bleach
import re

#turn keyterm into a list
earl = '<url goes here>'
breakdown = re.sub('\W+',' ', earl)
breakdown = re.sub( r"([A-Z])", r" \1", breakdown)
breakdown = breakdown.split()
print(breakdown)
#pull keyterm from url
item = breakdown[0]
while item != 'net':
    breakdown.remove(breakdown[0])
    item = breakdown[0]
if breakdown[0] == 'net': breakdown.remove(breakdown[0])
keyterm = breakdown
#get html from url
with ul.request.urlopen(earl) as response:
    html = response.read()

html = str(html)
html = html.lower()
MC = ['<article>','<meta name="description"', '<iframe ']
SC = ['<nav class="bottom-nav"','<footer','<aside id="site-contact"']
UN = ['</']
mtag = len(MC)
stag = len(SC)
a = 0
b = 0
c = 0
maincontent = 0
seccontent = 0
while a < mtag:
    mctotal = html.count(MC[a])
    print(MC[a] + ": " + str(mctotal))
    maincontent = maincontent + mctotal
    a = a+1
while b < stag:
    sctotal = html.count(SC[b])
    print(SC[b] + ": " + str(sctotal))
    seccontent = seccontent + sctotal
    b = b+1

maincontent = maincontent*10
seccontent = seccontent*5
tags = html.count(UN[0])
uncontent = tags - maincontent - seccontent
print("Total Unrelated Tags: " + str(uncontent))
#Calculate % of MC and SC.
mcper = round((maincontent / uncontent)*100, 2)
scper = round((seccontent / uncontent)*100, 2)
print("Main: " + str(mcper))
print("Secondary: " + str(scper))
#pull just the article from the html
articles = ss('article')
#clean all tags from the article
soup = bs(html, "lxml", parse_only=articles)
article = soup.find_all('article')
thing = bleach.clean(str(article), strip=True)
thing = re.sub('\W+',' ', thing)
thing = re.sub( r"([A-Z])", r" \1", thing)
#remove extraneous words from the text
text = thing
text = text.lower()
text = text.split()
cleanlist = ["a", "an", "the", "for", "of", "it", "but", "nor", "so", "and", "but", "or", "yet", "is", "to", "at", "i", "if", "as", "in", "by", "on", "li", "ul", "p"]
cleantext  = [word for word in text if word.lower() not in cleanlist]
#count keyterms in the text
izer = len(keyterm)
x = 0
totalkts = 0
while x < izer:
  kts = cleantext.count(keyterm[x])
  print(keyterm[x] + ": " + str(kts))
  totalkts = totalkts + kts
  x = x+1
#count total words in text
wordcount = len(cleantext)
print("Total words: " + str(wordcount))
#calculate keyterm density
dense = (totalkts/wordcount)*100
print("Keyword Density: " + str(round(dense, 2)) + "%")

if 4 < dense and dense < 10:
  ktdscore = 5
elif dense < 4 and dense > 2:
  ktdscore = 2.5
elif dense > 8 and dense < 13:
  ktdscore = 2.5
else:
  ktdscore = 0
#PageSpeed
#TODO: Find a way to run PageSpeed from the script.
#TODO: Assign score to PageSpeed. [score/20]?
psi = input("PageSpeed Desktop Score: ")
psi = int(psi)
#TODO: Assign score to Mobile. [score/10]?
psimob = input("PageSpeed Mobile Score: ")
psimob = int(psimob)
psiscore = ((psi/20) + (psimob/10))/2
#Backlinks
#TODO: Find a way to crawl for backlinks.
#TODO: Assign score to backlinks. [2 per]?
linx = input("Number of backlinks: ")
linx = int(linx)
backscore = linx*2
#Content
#TODO: Assign a score to content [MC/10 + SC/20]?
mainc = mcper
secc = scper
mainc = float(mainc)
secc = float(secc)
conscore = round((mainc/10) + (secc/20), 2)
totalscore = ktdscore + psiscore + conscore + backscore
totalscore = round(totalscore, 2)
print("Keyterm Score: " + str(ktdscore))
print("PageSpeed Score: " + str(psiscore))
print("Backlink Score: " + str(backscore))
print("Content Score: " + str(conscore))
print("Site SEO Score: " + str(totalscore))
final = [earl, ktdscore, psiscore, backscore, conscore, totalscore]
print(final)