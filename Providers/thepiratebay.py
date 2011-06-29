# This is an addtional provider for http://thepiratebay.org/
# which supports searching

import urllib2
import re
from Libs.config import get_config

def TPBSearch(series):
    '''Search for a series on The Pirate Bay'''
    encode = urllib2.quote(series)
    u = 'http://thepiratebay.org/search/%s/0/99/200' % encode
    req = urllib2.urlopen(u)
    rss = req.read()

    match = re.compile('<a href="(.*)" class="detLink" title="Details for .*">(.*)</a>', re.IGNORECASE).findall(rss)
    return match

def episodes(s):
    '''Search over the results of userRSS and extract episode numbers,
    then return URLs for all episodes greater or equal to your startnum'''
    epis = []
    items = TPBSearch(s['searchname'])
    for item in items:
        epnum = re.search('%s\.S[0]?%sE([0]?\d*)' % (s['searchname'], s['season']), item[1], re.IGNORECASE)
        if epnum:
            if int(epnum.group(1)) >= int(s['startnum']):
                u = 'http://thepiratebay.org' + item[0]
                req = urllib2.urlopen(u)
                page = req.read()
                match = re.search('<a href="(.*\.torrent)" title="Download this torrent">Download this torrent</a>', page)
                if match:
                    epis.append((match.group(1), epnum.group(1)))

    return epis

