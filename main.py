"""
main.py --> where the magic happens

to do:
	1. UI shit
		- add input for input file name, should be dynamic
		- add inputs for source and target nodes
		- (definitely john) document this better
		- run through print statements and determine what should stay
	2. other shit
		- idk yet

"""

import os, sys, igraph, random
from utils import *
from shutil import rmtree # for deleting previous data in results folder

class Individual:
	POP_SIZE = 100 # size of each generation
	# class method -> gets random edge from input file
	@classmethod
	def mutate(cls, edges): return random.choice(edges)
	# checks if path in individual goes from point a to point b
	def isValid(self):
		return isValidPath(self.__chromosome, self.__source, self.__target)
		global allPaths
		nodes = set()
		for tup in self.__chromosome:
			nodes.add(tup[0])
			nodes.add(tup[1])
		nodes = list(nodes)
		nodes.sort()
		#return nodes in allPaths or Individual.isSubset(nodes, allPaths)
		#if nodes in allPaths: return True
		global graph
		print(graph.get_subisomorphisms_vf2(graph.subgraph(nodes)))
		sys.exit()
	# checks if b is a subset of a (a: nodes, b: paths)
	@classmethod
	def isSubset(cls, nodes, paths):
		count = 0
		found = False
		a = set(nodes)
		while(count < len(paths) and not found):
			b = set(paths[count])
			if(b.issubset(a)): found = True
			count += 1
		if(not found): return found
		...
		return found
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
			if(weight < probs[0]): child.append(random.choice(self.__chromosome))
			elif(weight < probs[1]): child.append(random.choice(other.__chromosome))
			else: child.append(Individual.mutate(edges))
		return Individual(child, self.__source, self.__target)

#=========================================================================================== debugging shit ======================================================================================
class Node:
	def __init__(self, data, next):
		self.__data = data
		self.__next = next
	def setData(self, data): self.__data = data
	def setNext(self, next): self.__next = next
	def getData(self): return self.__data
	def getNext(self): return self.__next

class Stack:
	def __init__(self): self.__head = None
	def push(self, obj):
		if self.__headnext is None: next = None
		else: next = self.__head
		self.__head = Node(obj, next)
	def pop(self):
		if self.__head is None: return None
		data = self.__head.getData()
		self.__head = self.__head.getNext()
		return data
	def peek(self):
		if self.__head is None: return None
		return self.__head.getData()

class Writer:
	def __init__(self): self.__buffer = ""
	def append(self, s):
		if(type(s) != type("")):
			try: self.__buffer += str(s)
			except KeyboardInterrupt: sys.exit()
			except Exception: print(f"{s} is cannot be converted to string")
		else: self.__buffer += s
	def dump(self, fn):
		try:
			if(os.path.isfile(fn)): mode = "a"
			else: mode = "a"
			with open(fn, mode) as file: file.write(self.__buffer)
			self.__buffer = ""
			return True
		except KeyboardInterrupt: sys.exit()
		except Exception as e: print(e)
		return False
#=================================================================================================================================================================================================

#=============================================================================================== deprecated ======================================================================================
"""
def getRandom(p, weight):
	# p: population
	valid = False
	entity = None
	while(not valid):
		entity = random.choice(p[:weight])
		if(isValidPath(entity.getChromosome(), entity.getSource(), entity.getTarget())): valid = True
	return entity
def getMin(p):
	m = sys.maxsize
	index = 0
	count = 0
	for e in p:
		if(e.fitness() < m):
			m = e.fitness()
			index = count
		count += 1
	return p[index]
def checkSubset(target, paths):
	count = 0
	found = False
	a = set(target)
	while(count < len(paths) and not found):
		b = set(paths[count])
		if(b.issubset(a)): found = True
		count += 1
	return found
def checkPop(graph, pop):
	allPaths = graph.get_all_simple_paths(pop[0].getSource(), pop[0].getTarget())
	count = 0
	found = False
	writer = Writer()
	while(count < len(pop) and not found):
		# path = all nodes in path
		path = getNodes(pop[count].getChromosome())
		path.sort()
		if path in allPaths: found = True
		else: found = checkSubset(path, allPaths)
		writer.append(f"\n{path} in allPaths?: {found}")
		count += 1
	writer.dump("output.txt")
	return found
def writeAllPaths(paths):
	writer = Writer()
	writer.append("ALL PATHS:")
	for path in paths: writer.append(f"\n{str(path)}")
	writer.dump("output.txt")
	return
"""
#=================================================================================================================================================================================================

def getNodes(path):
	nodes = set()
	for tup in path:
		nodes.add(tup[0])
		nodes.add(tup[1])
	return list(nodes)
def isValidPath(path, source, target):
	current = source
	count = 0
	while(current != target and count < len(path)):
		for edge in path:
			if(current in edge):
				if(current == edge[0]): current = edge[1]
				else: current = edge[0]
		count += 1
	return current == target
def newGenome(edges):
	TARGET = random.randint(1, len(edges))
	genome = list()
	count = 0
	while(count < TARGET):
		genome.append(Individual.mutate(edges))
		count += 1
	return genome
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

if(os.path.isdir("results")): rmtree("results")

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
a = 0 # debug -> starting node
b = 14 # debug -> ending node
cutoff = 1000 # what generation is the last generation
generation = 1
pop = list()
for _i in range(Individual.POP_SIZE): pop.append(Individual(newGenome(edges), a, b)) # generating first generation

allPaths = graph.get_all_simple_paths(a, b) # getting all (simple?) paths from starting node to ending node

while(generation < cutoff):
	pop.sort(key = lambda entity : entity.fitness()) # sort population by fitness
	next = list()
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
	writeResult(graph, pop[0].getChromosome(), generation)
	print(f"End of generation {generation}")
	generation += 1 # increment generation

print(f"Fittest individual: {pop[0].fitness()}\nIts edges:")
for edge in pop[0].getChromosome(): print(f"\n{edge}")
print(f"Results of fittest individual were written to results{os.path.sep}")
