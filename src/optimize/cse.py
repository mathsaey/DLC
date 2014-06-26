# cse.py
# Mathijs Saey
# DLC

# This module implements common subexpression elimination
# It does this by looking for nodes with identical inputs and operations.

import IGR

didChange = True

def setChange():
	global didChange
	didChange = True

def resetChange():
	global didChange
	didChange = False

def common(n1, n2):
	if n1 is n2: return
	elif n1.args is not n2.args: return
	elif type(n1) is not type(n2): return
	elif n1.isCall() and n1.name != n2.name: return
	elif n1.isOp() and n1.op != n2.op: return
	elif n1.isCompound(): return

	for p1, p2 in zip(n1.ports, n2.ports):
		if p1.hasLit() and p2.hasLit() and p1.src.val != p2.src.val: return
		elif not p1.hasLit() and p1.src != p2.src: return
	return True

def replace(n1, n2):
	for target in n2.out.targets:
		n1.out.bind(target)
	for port in n2.ports:
		port.src.removeBound(port)
	n2.remove()

def hasCommon(node, lst):
	for el in lst:
		if common(node, el): 
			replace(node, el)
			setChange()

def node(node):
	hasCommon(node, node.sg)

def eliminate(graph):
	while didChange:
		resetChange()
		IGR.traverse(
			graph,
			node,
			lambda x : None,
			lambda x : None,
			lambda x : None,
			lambda x : None
		)