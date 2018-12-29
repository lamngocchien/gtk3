from distutils.core import setup
import py2exe, sys, os

sys.argv.append('py2exe')

setup(
    options = {'py2exe': {'bundle_files': 3, 'compressed': True,
                          'packages': ['gi','cairo','pango','pangocairo','atk','gobject','gio','gtk.keysyms','xlsxwriter','json'],}},
    windows = [{'script': "demo.py"}],
    zipfile = None,
)