import os, sys, subprocess
from utils import *
from json import loads

"""

launcher that will launch main.py after ensuring that the virtual environment containing the dependencies is installed

prints return values code in codes.json

notes:
	replace os.system with subprocess

"""


def pout(command): return os.system(command)

venv = "app-env"
newVenv = False
if sys.platform in {"win32", "msys", "cygwin"}:
	# windows
	win = True
	pycall = "python"
else:
	# not windows
	win = False
	pycall = "python3"
if(not os.path.isdir(venv)):
	newVenv = True
	os.system(f"{pycall} -m venv {venv}")
if(win): command = "app-env\\Scripts\\activate.bat" # windows
else: command = "source app-env/bin/activate" # not windows
if(newVenv):
	pout(f"{command} && {pycall} -m pip install --upgrade pip")
	depens = readFile("dependencies.gm", True)
	for d in depens: pout(f"{command} && {pycall} -m pip install {d}")

with open("codes.json") as file: codes = loads(file.read())
ret = str(pout(f"{command} && {pycall} main.py"))

if ret in codes: print(codes[ret])
else: print(f"ERROR: RETURN VALUE {ret} NOT RECOGNIZED --> PLEASE DEFINE IT IN CODES.JSON")
