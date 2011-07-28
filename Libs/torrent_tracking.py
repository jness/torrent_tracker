import os
import urllib2

from cache import get_cache
from re import compile
from configobj import ConfigObj
from glob import glob
from config import get_config

def series():
    '''Return a list of all configs found in conf_dir,
    the configuration will contain needed regular expressions and 
    URLs to grab latest episodes.'''
    
    relpath = os.path.split(os.path.abspath(__file__))[0]
    path = os.path.split(relpath)[0]
    config_dir = path + '/Series'
    series = []
    for _file in glob("%s/*.conf" % config_dir):
        c = ConfigObj(_file)
        if not c['enabled'] in [True, 'True', 'true', 1, '1']:
            continue
        series.append(c)
    return series

def newepisodes(episodes, cachefile, name):
    '''Checks the episode against our pickle database 
    to determine if this is a new episodes'''

    # read our cache
    cache = get_cache(cachefile)
   
    newepisodes = {}
    for e in episodes:
        for results in e:
            if results.isdigit():
                epnum = results
                episodename = name + epnum

        # compare episode with cache
        new = True
        for c in cache:
            if episodename in c:
                new = False
        if new:
            newepisodes[epnum] = e

    newepisodes = list(newepisodes.values())

    return newepisodes

def download_torrent(name, episode, torrent, path):
    '''downloads torrent files to path/name-episodenum.torrent'''
    c = get_config()
    
    # take user based paths
    path = os.path.expanduser(path)

    if not os.path.exists(path):
        os.makedirs(path)
    f = open('%s/%s-%s%s' % (path, name, episode, c['file_extension']), 'w')
    try:
        tor = urllib2.urlopen(torrent)
        f.write(tor.read())
    except urllib2.HTTPError as e:
        status = '%s %s url was %s' % (e.getcode(), e.msg, torrent)
    else:
        status = 'Downloaded %s%s from %s' % (episode, c['file_extension'], torrent)
    f.close()
    return status
