from bs4 import BeautifulSoup as bs
import urlparse
from urllib2 import urlopen
from urllib import urlretrieve
import ImageFile
import os
import sys

def getImagesFromURL(url, filedir="/Users/slee/shopsquare/media/images/usrimg/", filename="image.jpg", start_index=0):
    """Downloads all the images at 'url' to /test/"""
    parsed = urlparse.urlparse(url)
    soup = bs(urlopen(url))
    images = soup.findAll("img")

    didScrape = False
    imgindex = 0
    for x,image in enumerate(images):
        if x < start_index: continue
        if not image.has_key('src'): continue
        # get image uri
        base_split = parsed[:]
        img_split = urlparse.urlparse(image["src"])

        full_image_uri = (
            img_split[0] if img_split[0] else base_split[0],
            img_split[1] if img_split[1] else base_split[1],
            img_split[2],
            img_split[3],
            img_split[4],
            img_split[5]
            )
        
        full_image_uri = urlparse.urlunparse(full_image_uri)
        print "*"*80
        print "image tag %s has uri --> %s" % (image, full_image_uri)

        try:
            (bytes, (w,h)) = getsizes(full_image_uri)
            if w < 200 or h < 300:
                raise Exception
            if bytes and  bytes < 5120:
                raise Exception
        except Exception, e:
            print "skipping image with size (%s, %s), %s bytes" % (w,h,bytes)
            continue
        
        imgpath = os.path.join(filedir, filename)
        urlretrieve(full_image_uri, imgpath)
        didScrape = True
        imgindex = x+1
        print "scraped image index %s to file: %s" % (imgindex, imgpath)
        break

    return (filedir, filename, imgindex, (w,h)) if didScrape else ('', '', -1)

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
    filedir = ''
    if not url.lower().startswith("http"):
        filedir = sys.argv[-1]
        url = sys.argv[-2]
        if not url.lower().startswith("http"):
            _usage()
            sys.exit(-1)
    getImagesFromURL(url, filedir)
