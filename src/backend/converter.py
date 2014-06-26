# converter.py
# Mathijs Saey
# DLC

# This module is responsible for the mapping
# of the various IGR elements to their DIS counterparts

import IGR

# ---------------- #
# Links & Literals #
# ---------------- #

def links(port, dis, map):
	srcC, srcK = map.getSrc(port.node)
	srcP = port.idx

	for port in port.targets:
		dstC, dstK = map.getDst(port.node)
		dstP = port.idx

		dis.addLink(srcC, srcK, srcP, dstC, dstK, dstP)

def literals(node, dis, map):
	chunk, key = map.getDst(node)

	for port in node.ports:
		if port.hasLit():
			dis.addLiteral(chunk, key, port.idx, port.src.val)

# ----- #
# Nodes #
# ----- #

def addNode(node, dis, map, chunk, type, args = []):
	key = dis.addInstruction(chunk, type, args)
	map.add(node, key, key)
	return key

def operation(n, d, m): addNode(n, d, m, 1, 'OPR', [n.op, n.args])
def constant(n, d, m):  addNode(n, d, m, 0, 'CNS', ["<=", n.val])

def call(n, d, m):
	dstC, dstK = m.getName(n.name)
	retC, retK = (0, d.currentKey(0) + 1)

	callKey = d.addInstruction(0, 'CHN', [n.args, 1, dstC, dstK, retC, retK])
	retKey  = d.addInstruction(0, 'SNK', [])

	m.add(n, retKey, callKey)

# --------- #
# Compounds #
# --------- #

def forN(n, d, m):
	key0 = d.currentKey(0)
	key1 = d.currentKey(1)
	splK = d.addInstruction(1, 'SPL', [n.args, 0, key0, 1, key1 + 1])
	snkK = d.addInstruction(0, 'SNK', [])
	retK = d.addInstruction(0, 'RST', [])
	mrgK = d.addInstruction(1, 'OPR', ['array', 0])

	d.indent += 1
	m.add(n.body, snkK, retK)
	subGraphs(n, d, m)
	d.indent -= 1

	m.add(n, mrgK, splK)
	

def ifN(n, d, m):
	key = d.currentKey(0)
	swiK = d.addInstruction(0, 'SWI', [0, key + 2, 0, key + 3])

	retK = d.addInstruction(0, 'SNK', [])
	elsK = d.addInstruction(0, 'SNK', [])
	thnK = d.addInstruction(0, 'SNK', [])

	d.indent += 1
	m.add(n.thn, thnK, retK)
	m.add(n.els, elsK, retK)
	subGraphs(n, d, m)
	d.indent -= 1

	m.add(n, retK, swiK)

# --------- #
# Compounds #
# --------- #

def subGraphs(graph, prog, map):
	nodes = []

	def nodeP(n, d, m): 
		node(n, d, m)
		nodes.append(node)

	def sgStart(sg, prog, map):
		prog.addCommentLines("Starting subgraph %s" % sg.name)
		if sg.isFunc(): funcGraph(sg, prog, map)

	def sgStop(sg, prog, map):
		prog.addNewlines()

		for port in sg.entry: links(port, prog, map)
		for node in sg: links(node.out, prog, map)
		for node in sg: literals(node, prog, map)
		prog.addCommentLines("Leaving subgraph %s" % sg.name)
		prog.addNewlines()
		del nodes[:]

	IGR.traverse(
		graph,
		lambda x : nodeP(x, prog, map),
		lambda x : sgStart(x, prog, map),
		lambda x : sgStop(x, prog, map),
		lambda x : None,
		lambda x : None,
		False
	)

# ------- #
# General #
# ------- #

converters = {
	IGR.OperationNode : operation,
	IGR.ConstantNode  : constant,
	IGR.CallNode      : call,
	IGR.ForNode       : forN,
	IGR.IfNode        : ifN
}

def node(node, dis, map):
	return converters[type(node)](node, dis, map)

def funcGraph(sg, dis, map):
	inKey  = dis.addInstruction(0, 'SNK', [])
	outKey = dis.addInstruction(0, 'RST', [])
	map.addName(sg.name, inKey)
	map.add(sg, inKey, outKey)