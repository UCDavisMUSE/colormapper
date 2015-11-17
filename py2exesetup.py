from distutils.core import setup
import py2exe
import numpy as np

setup(
    options = {
            "py2exe":{
            "dll_excludes": ["MSVCP90.dll", "HID.DLL", "w9xpopen.exe"],
        }
    },
    windows = [{'script': 'colormapper.py'}]
)
