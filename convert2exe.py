from distutils.core import setup
import py2exe

setup(
console=['export_excel.py'],
options = {
              'py2exe' : {
                      'packages' : ['xlsxwriter']
                      }
              }
)