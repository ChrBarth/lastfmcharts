#!/usr/bin/python3
# -*- coding: UTF8 -*-

# last.fm Charts in python!

from bs4 import BeautifulSoup
import urllib.request
import sys
import re

# Defaultwerte:
lastfmuser = ""			# last.fm username
datefrom = "2015-01-01"		# start-date
dateto = "2015-12-31"		# end-date
result = []
scrobbles = []
limit = 20			# max no. of hits
charttype = "artists"		# top artists/tracks/albums
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
			print("user changed to " + lastfmuser)
		if m.group(1) == "c":
			cmatch = re.match("(artists|tracks|albums)", m.group(2))
			if cmatch:
				charttype = m.group(2)
				print("charttype changed to " + charttype)
		if m.group(1) == "f":
			cmatch = re.match("\d\d\d\d-\d\d-\d\d", m.group(2))
			if cmatch:
				datefrom = m.group(2)
				print("start date changed to " + datefrom)
		if m.group(1) == "t":
			cmatch = re.match("\d\d\d\d-\d\d-\d\d", m.group(2))
			if cmatch:
				dateto = m.group(2)
				print("end date changed to " + dateto)
		if m.group(1) == "l":
			cmatch = re.match("^\d+$", m.group(2))
			if cmatch:
				limit = int(m.group(2))
				print("limit changed to " + str(limit))
		if m.group(1) == "s":
			cmatch = re.match("^[yn]$", m.group(2), flags=re.IGNORECASE)
			if cmatch:
				if cmatch.group(0).lower() == "y":
					display_scrobbles = True
					print("Displaying scrobbles...")
				else:
					display_scrobbles = False
					print("Don`t show scrobbles...")
		if m.group(1) == "n":
			cmatch = re.match("^[yn]$", m.group(2), flags=re.IGNORECASE)
			if cmatch:
				if cmatch.group(0).lower() == "y":
					display_ranknums = True
					print("Displaying rank numbers...")
				else:
					display_ranknums = False
					print("Don`t display rank numbers...")

if(lastfmuser == ""):
	print("Need at least a last.fm username. Aborting...")
	sys.exit()

# loading the page
requrl = "http://www.last.fm/de/user/" + lastfmuser + "/library/" + charttype + "?from=" + datefrom + "&to=" + dateto	# generates the url we will open and parse
req = urllib.request.Request(requrl)
response = urllib.request.urlopen(requrl)
htmlpage = response.read()

soup = BeautifulSoup(htmlpage, 'html.parser')

# artists:
if charttype == "artists":
	for a in soup.find_all("td", "chartlist-name"):
		artist = a.span.text
		result.append(artist.strip("\n"))

# albums:
if charttype == "albums":
	for a in soup.find_all("a", "link-block-target"):
		if(a.get('title')):
			result.append(a['title'])
		else:
			result.append("unknown")
			# happens sometimes when the tag contains special characters...

# tracks:
if charttype == "tracks":
	for a in soup.find_all("a", "link-block-target"):
		if(a.get('title')):
			result.append(a['title'])
		else:
			result.append("unknown")
			# see above

# number of scrobbles:
for s in soup.find_all("td", "chartlist-countbar"):
	scrobble = s.span.text
	scrobbles.append(int(scrobble.strip("\n Scrobles")))

# adjust value of limit if we have fewer results than limit:
if len(scrobbles)<limit:
	limit = len(scrobbles)

# trim the results:
del result[limit:]

# printing the charts:
print("\n\nDisplaying %s-charts for user %s between %s and %s\n\n" % (charttype, lastfmuser, datefrom, dateto))
for n,line in enumerate((result)):
	output = ""
	if display_ranknums:
		output = str(n+1) + " - "
	output = output + line
	if display_scrobbles:
		output = output + " (" + str(scrobbles[n]) + ")"
	print(output)
