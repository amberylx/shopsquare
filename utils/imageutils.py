from os.path import split,join
from PIL import Image

def crop_image(filedir, filename, box):
    imgpath = join(filedir, filename)
    img = Image.open(imgpath)
    cropped_area = img.crop(box)
    cropped_area.save(imgpath, 'jpeg')
    return (filedir, filename)

def resize_image(filedir, filename):
    max_width = 600
    imgpath = join(filedir, filename)
    img = Image.open(imgpath)
    (w,h) = img.size

    if w > max_width:
        new_height = int((float(max_width)*h)/w)
        img = img.resize((max_width,new_height), Image.ANTIALIAS)
        img.save(imgpath, 'jpeg')
        print "cropped image to (%s, %s)" % (max_width, new_height)
    return (filedir, filename)
    

if __name__ == "__main__":
    path = '/Users/slee/shopsquare/media/images/usrimg/tmp.jpg'
    crop_image(path, (130,0,260,390))
        
