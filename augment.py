from shutil import copy
import imgaug as ia
from imgaug import augmenters as iaa
from imgaug.augmentables.bbs import BoundingBox, BoundingBoxesOnImage
from pathlib import Path
import cv2
from label_convert import YoloToReg,RegToYolo
from random import random

source_dir = Path('D_bg_r_blur_cutout_PerpectiveTransform')
target_dir = Path('D_bg_r_blur_cutout_PerpectiveTransform_Sharp')

if not target_dir.is_dir():
    target_dir.mkdir()
    Path(target_dir,'images').mkdir()
    Path(target_dir,'labels').mkdir()

ty = 'train'
for f in target_dir.iterdir():
    if not Path(f,ty).is_dir():
        Path(f,ty).mkdir()

ls_img = list(source_dir.glob('**/train/*.jpg'))
ls_lab = list(source_dir.glob('**/train/*.txt'))

ls_img = sorted(ls_img)
ls_lab = sorted(ls_lab)

seq = iaa.Sequential([
    # iaa.GaussianBlur(sigma=((1,2.5)))
    # iaa.Cutout(nb_iterations=(1, 10), size=0.15, squared=False)
    # iaa.Multiply((0.6,1.4))
    # iaa.PerspectiveTransform(scale=(0.01, 0.15))
    # iaa.TranslateX(percent=(-0.2, 0.2)),
    # iaa.TranslateY(percent=(-0.2, 0.2))
    # iaa.ScaleX((0.8, 1.3)),
    # iaa.ScaleY((0.8, 1.3))
    # iaa.MultiplyHueAndSaturation((0.8, 1.2), per_channel=True)
    iaa.Sharpen(alpha=(0.1, 0.5), lightness=(0.75, 1.0))
])

idx = 0

for img,lab in zip(ls_img,ls_lab):
    if img.stem != lab.stem:
        print('False')
        continue
    # idx+=1
    # if idx == 500:
    #     break
    if random()<0.85:
        copy(img, Path(target_dir,'images',ty,img.stem + '.jpg'))
        copy(lab, Path(target_dir,'labels',ty,lab.stem + '.txt'))
        continue
    idx+=1
    image = cv2.imread(str(img))
    with open(lab,'r') as f:
        lines = f.readlines()
    labels=[]
    bbs = BoundingBoxesOnImage([],shape=image.shape)
    for line in lines:
        cls,x,y,w,h = map(float,line.split())
        cls = int(cls)
        x1,y1,x2,y2 = YoloToReg(image,x,y,w,h)
        labels.append((cls,x1,y1,x2,y2))
        bbs.bounding_boxes.append(BoundingBox(x1,y1,x2,y2,cls))
    image_aug,bbs_aug = seq(image = image,bounding_boxes=bbs)

    new_img_path = Path(target_dir,'images',ty,'Sh_'+img.stem + '.jpg')
    cv2.imwrite(str(new_img_path),image_aug,[int(cv2.IMWRITE_JPEG_QUALITY), 95])
    
    new_lab_path = Path(target_dir,'labels',ty,'Sh_'+img.stem + '.txt')
    with open(new_lab_path,'w') as f:
        for bb in bbs_aug.bounding_boxes:
            x1,y1,x2,y2,cls = bb.x1,bb.y1,bb.x2,bb.y2,bb.label
            x1,y1,x2,y2 = RegToYolo(image_aug,x1,y1,x2,y2)
            f.write('{} {} {} {} {}\n'.format(cls,x1,y1,x2,y2))

    # cv2.imshow(str(new_img_path),image_aug)
    # cv2.waitKey(0)
    # break
print('number of augmented images: ',idx)