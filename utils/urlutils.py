from time import time
from utils import slugify
import MyGlobals

def getStoreImageFilename(storename, storeid):
    return "%s-%s.jpg" % (slugify.slugify(storename), storeid)

def getScrapedImageFilename():
    return "%s.jpg" % int(time())

def getWishlistImageFilename(wlid):
    return "%s.jpg" % wlid

if __name__ == "__main__":
    pass
        
