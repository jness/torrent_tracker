#!/usr/bin/env python

import sys
from Libs.config import get_config
from Libs.cache import get_cache, add_cache
from Libs.torrent_tracking import series, newepisodes, download_torrent

def main():
    '''Our main function that does all the work'''

    newfiles = []
    c = get_config()
    
    ser = series()
    for s in ser:

        # load the correct module
        provider = 'Providers.%s' % s['provider']
        __import__(provider)
        episodes = sys.modules[provider].episodes

        print '\n'
        print 'Searching for episodes in %s using provider %s' % (s['name'], s['provider']) 
        epis = episodes(s)

        new = newepisodes(epis, c['cachefile'], s['name'])
        
        for ep in new:
            print 'Found new episode!', ep
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
            filename = '%s-%s.%s' % (s['name'], ep_number, c['file_extension'])
            print 'Attempting to Download %s' % filename
            d = download_torrent(s['name'], ep_number, tor, c['download_path'])
            print d

            add_cache(c['cachefile'], (torrent, s['name'] + ep_number))
            newfiles.append(filename)

    # Notifications
    # send Email if enabled
    if c['enable_email'] == 'True':
        from Libs.emailnotify import send_email
        send_email(
            c['toaddr'],
            c['fromaddr'],
            newfiles,
            c['host'])

    # send SMS if enabled, this modular 
    # requires pygooglevoice
    if c['enable_sms'] == 'True':
        from Libs.smsnotify import send_sms
        send_sms(
            c['gmail_username'], 
            c['gmail_password'], 
            c['cellnumber'], 
            newfiles)

# run main if we called directly
if '__main__' == __name__:
    main()
