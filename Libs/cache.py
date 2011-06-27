import os
import pickle

def get_cache(cachefile):
    '''reads in our pickle cache file and returns a list
    of episodes, else if a cache file does not exist return 
    a empty list'''
    
    c = os.path.expanduser(cachefile)
    if os.path.exists(c):
        f = open(c, 'rb')
        cache = pickle.load(f)
        f.close()
        return cache
    else:
        return list()
        
def add_cache(cachefile, torrent):
    '''appends a episode to the cache file using existing object
    which was returned from get_cache()'''
    
    cache = get_cache(cachefile)
    cache.append(torrent)
    
    c = os.path.expanduser(cachefile)
    f = open(c, 'wb')
    pickle.dump(cache, f)
    f.close()
    return
