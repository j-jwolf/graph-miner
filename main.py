import os, sys, igraph
from utils import *

vars = readJSON("vars.json") # global variables --> easier to change a json file than to dig through code. contains information about genetic algorithm specifically

class Entity:
	def __init__(self, c): self.__chromosome = c
	def setChromosome(self, c): self.__chromosome = c # chromosome setter
	def getChromosome(self): return self.__chromosome # chromosome getter
	def getFitness(self, t):
		# gets the fitness of current entity --> how close am i to the target?
		fitness = 0
		for a, b in zip(self.__chromosome, t):
			if(a != b): fitness += 1
		return fitness
	def mutate(self, g): return random.choice(g) # get a mutation (random new char from gene pool)
	def newGenome(self, t):
		# gets a new genome sequence
		g = list()
		for i in range(len(t)): g.append(self.mutate())
		return g
	def nextGen(self, other):
		# gets child of this and other
		global vars
		c = list()
		for a, b in zip(self.chromosome, other.chromosome):
			weight = random.random()
			if(weight < vars["LOWER_BOUND"]): c.append(a)
			elif(weight < vars["UPPER_BOUND"]): c.append(b)
			else: c.append(self.mutate())
		return Entity(c)


def line(): return f"\n{'='*50}\n" # for formatting

try:
	graph = igraph.Graph(directed = False)

	userInput = ""
	while(userInput != "e" and not os.path.isfile(userInput)):
		userInput = input("Enter input file name or 'e' to exit: ")
		if(userInput != "e" and not os.path.isfile(userInput)): print(f"{userInput} is not a valid file")

	if(userInput == "e"): sys.exit(1)
	subsetFile = userInput

	rawEdges = readFile("input.txt", True)
	subset = readFile(subsetFile)
	edges = list()
	count = 0
	vCount = 0
	verts = set()

	# read in existing edges, gets number of vertices from this data using a set
	for line in rawEdges:
		if(count >= 2):
			tok = line.split(" ")
			tup = (int(tok[0]), int(tok[1]))
			edges.append(tup)
			verts.add(int(tok[0]))
			verts.add(int(tok[1]))
		else: pass
		count += 1

	# prints vertices in this graph
	print(f"printing {len(verts)} vertices")
	for vert in verts: print(vert)

	# prints edges in this graph
	print(f"\n\nprinting {len(edges)} edges")
	for edge in edges: print(edge)

	# adding vertices to graph and labeling them
	graph.add_vertices(len(verts))
	for i in range(len(graph.vs)):
		graph.vs[i]["id"] = i
		graph.vs[i]["label"] = str(i)

	graph.add_edges(edges)

	# delete me -- this is for viewing that the graph information is correct
	vs = {}
	output = "test.png"
	vs["bbox"] = (400, 400)
	vs["margin"] = 27
	vs["vertex_color"] = "white"
	vs["vertex_size"] = 45
	vs["vertex_label_size"] = 22
	vs["edge_curved"] = False
	layout = graph.layout()
	vs["layout"] = layout
	igraph.plot(graph, output, **vs)
except KeyboardInterrupt: sys.exit(-2)
except Exception as e:
	print(e)
	sys.exit(-1)
