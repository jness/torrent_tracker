# This is an addtional provider for http://www.demonoid.me/
# which supports checking a users RSS feed for new torrents

import urllib2
import re

def userRSS(user, series):
    '''Search a prefered User's RSS feed for episodes similar to your series'''
    u = 'http://www.demonoid.me/rss/users/%s.xml' % user
    req = urllib2.urlopen(u)
    rss = req.read()

    match = re.compile('<title>TV - (%s .*)</title>.*<link>(.*)</link>' % series, re.IGNORECASE).findall(rss)
    return match

def episodes(s):
    '''Search over the results of userRSS and extract episode numbers,
    then return URLs for all episodes greater or equal to your startnum'''
    epis = []
    items = userRSS(s['watchuser'], s['searchname'])
    for item in items:
        epnum = re.search('%s S[0]?%sE([0]?\d*)' % (s['searchname'], s['season']), item[0], re.IGNORECASE)
        if epnum:
            if epnum.group(1) >= int(s['startnum']):
                u = item[1]
                req = urllib2.urlopen(u)
                page = req.read()
                match = re.search('<a href="(.*)">Click here to download the torrent</a>', page)
                if match:
                    epis.append(('http://www.demonoid.me' + match.group(1), epnum.group(1)))
    return epis

