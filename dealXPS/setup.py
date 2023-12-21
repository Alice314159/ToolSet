# setup.py

from distutils.core import setup
import glob
import py2exe

setup(console=['main.py','readPages.py'])


# setup(console=["myscript.py"],
#        data_files=[("bitmaps",
#                     ["bm/large.gif", "bm/small.gif"]),
#                    ("fonts",
#                     glob.glob("fonts\\*.fnt"))],
# )