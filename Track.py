#!/usr/bin/env python

from Libs.config import get_config
from Libs.cache import get_cache, add_cache
from Libs.torrent_tracking import series, episodes, newepisodes, download_torrent

def main():
    '''Our main function that does all the work'''

    # read our config
    c = get_config()
    
    ser = series()
    for s in ser:
        epis = episodes(s)
        new = newepisodes(epis, c['cachefile'])
        
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
            download_torrent(s['name'], ep_number, tor, c['download_path'])
            
            # send SMS if enabled
            if c['enable_sms'] == 'True':
                from Libs.sms import send_sms
                send_sms(
                    c['gmail_username'], 
                    c['gmail_password'], 
                    c['cellnumber'], 
                    filename)

            add_cache(c['cachefile'], torrent)

# run main if we called directly
if '__main__' == __name__:
    main()
