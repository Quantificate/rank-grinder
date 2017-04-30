import urllib as ul
import urllib.request

earl = 'http://www.premier-mountain-properties.net/sell-my-home-wildhorse-at-prospect/'
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