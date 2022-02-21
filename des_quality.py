from pathlib import Path
from shutil import copy,copytree,ignore_patterns
import cv2

source_dir = Path('augv5')
target_dir = Path( f'{source_dir.stem}_low')

if not target_dir.is_dir():
    # target_dir.mkdir()
    copytree(source_dir,target_dir,ignore=ignore_patterns('train'))
    Path(target_dir,'images','train').mkdir()
    Path(target_dir,'labels','train').mkdir()

ls_img = list(source_dir.glob('**/train/*.jpg'))
ls_lab = list(source_dir.glob('**/train/*.txt'))

ls_img = sorted(ls_img)
ls_lab = sorted(ls_lab)

for img,lab in zip(ls_img,ls_lab):
    if img.stem != lab.stem:
        print('False')
        continue
    image = cv2.imread(str(img))
    new_img = Path(target_dir,'images','train',img.name)
    cv2.imwrite(str(new_img),image,[int(cv2.IMWRITE_JPEG_QUALITY), 95])

    new_lab = Path(target_dir,'labels','train',lab.name)
    copy(lab,new_lab)
