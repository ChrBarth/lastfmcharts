# lastfmcharts

last.fm charts on the commandline with python.

## requirements:

requires python3 and BeautifulSoup (sudo apt install python-bs4)

## usage:

    lastfmcharts.py [options]
    [u=lastfm-user]
    [c=artists|tracks|albums]
    [f=date from YYYY-MM-DD]
    [t=date to YYYY-MM-DD]
    [l=limit (1-50)]
    [s=y/n (display number of scrobbles, default no)]
    [n=y/n (display rank numbers, default yes)]

example:

    lastfmcharts.py u=joesmith c=albums f=2016-01-01 t=2016-12-31 l=10

Grabs the top 10 (l=10) albums(c=albums) of the last.fm user joesmith for the time between Jan 1st 2016 (f=2016-01-01) and Dec 31st 2016 (t=2016-12-31) 

## known issues:

~~special characters in album- and songtitles result in "unknown" since BeautifulSoup (the python-library that does all the dirty work) seems to have a problem with those.~~
(suddenly works as expected...)
