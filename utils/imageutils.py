from os.path import split,join
from PIL import Image

def crop_image(imgpath, box):
    (imgpath_dir, imgpath_file) = split(imgpath)
    new_path = join(imgpath_dir, "cropped_%s"%imgpath_file)
    img = Image.open(imgpath)
    cropped_area = img.crop(box)
    cropped_area.save(new_path, 'jpeg')
    return new_path

if __name__ == "__main__":
    path = '/Users/slee/shopsquare/media/images/usrimg/tmp.jpg'
    crop_image(path, (130,0,260,390))
        
