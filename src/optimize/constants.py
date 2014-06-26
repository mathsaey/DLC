# constants.py
# Mathijs Saey
# DLC

# This module is responsible for the elimination
# of nodes that only accept literals.

import backend
import IGR

def isLit(node):
	for port in node.ports:
		if not port.hasLit():
			return False
	return True

def getVal(node):
	targets = node.out.targets
	values = [port.src.val for port in node.ports]
	for port in node.ports: port.src = None
	node.out.targets = []

	dis = backend.convert(node.sg.func.graph, linkTo = node)
	res = backend.run(values, dis)
	node.out.targets = targets
	return res

def propagate(node, val):
	lit = IGR.Literal(val, node.out.typ)
	for target in node.out: 
		lit.bind(target)
	for port in node.ports: 
		if port.src: port.src.removeBound(port)
	node.remove()

def node(node):
	if node.isCall():
		func = node.sg.func.graph[node.name]
		if func.exit.hasLit(): return propagate(node, func.exit.src.val)
	if isLit(node):
		val = getVal(node)
		propagate(node, val)

def sg(sg):
	if sg.isFunc() or not sg.exit.hasLit(): return
	node = IGR.ConstantNode(sg, sg.exit.src.val)
	node.out.bind(sg.exit)
	sg.entry[0].bind(node[0])

def remove(graph):
	IGR.traverse(graph,
		lambda x : node(x),
		lambda x : None,
		lambda x : sg(x),
		lambda x : None,
		lambda x : None
	)