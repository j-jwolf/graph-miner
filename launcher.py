import os, sys, subprocess
from utils import *
from json import loads

"""

launcher that will launch main.py after ensuring that the virtual environment containing the dependencies is installed

prints return values code in codes.json

!!! pass input file as argument to skip the file name verification in main.py --> ex: python launcher.py input.txt !!!

notes:
	replace os.system with subprocess

"""


def pout(command, processInput = None):
	if processInput is None: p = subprocess.run(command)
	else:
		p = subprocess.Popen(command, stdin = subprocess.PIPE)
		output = p.communicate(input = processInput.encode())[0]
	return p.returncode

quickInput = ""
if(len(sys.argv) > 1):
	count = 0
	while(quickInput == "" and count < len(sys.argv)):
		if(os.path.isfile(sys.argv[count]) and not sys.argv[count].endswith(".py")): quickInput = sys.argv[count]
		count += 1
	print(f"DEBUG --> quickInput: {quickInput}")
	#sys.exit()
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

#with open("codes.json") as file: codes = loads(file.read())
codes = readJSON("codes.json")
if(quickInput == ""): quickInput = None
ret = str(pout(f"{command} && {pycall} main.py", quickInput))

if ret in codes: print(codes[ret])
else: print(f"ERROR: RETURN VALUE {ret} NOT RECOGNIZED --> PLEASE DEFINE IT IN CODES.JSON WITH CODER.PY")
