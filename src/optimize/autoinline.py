# calls.py
# Mathijs Saey
# DLC

# This optimization autmatically inlines non-recursive
# functions that match one of the following properties:
#	- They return a constant
#	- They are called less than a given threshold
# The optimization also removes unused subgraphs from the program.

import IGR

INLINE_THRESHOLD = 2

def node(node, dct):
	if node.isCall() and not node.isRec:
		lst = dct[node.name]
		lst.append(node)
		dct.update({node.name : lst})

def findCalls(graph, dct):
	IGR.traverse(
		graph,
		lambda x : node(x, dct),
		lambda x : None,
		lambda x : None,
		lambda x : None,
		lambda x : None
	)

def insert(graph, sg, node):
	node.sg.nodes += sg.nodes
	out = sg.exit.src
	out.removeBound(sg.exit)
	out.bindMany(node.out.targets)

	for i in xrange(0, node.args):
		port = sg.entry[i]

		for target in port:
			node[i].src.bind(target)
		for port in node.ports:
			port.src.removeBound(port)

	node.remove()

def checkCalls(graph, dct):
	didChange = False
	for (name, lst) in dct.iteritems():
		if   name == 'main': continue
		elif len(lst) == 0: 
			graph.delSubGraph(name)
			didChange = True

		elif graph[name].isRec: continue

		elif len(lst) <= INLINE_THRESHOLD or graph[name].args is 0:
			for node in lst: 
				insert(graph, graph[name], node)
				didChange = True

	return didChange

def inline(graph):
	didChange = True
	while didChange:
		callDct = {key : [] for key in graph.functions.iterkeys()}
		findCalls(graph, callDct)
		didChange = checkCalls(graph, callDct)
