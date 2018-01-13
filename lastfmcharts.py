#!/usr/bin/python3
# -*- coding: UTF8 -*-

# last.fm Charts in python!

from bs4 import BeautifulSoup
import urllib.request
import sys
import re

# Defaultwerte:
lastfmuser = ""         # last.fm username
datefrom = "2015-01-01"     # start-date
dateto = "2015-12-31"       # end-date
result = []
scrobbles = []
limit = 20          # max no. of hits
charttype = "artists"       # top artists/tracks/albums
display_scrobbles = False
display_ranknums = True

# parsing the commandline:
if len(sys.argv) == 1:
    print("""usage: lastfmcharts
    [u=lastfm-user]
    [c=artists|tracks|albums]
    [f=date from YYYY-MM-DD]
    [t=date to YYYY-MM-DD]
    [l=limit (1-50)]
    [s=y/n (display number of scrobbles, default no)]
    [n=y/n (display rank numbers, default yes)]
""")
    sys.exit(1)

for a in sys.argv[1:]:
    m = re.match("^([ucftlsn])\=(.*)", a)
    if m:
        if m.group(1) == "u":
            lastfmuser = m.group(2)
        if m.group(1) == "c":
            cmatch = re.match("(artists|tracks|albums)", m.group(2))
            if cmatch:
                charttype = m.group(2)
        if m.group(1) == "f":
            cmatch = re.match("\d\d\d\d-\d\d-\d\d", m.group(2))
            if cmatch:
                datefrom = m.group(2)
        if m.group(1) == "t":
            cmatch = re.match("\d\d\d\d-\d\d-\d\d", m.group(2))
            if cmatch:
                dateto = m.group(2)
        if m.group(1) == "l":
            cmatch = re.match("^\d+$", m.group(2))
            if cmatch:
                limit = int(m.group(2))
        if m.group(1) == "s":
            cmatch = re.match("^[yn]$", m.group(2), flags=re.IGNORECASE)
            if cmatch:
                if cmatch.group(0).lower() == "y":
                    display_scrobbles = True
                else:
                    display_scrobbles = False
        if m.group(1) == "n":
            cmatch = re.match("^[yn]$", m.group(2), flags=re.IGNORECASE)
            if cmatch:
                if cmatch.group(0).lower() == "y":
                    display_ranknums = True
                else:
                    display_ranknums = False

if(lastfmuser == ""):
    print("Need at least a last.fm username. Aborting...")
    sys.exit()

# loading the page
requrl = "http://www.last.fm/de/user/" + lastfmuser + "/library/" + charttype + "?from=" + datefrom + "&to=" + dateto   # generates the url we will open and parse
req = urllib.request.Request(requrl)
response = urllib.request.urlopen(requrl)
htmlpage = response.read()

soup = BeautifulSoup(htmlpage, 'html.parser')

# artists:
if charttype == "artists":
    for a in soup.find_all("td", "chartlist-name"):
        artist = a.span.text
        result.append(artist.strip("\n"))

# albums/tracks:
if charttype == "albums" or charttype == "tracks":
    for a in soup.find_all("a", "link-block-target"):
        if(a.get('title')):
            result.append(a['title'])
        else:
            result.append("unknown")
            # happens sometimes when the tag contains special characters...

# number of scrobbles:
for s in soup.find_all("td", "chartlist-countbar"):
    scrobble = s.span.text
    # remove dots ( "1.000" => "1000")
    scrobble = scrobble.replace('.','').strip("\n Scrobbles")
    scrobbles.append(int(scrobble))

# trim the results:
del result[limit:]

# printing the charts:
print("%s for user %s between %s and %s\n" % (charttype, lastfmuser, datefrom, dateto))
for n,line in enumerate((result)):
    output = ""
    if display_ranknums:
        output = str(n+1) + " - "
    output = output + line
    if display_scrobbles:
        output = output + " (" + str(scrobbles[n]) + ")"
    print(output)
