from time import time
from urlparse import urlparse
import slugify

def getStoreImageFilename(storename, storeid):
    return "%s-%s.jpg" % (slugify.slugify(storename), storeid)

def getScrapedImageFilename():
    return "%s.jpg" % int(time())

def getWishlistImageFilename(wlid):
    return "%s.jpg" % wlid

def getDomainFromUrl(url):
    split_domain = urlparse(url)[1].split('.')
    if len(split_domain) == 2:
        domain = split_domain[0]
    elif len(split_domain) == 3:
        domain = split_domain[1]
    elif len(split_domain) == 1:
        domain = split_domain[0]
    return domain

if __name__ == "__main__":
    print getDomainFromUrl('http://imm-living.com/index.php?p=product&cat_id=8')
    print getDomainFromUrl('http://www.urbanoutfitters.com/urban/catalog/productdetail.jsp?id=24033169&parentid=W_APP_DRESSES')
        
