"""

Responsible for running the genetic algorithm and writing its results

Program arguments:
	flags:
		-min: minimum image output
		-quiet: minimum console output
		-silent: no console output other than results
	arguments:
		cutoff: tells the program how many generations to run [defaults to 1000]
	THESE ARE DOCUMENTED BETTER IN README.MD

"""

import os, sys, igraph, random
from utils import * # read/write file functions
from shutil import rmtree # for deleting previous data in results folder

class Individual:
	POP_SIZE = 100 # size of each generation
	# class method -> gets random edge from input file
	@classmethod
	def mutate(cls, edges): return random.choice(edges)
	# checks if path in individual goes from point a to point b
	def isValid(self): return isValidPath(self.__chromosome, self.__source, self.__target)
	# constructor -> c: chromosome, source: starting node, target: node to find path to
	def __init__(self, c, source, target):
		self.__chromosome = c
		self.__source = source
		self.__target = target
	def setChromosome(self, c): self.__chromosome = c
	def setSource(self, source): self.__source = source
	def setTarget(self, target): self.__target = target
	def getChromosome(self): return list(set(self.__chromosome))
	def getSource(self): return self.__source
	def getTarget(self): return self.__target
	# calculates the individuals fitness -> how many nodes in the path? lower == better
	def fitness(self):
		if(self.isValid()): return len(set(self.__chromosome))
		return sys.maxsize
	# crosses this individual with another, returns their child
	def crossover(self, other):
		global TARGET
		probs = [0.45, 0.9]
		child = list()
		for i in range(TARGET):
			weight = random.random()
			if(weight < probs[0]): child.append(random.choice(self.__chromosome)) # inherits one element from this individual
			elif(weight < probs[1]): child.append(random.choice(other.__chromosome)) # inherits one element from the other individual
			else: # gets a new mutation from the edge pool instead of inheriting
				weight = random.randint(0, 100)
				if(weight < 30): pass
				else: child.append(Individual.mutate(edges))
		return Individual(child, self.__source, self.__target)

# gets all the nodes in the path as a list
def getNodes(path):
	nodes = set()
	for tup in path:
		nodes.add(tup[0])
		nodes.add(tup[1])
	return list(nodes)
# checks if the only element remaining contains both the source and target nodes --> allows for cutoff to happen if the nodes share an edge
def checkSingle(edge, source, target): return source in edge and target in edge
# deprecated, checks if the remaining edges contain the source and target nodes --> allows for cutoff if the nodes share an edge and there are two solutions remaining
def checkDouble(edges, source, target):
	a = edges[0]
	b = edges[1]
	if source in a and target in a: return a
	if source in b and target in b: return b
	return None
# checks if the path contains both the source and target node --> cant be a valid path from a to b without a or b
def endpoints(path, source, target):
	found = False
	tofind = [False, False]
	count = 0
	while(count < len(path) and not found):
		if source in path[count]: tofind[0] = True
		if target in path[count]: tofind[1] = True
		found = tofind[0] and tofind[1]
		count += 1
	return found
# search through the path to see if it is a valid path from a to b --> is this a connected path to a from b?
def isValidPath(path, source, target):
	if(len(path) == 1 and checkSingle(path[0], source, target)): return True
	if(not endpoints(path, source, target)): return False
	current = source
	count = 0
	#while(current != target and count < len(path)):
	while(count < len(path)):
		for edge in path:
			if(current in edge):
				if(current == edge[0]): current = edge[1]
				else: current = edge[0]
		count += 1
	return current == target
# creates a new random genome for the initial population
def newGenome(edges):
	TARGET = random.randint(1, len(edges)) # how long should my genome be?
	genome = list()
	count = 0
	while(count < TARGET):
		genome.append(Individual.mutate(edges)) # add a random edge from all possible edges in input file
		count += 1
	return genome
# writes result to file in results directory named generation-[whatever the generation is]
def writeResult(graph, chromosome, count):
	sub = graph.subgraph(getNodes(chromosome))
	if(not os.path.isdir("results")): os.mkdir("results")
	fn = f"results{os.path.sep}generation-{count}.png"
	data = dict()
	data["bbox"] = (400, 400)
	data["margin"] = 30
	data["vertex_color"] = "white"
	data["vertex_size"] = 45
	data["vertex_label_size"] = 22
	data["edge_curved"] = False
	data["layout"] = graph.layout()
	igraph.plot(sub, fn, **data)
