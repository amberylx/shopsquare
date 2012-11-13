import sys, re
import unicodedata

def slugify(str):
    slug = unicodedata.normalize('NFKD', unicode(str))
    slug = slug.encode('ascii', 'ignore').lower()
    slug = re.sub(r'[^\w]+', '-', slug).strip('-')
    slug = re.sub(r'[-]+', '-', slug)
    return slug

_USAGE = \
""" 
Usage: %s [string to slugify]
"""

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print _USAGE % sys.argv[0]
        sys.exit(1)

    print sys.argv[1]
    print slugify(sys.argv[1])
