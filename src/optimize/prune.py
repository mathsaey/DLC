# prune.py
# Mathijs Saey
# DLC

# This optimization removes unbound nodes
# from the program

import IGR

def node(x):
	if not x.out.isBound():
		x.sg.delNode(x)
		for port in x.ports:
			port.src.removeBound(port)
		prune(x.sg.func.graph)

def prune(graph):
	IGR.traverse(
		graph,
		lambda x : node(x),
		lambda x : None,
		lambda x : None,
		lambda x : None,
		lambda x : None
	)