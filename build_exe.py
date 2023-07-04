import os
import distutils.dir_util

os.system("pyinstaller main.py --onefile --noconsole")
distutils.dir_util.copy_tree("./assets", "./dist/assets")
