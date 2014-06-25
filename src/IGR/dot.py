# dot.py
# Mathijs Saey
# DLC

# This module allows us to generate
# a DOT graph of our graph representation
# Based on dot generator from DVM

import sys
import graph
import StringIO
import subprocess

from traverse import traverse

# -------- #
# Compound #
# -------- #

def compoundHeader(buffer, node):
	name = str(node.id)
	buffer.write("subgraph cluster_compound_" + name + " {\n")
	buffer.write("label = compound_" + name + "\n")
	buffer.write("graph [pencolor = black, bgcolor = lightgrey]\n")

def compoundFooter(buffer, node):
	buffer.write("}\n")

# ----- #
# Ports #
# ----- #

def portStr(port, pref):
	if port.isBound() and port.typ: label = port.typ.__name__
	elif port.isBound(): label = '*'
	else: label = ''

	return "<%s%d>%s" % (pref, port.idx, label)

def inPortStr(port):
	if port.hasLit(): return str(port.src.val)
	else: return portStr(port, 'I')
	
def outPortStr(port):
	return portStr(port, 'O')

def portLst(lst, fn):
	str = '|'.join([fn(port) for port in lst])
	return "{%s}" % str

def inputStr(ports):
	return portLst(ports, inPortStr) + '|'

def outputStr(ports):
	return '|' + portLst(ports, outPortStr)


# ----- #
# Edges #
# ----- #

def getId(target, isSrc):
	if isinstance(target.node, graph.SubGraph):
		name = "%s_%s" % (target.node.name, 'in' if isSrc else 'out')
	else: name = str(target.node.id)
	return "%s : %s%d" % (name, 'O' if isSrc else 'I', target.idx)

def edges(buffer, port):
	for target in port:
		buffer.write("%s -> %s ;\n" % (getId(port, True), getId(target, False)))

# --------- #
# Subgraphs #
# --------- #

def subGraphHeader(buffer, subGraph):
	name = subGraph.name.replace(".", "_")
	buffer.write("subgraph cluster_" + name + " {\n")
	buffer.write("label = " + name + "\n")
	buffer.write("graph [pencolor = black, bgcolor = white]\n")
	buffer.write('%s_in[label="{%s_in%s}"];\n' % (subGraph.name, subGraph.name, outputStr(subGraph.entry)))
	for port in subGraph.entry: edges(buffer, port)

def subGraphFooter(buffer, subGraph):
	port = subGraph.exit
	buffer.write('%s_out[label="{%s%s_out}"];\n' %  (subGraph.name, inputStr((port,)), subGraph.name))
	buffer.write("}\n")

# ----- #
# Nodes #
# ----- #

def nodeLabel(buffer, node):
	buffer.write(str(node.id))
	buffer.write(' [')
	buffer.write('label="' + '{' + inputStr(node.ports) + str(node) + outputStr((node.out,)) + '}"')
	if node.isCompound():  buffer.write("style = filled, fillcolor = lightgrey")
	if node.isCall():      buffer.write("style = dashed")
	buffer.write('];\n')

def nodeLinks(buffer, node):
	for target in node.out:
		if isinstance(target.node, graph.SubGraph):
			buffer.write("%s -> %s_out;\n" % (str(node.id), node.sg.name))
		else:
			buffer.write("%s : O ->  %s : I%d;\n" % (
				str(node.id), str(target.node.id), target.idx))

def writeNode(buffer, node):
	nodeLabel(buffer, node)
	edges(buffer, node.out)

# --- #
# Dot #
# --- #

def dotHeader(buffer):
	buffer.write("digraph IGR {\n")
	buffer.write("graph [compound=true];\n")
	buffer.write("node [shape=record];\n")

def dotFooter(buffer):
	buffer.write("}")

def getDot(graph, buffer = None):
	buffer = StringIO.StringIO()
	dotHeader(buffer)

	traverse(
		graph,
		lambda x : writeNode(buffer, x),
		lambda x : subGraphHeader(buffer, x),
		lambda x : subGraphFooter(buffer, x),
		lambda x : compoundHeader(buffer, x),
		lambda x : compoundFooter(buffer, x)
		)

	dotFooter(buffer)
	str = buffer.getvalue()
	buffer.close()
	return str

def dotToFile(path, graph):
	f = open(path, 'w')
	f.write(getDot(graph))
	f.close()

def dot(
	graph,
	dotpath = "dot",
	path = "igr.dot", 
	format = "png", 
	output = "", 
	other = [], 
	):

	dotToFile(path, graph)

	format = "-T" + format

	if output: output = "-o" + output
	else: output = "-O"

	try:
		subprocess.check_call([dotpath, format, path, output] + other)
	except subprocess.CalledProcessError, e:
		print >> sys.stderr, "Dot returned with exit code %d" % e.returncode
	except OSError:
		print >> sys.stderr, "Dot executable not found"
