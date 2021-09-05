import sys
from cx_Freeze import setup, Executable

build_exe_options = {'include_files': ['SFLIU220', 'SFGE.bmp'], "excludes": ["tkinter"]}


setup(
    name ='SFPygame',
    author='rdn',
    version = '1.0',
    options={'build_exe': build_exe_options},
    executables = [Executable('SFPygame.py', base = 'Win32GUI',icon = 'SFGE.ico')])




#in command line(cmd)  change to current directory(cd) and write: "setup.py build" or "setup.py build_exe"
