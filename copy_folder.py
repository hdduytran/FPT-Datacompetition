from shutil import copytree
from pathlib import Path
source_dir = Path('D_bg_r')
target_dir = Path('D_bg_r_blur')

if not target_dir.is_dir():
    target_dir.mkdir()
    Path(target_dir,'images').mkdir()
    Path(target_dir,'labels').mkdir()

copytree(Path(source_dir,'images','val'),Path(target_dir,'images','val'))
copytree(Path(source_dir,'labels','val'),Path(target_dir,'labels','val'))

