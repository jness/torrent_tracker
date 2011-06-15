#!/usr/bin/env python
import os
import urllib2
import pickle

def series():
    '''Return a list of all configs found in conf_dir,
    the configuration will contain needed regular expressions and 
    URLs to grab latest episodes.'''
    
    from configobj import ConfigObj
    from glob import glob

    path = os.path.split(os.path.abspath(__file__))[0]
    config_dir = path + '/series'
    series = []
    for _file in glob("%s/*.conf" % config_dir):
        c = ConfigObj(_file)
        if not c['enabled'] in [True, 'True', 'true', 1, '1']:
            continue
        series.append(c)
    return series

def episodes(s):
    '''Returns a list of all episodes greather than
    or equal to your startnum'''

    from re import compile

    epis = []

    u = urllib2.urlopen(s['url'])
    req = u.read()
    match = compile(s['regex']).findall(req)

    # only check for episodes higher than our startnum
    for m in match:
        try:
            float(m[0])
            start = m[0]
        except ValueError:
            start = m[1]

        if int(start) >= int(s['startnum']):
            epis.append(m)

    # return all episodes greater than startnum
    return epis


def newepisodes(episodes):
    '''Checks our Pickle Database for new episodes'''

    # read our cache
    c = os.path.expanduser('~/.anime_cache')
    if os.path.exists(c):
        f = open(c, 'rb')
        cache = pickle.load(f)
        f.close()
    else:
        f = open(c, 'wb')
        empty = []
        pickle.dump(empty, f)
        cache = []
        f.close()

    newepisodes = []

    for e in episodes:
        try:
            float(e[0])
            ep = e[1]
        except ValueError:
            ep = e[0]

        if ep not in cache:
            newepisodes.append(ep)
    return newepisodes

def download_torrent(torrent):
    '''Downloads torrent files'''

    from random import randrange

    name = randrange(2000, 100000)
    f = open('Torrents/' + str(name), 'w')
    tor = urllib2.urlopen(torrent)
    f.write(tor.read())
    f.close()


def main():
    ser = series()
    for s in ser:
        epis = episodes(s)
        new = newepisodes(epis)
        for torrent in new:
            try:
                download_torrent(s['prefix'] + torrent)
            except KeyError:
                download_torrent(torrent)
    
            print 'Downloading %s' % s['name'] 
            c = os.path.expanduser('~/.anime_cache')
            f = open(c, 'rb')
            cache = pickle.load(f)
            f.close()

            cache.append(torrent)
            f = open(c, 'wb')
            pickle.dump(cache, f)
            f.close()

if '__main__' == __name__:
    main()
