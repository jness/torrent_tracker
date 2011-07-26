# This Provider can be used for any site that
# has a list of direct download torrent links

from StringIO import StringIO
import urllib2
from re import compile 

def episodes(s):
    '''Returns a list of all episodes greather than
    or equal to your startnum from a source with direct
    downloads.'''

    epis = []
    request = urllib2.Request(s['url'])
    request.add_header('Accept-encoding', 'gzip')
    response = urllib2.urlopen(request)
    if response.info().get('Content-Encoding') == 'gzip':
        buf = StringIO( response.read())
        f = gzip.GzipFile(fileobj=buf)
        data = f.read()
    else:
        data = response.read()
    match = compile(s['regex']).findall(data)

    # only check for episodes higher than our startnum
    for m in match:
        for results in m:
            if results.isdigit():
                start_ep = results

        if int(start_ep) >= int(s['startnum']):
            epis.append(m)

    # return all episodes greater than startnum
    return epis
