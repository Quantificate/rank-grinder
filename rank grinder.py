from bs4 import BeautifulSoup as bs
from bs4 import SoupStrainer as ss
import urllib as ul
import urllib.request
import bleach
import re
import csv

#open sitemap
with ul.request.urlopen('http://www.premier-mountain-properties.net/sitemap/') as response:
    html = response.read()

#extract sitemap links within the domain
articles = ss('a')
linklist=[]
soup = bs(html, "lxml", parse_only=articles)
for link in soup.find_all('a', href=True):
    linklist.append(link['href'])

clearflags = ['/', '/rss','#weatherinline','/happenings/','/sitemap']
clearlist = [x for x in linklist if '.' not in x]
clearlinks = [y for y in clearlist if y not in clearflags]

finallinks = []
a=0
while a < len(clearlinks):
    fulllink = 'http://www.premier-mountain-properties.net' + clearlinks[a]
    finallinks.append(fulllink)
    a=a+1

#iterate over finallinks
z=0
while z < len(finallinks):
    # turn keyterm into a list
    earl = finallinks[z]
    breakdown = re.sub('\W+', ' ', earl)
    breakdown = re.sub(r"([A-Z])", r" \1", breakdown)
    breakdown = breakdown.split()
    print(breakdown)
    # pull keyterm from url
    item = breakdown[0]
    while item != 'net':
        breakdown.remove(breakdown[0])
        item = breakdown[0]
    if breakdown[0] == 'net': breakdown.remove(breakdown[0])
    keyterm = breakdown
    # get html from url
    with ul.request.urlopen(earl) as response:
        html = response.read()
    #calculate main content and secondary content
    html = str(html)
    html = html.lower()
    MC = ['<article>', '<meta name="description"', '<iframe ']
    SC = ['<nav class="bottom-nav"', '<footer', '<aside id="site-contact"']
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
        a = a + 1
    while b < stag:
        sctotal = html.count(SC[b])
        print(SC[b] + ": " + str(sctotal))
        seccontent = seccontent + sctotal
        b = b + 1
    #score mc and sc
    maincontent = maincontent * 10
    seccontent = seccontent * 5
    tags = html.count(UN[0])
    uncontent = tags - maincontent - seccontent
    print("Total Unrelated Tags: " + str(uncontent))
    # Calculate % of MC and SC.
    mcper = round((maincontent / uncontent) * 100, 2)
    scper = round((seccontent / uncontent) * 100, 2)
    print("Main: " + str(mcper))
    print("Secondary: " + str(scper))

    # pull just the article from the html
    articles = ss('article')
    # clean all tags from the article
    soup = bs(html, "lxml", parse_only=articles)
    article = soup.find_all('article')
    thing = bleach.clean(str(article), strip=True)
    thing = re.sub('\W+', ' ', thing)
    thing = re.sub(r"([A-Z])", r" \1", thing)
    # remove extraneous words from the text
    text = thing
    text = text.lower()
    text = text.split()
    cleanlist = ["a", "an", "the", "for", "of", "it", "but", "nor", "so", "and", "but", "or", "yet", "is", "to", "at",
                 "i", "if", "as", "in", "by", "on", "li", "ul", "p"]
    cleantext = [word for word in text if word.lower() not in cleanlist]
    # count keyterms in the text
    izer = len(keyterm)
    x = 0
    totalkts = 0
    while x < izer:
        kts = cleantext.count(keyterm[x])
        print(keyterm[x] + ": " + str(kts))
        totalkts = totalkts + kts
        x = x + 1
    # count total words in text
    wordcount = len(cleantext)
    print("Total words: " + str(wordcount))
    # calculate keyterm density
    dense = (totalkts / wordcount) * 100
    print("Keyword Density: " + str(round(dense, 2)) + "%")

    if 4 < dense and dense < 10:
        ktdscore = 5
    elif dense < 4 and dense > 2:
        ktdscore = 2.5
    elif dense > 8 and dense < 13:
        ktdscore = 2.5
    else:
        ktdscore = 0
    # PageSpeed
    # TODO: Find a way to run PageSpeed from the script.
    # TODO: Assign score to PageSpeed. [score/20]?
    psi = 89
    psi = int(psi)
    # TODO: Assign score to Mobile. [score/10]?
    psimob = 71
    psimob = int(psimob)
    psiscore = ((psi / 20) + (psimob / 10)) / 2
    # Backlinks
    # TODO: Find a way to crawl for backlinks.
    # TODO: Assign score to backlinks. [2 per]?
    linx = 3
    linx = int(linx)
    backscore = linx * 2
    # Content
    # TODO: Assign a score to content [MC/10 + SC/20]?
    mainc = mcper
    secc = scper
    mainc = float(mainc)
    secc = float(secc)
    conscore = round((mainc / 10) + (secc / 20), 2)
    totalscore = ktdscore + psiscore + conscore + backscore
    totalscore = round(totalscore, 2)
    print("Keyterm Score: " + str(ktdscore))
    print("PageSpeed Score: " + str(psiscore))
    print("Backlink Score: " + str(backscore))
    print("Content Score: " + str(conscore))
    print("Site SEO Score: " + str(totalscore))
    final = [earl, ktdscore, psiscore, backscore, conscore, totalscore]
    print(final)
    with open('scores.csv', 'w') as fout:
        w = csv.writer(f)
        w.writerow(['URL', 'Keyterm Score', 'PageSpeed Score', 'Backlink Score', 'Content Score', 'Total Score'])
        w.writerows(final)