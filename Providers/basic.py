import urllib2
from re import compile 

def episodes(s):
    '''Returns a list of all episodes greather than
    or equal to your startnum from a source with direct
    downloads.'''

    epis = []
    u = urllib2.urlopen(s['url'])
    req = u.read()
    match = compile(s['regex']).findall(req)

    # only check for episodes higher than our startnum
    for m in match:
        for results in m:
            if results.isdigit():
                start_ep = results

        if int(start_ep) >= int(s['startnum']):
            epis.append(m)

    # return all episodes greater than startnum
    return epis
