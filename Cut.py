from typing import overload
import cv2
from pathlib import Path
from label_convert import YoloToReg,RegToYolo

def cutRegion(img,x,y,h,w):
    x,y,h,w = map(int,(x,y,h,w))
    new_img = img[y:h,x:w,:]
    return new_img

def checkOverlap(lx1,ly1,rx1,ry1,lx2,ly2,rx2,ry2):
    ''' check if overlap    '''
    if (lx1 >rx2 or lx2>rx1 ):
        return False
    if ry1<ly2 or ry2<ly1:
        return False
    return True 

def cutImage(image_path, labels_path):
    img = cv2.imread(str(image_path))
    with open(labels_path,'r') as f:
        lines= f.readlines()
        if len(lines) > 50:
             return
        labels = []
        for line in lines:
            cls,x,y,w,h = map(float,line.split())
            x,y,w,h = YoloToReg(img,x,y,w,h)
            labels.append((cls,x,y,w,h))

        for label in labels:
            cls,x,y,w,h = label
            pw = (w-x) // 2
            ph = (h-y) // 2
            
            overlap = False
            for lb in labels:
                if lb == label:
                    continue
                _,xt,yt,wt,ht = lb
                if checkOverlap(xt,yt,wt,ht,x-pw,y-ph,w+pw,h+ph*5):
                    overlap = True
                    break
            if overlap:
                continue
            image = cutRegion(img,x-pw,y-ph,h+ph*5,w+pw)
            if image.size <=70000 or image.shape[0]<image.shape[1]:
                continue
            try:
                xn,yn,wn,hn = RegToYolo(image,pw,ph,pw+pw*2,ph+ph*2)
                # xn,yn,wn,hn = getObjectRegion(image,xn,yn,wn,hn)
                # cv2.rectangle(image, (xn, yn), (wn, hn), (0, 0, 255), 1)
                global idx_new
                idx_new+=1
                correct_classes = [2,1,0] #sunplus
                # correct_classes = [0,1,2] #other
                cls = correct_classes[int(cls)]
                new_image_path = Path(target_dir,str(cls), 'images', str(idx_new)+'.jpg')
                new_label_path = Path(target_dir,str(cls),'labels' , str(idx_new)+'.txt')
                cv2.imwrite(str(new_image_path),image)
                with open(str(new_label_path),'w') as ff:
                    ff.write(f'{cls} {xn} {yn} {wn} {hn}')
            except Exception:
                print(Exception)

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

target_dir = Path(r'cut_split')
source_dir = Path(r'Sunplus')

idx_new = findIdx()
    
for img in Path(source_dir,'images').iterdir():
    if img.suffix in ['.jpg','.png','.jpeg']:
        try:
            label = Path(source_dir,'labels',img.stem+'.txt')
            cutImage(str(img),str(label))
        except Exception:
            print(Exception)