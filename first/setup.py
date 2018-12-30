# !/usr/bin/python
from distutils.core import setup
import py2exe
import sys, os, site, shutil, errno, time
site_dir = site.getsitepackages()[1]
include_dll_path = os.path.join(site_dir, "gnome")

gtk_dirs_to_include = ['etc', 'lib\\gtk-3.0', 'lib\\girepository-1.0',
                       'lib\\gio', 'lib\\gdk-pixbuf-2.0', 'share\\glib-2.0', 'share\\fonts',
                       'share\\icons', 'share\\themes\\Default', 'share\\themes\\HighContrast']

include_gi_path = os.path.join(site_dir, "gi")

gtk_dlls = []
tmp_dlls = []
cdir = os.getcwd()
dest_dir = os.path.join(cdir, 'dist')

sub_folder = ["export","import","config"]

for sub in sub_folder:
    sub_dir = os.path.join(dest_dir, sub)
    try:
        os.makedirs(sub_dir)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            pass

for dll in os.listdir(include_dll_path):
    if dll.lower().endswith('.dll'):
        gtk_dlls.append(os.path.join(include_dll_path, dll))
        tmp_dlls.append(os.path.join(cdir, dll))

for dll in gtk_dlls:
    shutil.copy(dll, cdir)

# shutil.copy("_gi.pyd", cdir)

def do_setup():
    setup(name="CorePyTools",
          version="2.0.2",
          description="CorePyTools",
          author="CorePart",
          url="http://www.nwsvmc.com/",
          author_email="admin@nwsvmc.com",
          maintainer="Core Part",
          maintainer_email="info@nwsvmc.com",
          data_files=[("config", ["config.json"])],
          # py_modules=["redstring"],
          windows=[
              {
                  'script': 'first.py',
                  "icon_resources": [(1, "corepytool.ico")],
                  "dest_base": "CorePyTools"
              }
          ],
          options={"py2exe": {
              "unbuffered": True,
              "compressed": True,
              "bundle_files": 3,
              'packages': ['gi','xlsxwriter','json'],
              # 'includes': ['gi','xlsxwriter','json'],
              'dll_excludes': [
                  'OLEAUT32.dll','USER32.dll', 'IMM32.dll', 'SHELL32.dll', 'KERNEL32.dll',
                  'WINMM.dll','COMDLG32.dll','ADVAPI32.dll','COMCTL32.dll','WS2_32.dll',
                  'GDI32.dll','RPCRT4.dll','ole32.dll','msvcrt.dll','ntdll.dll',
              ],
          }},
          # zipfile="shared.lib",
          zipfile=None,
          )

do_setup()
do_setup() #For apply icon

for dll in tmp_dlls:
    shutil.copy(dll, dest_dir)
    os.remove(dll)

for d in gtk_dirs_to_include:
    shutil.copytree(os.path.join(site_dir, "gnome", d),
                    os.path.join(dest_dir, d))


