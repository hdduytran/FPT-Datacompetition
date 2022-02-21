from pathlib import Path
import cv2
import shutil
for clss in '012':
    source = Path(r'cut_split/'+clss)
    target = Path(r'cut_split_flip/'+clss)

    for img_path in Path(source, 'images').iterdir():
            img = cv2.imread(str(img_path))
            # w, h = img.shape[:2]
            # img = cv2.resize(img, (int(640/w*h), 640))
        

            cv2.imwrite(str(Path(target, 'images', img_path.name)), img)
            shutil.copyfile(str(Path(source, 'labels', img_path.stem + '.txt')), str(Path(target, 'labels', img_path.stem + '.txt')))
            
            flip_img = cv2.flip(img, 1)
            flip_label = []
            cv2.imwrite(str(Path(target, 'images', img_path.stem + '_flip.jpg')), flip_img)

            with open(Path(source, 'labels', img_path.stem + '.txt'), 'r') as f:
                lines = f.readlines()
                for line in lines:
                    cls, x, y, w, h = line.split()
                    x = 1 - float(x)
                    new_label = ' '.join([cls, str(x), y, w, h])
                    flip_label.append(new_label)

            with open(Path(target, 'labels', img_path.stem + '_flip.txt'), 'w') as f:
                for new_label in flip_label:
                    f.write(new_label + '\n')

