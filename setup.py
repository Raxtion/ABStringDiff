import sys
from cx_Freeze import setup, Executable

build_exe_options = {'optimize':2, 'includes':['function_class.py', 'CCC.ico']}

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

executables = [
    Executable(script='Start.py',
               base=base,
               targetName='pyABDifference.exe',
               compress=True,
               icon='CCC.ico')]

setup(name='pyABDifference',
      version='0.2',
      description='Compare data in input_A and input_B',
      executables=executables,
      options={'build.exe': build_exe_options}
      )
