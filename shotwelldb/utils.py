# Non database specific support utils for shotwelldb
import re

def id_to_thumb(photoid):
    return "thumb%016x" % photoid
    
def regexp(pattern, item):
    r = re.compile(pattern)
    return r.search(item) is not None
