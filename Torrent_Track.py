#!/usr/bin/env python
import os
import urllib2
import pickle

def get_cache(cachefile):
    '''reads in our cache file and returns results if found,
    if a cache file does not exist return a empty list'''
    
    c = os.path.expanduser(cachefile)
    if os.path.exists(c):
        f = open(c, 'rb')
        cache = pickle.load(f)
        f.close()
        return cache
    else:
        return list()
        
def add_cache(cachefile, torrent):
    '''appends to the cache file which was returned from get_cache()'''
    
    cache = get_cache(cachefile)
    cache.append(torrent)
    
    c = os.path.expanduser(cachefile)
    f = open(c, 'wb')
    pickle.dump(cache, f)
    f.close()
    return
    

def series():
    '''Return a list of all configs found in conf_dir,
    the configuration will contain needed regular expressions and 
    URLs to grab latest episodes.'''
    
    from configobj import ConfigObj
    from glob import glob
    path = os.path.split(os.path.abspath(__file__))[0]
    config_dir = path + '/Series'
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
        for results in m:
            if results.isdigit():
                start_ep = results

        if int(start_ep) >= int(s['startnum']):
            epis.append(m)

    # return all episodes greater than startnum
    return epis


def newepisodes(episodes, cachefile):
    '''Checks our Pickle Database for new episodes'''

    # read our cache
    cache = get_cache(cachefile)
    
    newepisodes = []
    for e in episodes:
        for results in e:
            if not results.isdigit():
                ep = results

        # compare episode with cache
        if ep not in cache:
            newepisodes.append(e)

    # be sure to remove any duplicates
    newepisodes = list(set(newepisodes))

    return newepisodes

def download_torrent(name, episode, torrent, path):
    '''Downloads torrent files to path/name-episode.torrent'''

    if not os.path.exists(path):
        os.makedirs(path)
    f = open('%s/%s-%s.torrent' % (path, name, episode), 'w')
    tor = urllib2.urlopen(torrent)
    f.write(tor.read())
    f.close()
    return

def send_sms(username, password, cellnumber, filename):
    '''Sends a SMS message to cellnumber via Google API'''
    from googlevoice import Voice

    voice = Voice()
    voice.login(username, password)
    text = '%s downloaded' % filename
    voice.send_sms(cellnumber, text)
    return

def main():
    '''Our main function that does all the work'''
    
    # space for config options
    cachefile = '~/.torrent_cache'
    download_path = 'Torrents'

    enable_sms = False
    gmail_username = 'nobody'
    gmail_password = 'nobody'
    cellnumber = '555-555-5555'
    
    ser = series()
    for s in ser:
        epis = episodes(s)
        new = newepisodes(epis, cachefile)
        
        for ep in new:
            # extract our ep_number and torrent url
            for e in ep:
                if e.isdigit():
                    ep_number = e
                elif not e.isdigit():
                    torrent = e
                    
            # add prefix if we have it configured
            try:
                tor = '%s%s' % (s['prefix'], torrent)
            except KeyError:
                tor = torrent
                
            # some sites tend to use ampersand urls
            tor = tor.replace('amp;', '')
            
            # download our torrent file
            filename = '%s-%s.torrent' % (s['name'], ep_number)
            print 'Downloading %s' % filename
            download_torrent(s['name'], ep_number, tor, download_path)
            
            # send SMS if enabled
            if enable_sms:
                send_sms(gmail_username, gmail_password, cellnumber, filename)
            add_cache(cachefile, torrent)

# run main if we called directly
if '__main__' == __name__:
    main()
