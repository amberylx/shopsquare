from os.path import split,join
from PIL import Image

def crop_image(imgpath, box):
    (imgpath_dir, imgpath_file) = split(imgpath)
    new_imgfile = "cropped_%s" % imgpath_file
    new_path = join(imgpath_dir, new_imgfile)
    img = Image.open(imgpath)
    cropped_area = img.crop(box)
    cropped_area.save(new_path, 'jpeg')
    return new_imgfile

def resize_image(out_folder, filename):
    imgpath = "%s%s" % (out_folder, filename)
    max_width = 600
    img = Image.open(imgpath)
    (w,h) = img.size

    if w > max_width:
        new_height = int((float(max_width)*h)/w)
        img = img.resize((max_width,new_height), Image.ANTIALIAS)
        img.save("%s%s"%(out_folder,filename), 'jpeg')
        print "cropped image to (%s, %s)" % (max_width, new_height)
    return (out_folder, filename)
    

if __name__ == "__main__":
    path = '/Users/slee/shopsquare/media/images/usrimg/tmp.jpg'
    crop_image(path, (130,0,260,390))
        