# gets user inputs for which nodes to find a path between
def getInputs():
	inputs = ["", ""]
	userInput = ""
	valid = False
	while(userInput != "e" and not valid):
		userInput = input("Enter source node or e to exit: ")
		if(userInput == "e"): pass
		else:
			try:
				x = int(userInput)
				if(x > -1):
					inputs[0] = x
					while(userInput != "e" and userInput == str(inputs[0]) and not valid):
						userInput = input("Enter target node or e to exit: ")
						if(userInput == "e"): pass
						elif(userInput == inputs[0]): print("Source node cannot be the target node")
						else:
							try:
								x = int(userInput)
								if(x > -1):
									inputs[1] = x
									valid = True
								else: print(f"{userInput} is not a valid positive integer")
							except KeyboardInterrupt: sys.exit(2)
							except ValueError: print(f"{userInput} is not a valid positive integer")
							except Exception as e: print(e)
				else: print(f"{userInput} is not a valid positive integer")
			except KeyboardInterrupt: sys.exit(2)
			except ValueError: print(f"{userInput} is not a valid positive integer")
			except Exception as e: print(e)
	if(userInput == "e"): sys.exit(1)
	return inputs

# setting flags
minMode = "-min" in sys.argv
quietMode = "-quiet" in sys.argv
silentMode = "-silent" in sys.argv

# getting input file name
inputFile = ""
while(not os.path.isfile(inputFile) and inputFile != "e"):
	inputFile = input("Enter input file name or e to exit: ")
	if(inputFile != "e" and not os.path.isfile(inputFile)): print(f"{inputFile} does not exist!")
if(inputFile == "e"): sys.exit(1)

# building the graph from input file
inputFile = "input.txt"
rawEdges = readFile(inputFile, True)
edges = list()
verts = set()
count = 0
vcount = 0
for line in rawEdges:
	if(count >= 2):
		tok = line.split(" ")
		tup = (int(tok[0]), int(tok[1]))
		edges.append(tup)
		verts.add(int(tok[0]))
		verts.add(int(tok[1]))
	else: pass
	count += 1

# deletes previous results
if(os.path.isdir("results")): rmtree("results")

# build the graph from input file
graph = igraph.Graph(directed = False)
graph.add_vertices(len(verts))
for i in range(len(verts)):
	graph.vs[i]["id"] = i
	graph.vs[i]["label"] = str(i)
graph.add_edges(edges)

# initializing GA variables
TARGET = len(edges) # number of edges in graph
CARRYOVER = 10 # percent of fittest individuals that makes it to the next generation
CROSSOVER = 50 # percent of fittest individuals whose children makes it to next generation

# getting inputs for the source and target nodes
inputs = getInputs()
source = inputs[0]
target = inputs[1]

print("")

cutoff = 1000 # what generation is the last generation, default value
# checking for argument with different valid cutoff value
for arg in sys.argv:
	if(arg.startswith("cutoff:")):
		try:
			x = int(arg.split(":")[-1])
			if(x > 0): cutoff = x
			else: print(f"Cutoff must be at least one --> using default {cutoff} instead")
		except KeyboardInterrupt: sys.exit(2)
		except Exception: print(f"Cutoff argument invalid --> using default {cutoff} instead")

# creating first generation
generation = 1
pop = list()
for _i in range(Individual.POP_SIZE): pop.append(Individual(newGenome(edges), source, target)) # generating first generation
lastBest = len(pop[0].getChromosome())

while(generation < cutoff and len(pop[0].getChromosome()) > 1):
	pop.sort(key = lambda entity : entity.fitness()) # sort population by fitness
	next = list() # initialize next generation
	# top ranking moves to next gen
	rank = int((CARRYOVER*Individual.POP_SIZE)/100)
	next.extend(pop[:rank])
	# crossing individuals over
	rank = int((CROSSOVER*Individual.POP_SIZE)/100)
	for _i in range(Individual.POP_SIZE-CARRYOVER):
		valid = False
		while(not valid):
			parents = [
				random.choice(pop[:CROSSOVER]),
				random.choice(pop[:CROSSOVER])
			]
			if(parents[0].fitness() != 0 and parents[1].fitness() != 0): valid = True
		child = parents[0].crossover(parents[1])
		next.append(child)
	# population is now the next generation
	pop = next
	pop.sort(key = lambda entity : entity.fitness())
	# checking if should write fittest path to image file
	if(not minMode or minMode and len(pop[0].getChromosome()) < lastBest): writeResult(graph, pop[0].getChromosome(), generation)
	# checking if this should print to console or not, depending on flags
	if(not silentMode):
		if(not quietMode): print(f"End of generation {generation+1}")
		elif(quietMode and (generation+1) % 100 == 0): print(f"End of generation {generation+1}")
	# updating last best fitness score
	lastBest = len(pop[0].getChromosome())
	generation += 1 # increment generation

# printing results to console
print("\n\n========================================================================================================================")
print("RESULTS")
print("========================================================================================================================\n")
print(f"Source: {source} --> Target: {target}")
print(f"Fittest individual after {generation} generations: {pop[0].fitness()}\n\nIts edges:")
for edge in pop[0].getChromosome(): print(f"\t{edge}")
print(f"\nResults of fittest individual were written to results{os.path.sep}")
