from bs4 import BeautifulSoup as bs
import urlparse
from urllib2 import urlopen
from urllib import urlretrieve
import ImageFile
import os
import sys

def getImagesFromURL(url, out_folder="/Users/slee/shopsquare/media/images/usrimg/", filename="image.jpg"):
    """Downloads all the images at 'url' to /test/"""
    soup = bs(urlopen(url))
    parsed = list(urlparse.urlparse(url))
    images = soup.findAll("img")
    print len(images)

    for image in images:
        parsed_base = parsed[:]
        print "*"*80
        print "iterating over image: %s" % image
        if image["src"].startswith("http"):
            full_image_uri = image["src"]
        elif image["src"].startswith('//'):
            parsed_base[1] = image["src"].lstrip('/')
            full_image_uri = urlparse.urlunparse(parsed_base).rstrip('/')
        else:
            parsed_base[2] = image["src"]
            full_image_uri = urlparse.urlunparse(parsed_base).rstrip('/')
        print "full image uri: %s" % full_image_uri
        try:
            (bytes, (w,h)) = getsizes(full_image_uri)
            if w < 80 or h < 80:
                #print "skip image, (%s,%s) is too small" % (w,h)
                continue
            if bytes < 5120:
                #print "skip image, (%s) is too small" % bytes
                continue
        except Exception, e:
            pass
        
        outpath = os.path.join(out_folder, filename)
        print "scraping to file: %s" % outpath
        if image["src"].lower().startswith("http"):
            urlretrieve(image["src"], outpath)
        else:
            urlretrieve(full_image_uri, outpath)
        break

    return filename

def getsizes(uri):
    # get file size *and* image size (None if not known)
    file = urlopen(uri)
    size = file.headers.get("content-length")
    if size: size = int(size)
    p = ImageFile.Parser()
    while 1:
        data = file.read(1024)
        if not data:
            break
        p.feed(data)
        if p.image:
            return size, p.image.size
            break
    file.close()
    return size, None
            
def _usage():
    print "usage: python dumpimages.py http://example.com [outpath]"
    
if __name__ == "__main__":
    url = sys.argv[-1]
    out_folder = "/test/"
    if not url.lower().startswith("http"):
        out_folder = sys.argv[-1]
        url = sys.argv[-2]
        if not url.lower().startswith("http"):
            _usage()
            sys.exit(-1)
    getImagesFromURL(url, out_folder)
