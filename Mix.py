from math import radians
import cv2
from pathlib import Path
from random import random,randint,choice
from label_convert import YoloToReg,RegToYolo
def checkOverlap(lx1,ly1,rx1,ry1,lx2,ly2,rx2,ry2):
    ''' check if overlap    '''
    if (lx1 >rx2 or lx2>rx1 ):
        return False
    if ry1<ly2 or ry2<ly1:
        return False
    return True 

def allBackgroundLabels(img_background, label_background):
    labels = []
    with open(label_background,'r') as f:
        lines = f.readlines()
    for line in lines:
        cls,x,y,w,h = map(float,line.split())
        labels.append((cls,x,y,w,h))
    return labels

def MixImage(img_background,img_patch,labels,label_patch_path):
    h,w,_ = img_patch.shape
    h_background, w_background, _ = img_background.shape
    scale = 0
    if h>h_background:
        scale = h/h_background
    elif w > w_background/8 :
        scale = 200/w
    scale = scale + 1 + random()
    h,w = int(h/scale), int(w/scale)
    # print('w ',w,'w_ba ',w_background - w -1)
    # print('h ',h,'h_ba ',h_background - h -1)

    h_start = randint(0,h_background - h -1)
    w_start = randint(0,w_background - w -1)

    #check if patching overlap with background bb
    for label in labels:
        _,xbb,ybb,wbb,hbb = label
        xbb,ybb,wbb,hbb = YoloToReg(img_background,xbb,ybb,wbb,hbb)
        if checkOverlap(w_start,h_start,w+w_start,h+h_start,xbb,ybb,wbb,hbb):
            return labels

    img_patch = cv2.resize(img_patch,(w,h))
    img_background[h_start:h+h_start,w_start:w+w_start,:]=img_patch

    with open(label_patch_path, 'r') as f:
        cls,xpb,ypb,wpb,hpb = map(float,f.readline().split())
    ypb = (h_start+h*ypb)/h_background
    xpb =(w_start+w*xpb)/w_background
    wpb = w/w_background * wpb
    hpb = h/h_background * hpb

    labels.append((cls,xpb,ypb,wpb,hpb))

    # xpb,ypb,wpb,hpb = YoloToReg(img_background,xpb,ypb,wpb,hpb)
    # cv2.rectangle(img_background,(xpb,ypb),(wpb,hpb),(255,0,0),1)
    # cv2.imshow('1',img_background)
    # cv2.waitKey(0)
    return labels

def findIdx():
    img_names = list(target_dir.glob(r'**/*.jpg'))
    # find idx to name generated
    idx_new = 0

    for img in img_names:
        try:
            if int(img.stem) > idx_new:
                idx_new = int(img.stem)
        except:
            print('image name er')
    return idx_new

background_dir = Path(r'dataset_flip_resize')
patch_dir = Path(r'cut_split_flip')
target_dir = Path(r'cutmix_20')

idx_new = findIdx()

for img_background in Path(background_dir,'images').iterdir():
    print(idx_new)
    if img_background.suffix in ['.jpg','.png','.jpeg']:
        try:
            img_br = cv2.imread(str(img_background))
            label_background_path = Path(background_dir,'labels',img_background.stem+'.txt')

            labels = allBackgroundLabels(img_background,label_background_path)

            for num_patches in range(randint(1,2)):
                cls_choice = choice('000222222')
                patches_list = list(Path(patch_dir,cls_choice,'images').iterdir())
                img_patch_path = choice(patches_list)
                label_patch_path = Path(patch_dir,cls_choice,'labels',img_patch_path.stem +'.txt')
                img_patch = cv2.imread(str(img_patch_path))
                labels = MixImage(img_br,img_patch,labels,label_patch_path)
            idx_new+=1
            new_image_path = Path(target_dir,'images',str(idx_new) +'.jpg')
            new_label_path = Path(target_dir,'labels',str(idx_new) +'.txt')

            cv2.imwrite(str(new_image_path),img_br,[int(cv2.IMWRITE_JPEG_QUALITY), 95])
            with open(str(new_label_path),'w') as ff:
                for label in labels:
                    cls, xn, yn, wn, hn= label
                    ff.write(f'{int(cls)} {xn} {yn} {wn} {hn}\n')
        except Exception:
            print(Exception)