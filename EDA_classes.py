from pathlib import Path

dir = Path(r'augv2')

images = list(dir.glob(r'**/train/*.jpg'))
labels = {label.stem: label for label in list(dir.glob(r'**/train/*.txt'))}

classes =[0,0,0]
for img in images:
    with open(labels[img.stem],'r') as f:
        lines = f.readlines()
    for line in lines:
        cls = line[0]
        classes[int(cls)] +=1
for i,cls in enumerate(classes):
    print(f'{i}: {cls}')