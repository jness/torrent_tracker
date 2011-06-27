import os
from configobj import ConfigObj
from glob import glob

def get_config():
    '''Reads in our config from the Config directory'''
    
    relpath = os.path.split(os.path.abspath(__file__))[0]
    path = os.path.split(relpath)[0]
    config = path + '/Config/torrent_tracker.conf'
    c = ConfigObj(config)
    return c
