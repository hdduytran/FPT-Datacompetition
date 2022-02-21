import os
from pathlib import Path

dr = Path(r'background')
ls = list(dr.glob('**/*.jpg'))

def rename():
    for img in ls:
        os.rename(img,str(Path(dr,'bg'+img.name)))

def create_label():
    for img in ls:
        label = Path(dr,'labels',img.stem+'.txt')
        with open(label,'w') as f:
            f.write('')

create_label()