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

# process out --> runs command as process
def pout(command, processInput = None):
	p = subprocess.run(command)
	return p.returncode
# clears screen
def cls():
	try:
		if sys.platform in {"win32", "msys", "cygwin"}: os.system("cls")
		else: os.system("clear")
	except Exception as e: print(e) # just a precaution since this was not tested on mac or linux

cls()

print("========================================================================================================================\n")
print("HW3 -> Graph Miner by John Wolf and Dan Acosta")
print("\n========================================================================================================================")

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
	# virtual environment was not found
	newVenv = True
	os.system(f"{pycall} -m venv {venv}")
if(win): command = "app-env\\Scripts\\activate.bat" # windows command
else: command = "source app-env/bin/activate" # not windows command
if(newVenv):
	# new environment was created --> installing dependencies in it
	pout(f"{command} && {pycall} -m pip install --upgrade pip")
	depens = readFile("dependencies.gm", True)
	for d in depens: pout(f"{command} && {pycall} -m pip install {d}")

# gathering all arguments passed to this to pass to main.py
flags = ""
for arg in sys.argv:
	if(arg != __file__ and arg != "-debug"): flags += f" {arg}"

# run the program and get its return value
ret = pout(f"{command} && {pycall} main.py{flags}")

# these are pretty self explainatory
if(ret == 0): print("Exiting with no errors")
elif(ret == 1): print("User exited via menu")
elif(ret == 2): print("Exiting on keyboard interrupt")
else: print(f"Error code {ret} is undefined")
