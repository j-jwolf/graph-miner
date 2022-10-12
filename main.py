import os, sys, igraph
from utils import *

"""
def readFile(fn, lines = None):
	# reads a file, if lines is True: reads file by line, else read as string
	if not lines in {True, False}: lines = False
	data = None
	try:
		with open(fn) as file:
			if(lines): data = file.readlines()
			else: data = file.read()
	except Exception as e: print(e)
	return data
"""

def line(): return f"\n{'='*50}\n" # for formatting

try:
	graph = igraph.Graph(directed = False)

	userInput = ""
	while(userInput != "e" and not os.path.isfile(userInput)):
		userInput = input("Enter input file name or 'e' to exit: ")
		if(userInput != "e" and not os.path.isfile(userInput)): print(f"{userInput} is not a valid file")

	if(userInput == "e"): sys.exit(1)

	rawEdges = readFile("input.txt", True)
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
