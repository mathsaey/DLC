# __init__.py
# Mathijs Saey
# DLC

# This package contains a few optimizations

import IGR
from autoinline import inline


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