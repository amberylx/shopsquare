from time import time
from utils import slugify
import MyGlobals

def getStoreImageFilename(storename, storeid):
    return "%s-%s.jpg" % (slugify.slugify(storename), storeid)

def getStoreCroppedImageFilename(storename, storeid):
    return "%s-%s.jpg" % (slugify.slugify(storename), storeid)

def getStoreScrapedImageFilename():
    return "%s.jpg" % int(time())

if __name__ == "__main__":
    pass
        
