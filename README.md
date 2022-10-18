# Graph Miner - HW 3
## John Wolf and Dan Acosta

## Table of Contents
1. Instructions
2. Directory Contents
3. Dependencies

### 1. Instructions
**ONLY RUN LAUNCHER.PY**

Make sure you do not install a virtual environment. launcher.py will install the venv and the dependencies

#### Configuring the Environment
1. Default Mode
2. Flags
3. Arguments

##### 1. Default Mode
The program will print to the console every time a generation has ended. It will also write the fittest path from the source to the target into an image file in the results directory

##### 2. Flags
There are 3 flags that this program accepts as arguments. Flags are denoted by starting with -

1. -min
	- This flag will have the program only write image files if the fitness level has changed between generations. Minimizes the clutter in the results directory
2. -quiet
	- This flag has the program only print at the end of every 100 generations. Much less output in stdout
3. -silent
	- This flag has the genetic algorithm run without printing anything to the console.
	- **If you pass both -quiet and -silent, this will be the mode it runs in**

##### 3. Arguments
There is currently 1 argument that is taken. Arguments are denoted with nameOfVariable:valueOfVariable

1. cutoff
	- The maximum number of generations that the algorithm should do. If nothing is passed, defaults to 1000
	- Example: `python launcher.py cutoff:2000`

### 2. Directory Contents

#### Python Files
1. Launcher.py
	- Installs virtual environment and its dependencies and prints defined exit codes from main.py
2. Main.py
	- File that the main program will be run on
3. Utils.py
	- File containing utility functions, ie. readFile, writeFile

#### Data Files
1. Dependencies.gm
	- File containing the list of dependencies this application has. Make sure to update it if a new dependency is needed
2. Input.txt
	- File containing the input Dr. Kim gave us. Can be named anything, program asks for the name at run time

### 3. Dependencies
**DEPENDENCIES CAN ONLY BE INSTALLED VIA PIP**

1. igraph
	- Used to make graphs
2. pycairo
	- Used for writing graphs to an image file
