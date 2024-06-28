

from distutils.core import setup
import py2exe
import os
import sys

# Ensure the virtual environment paths are included
venv_path = os.path.join(os.path.dirname(sys.executable), 'Lib', 'site-packages')
sys.path.append(venv_path)
print(sys.path)

setup(
    name='pdf_merger',
    version='0.1',
    options={
        'py2exe': {
            'bundle_files': 1,
            'compressed': True,
            'includes': ['pdf_merger.py'],  # Explicitly include your script
            'excludes': ['__main__', 'posix', 'java', 'org.python', '_frozen_importlib', '_frozen_importlib_external', 'posixshmem', 'winreg', 'asyncio.DefaultEventLoopPolicy', 'dummy.Process', 'java.lang', 'org.python.core', 'os.path', 'tracemalloc', 'unittest', 'unittest.util', 'pep517', 'readline', 'resource'],
        }
    },
    console=['pdf_merger.py'],
    zipfile=None,
)

