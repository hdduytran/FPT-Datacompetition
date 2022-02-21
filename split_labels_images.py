from pathlib import Path
from shutil import move

d = Path(r'Dien_notest')
ls = list(d.glob('**/*.txt'))
for label in ls:
    move(label,Path(d,'labels',label.name))
