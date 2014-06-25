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

# --------- #
# Subgraphs #
# --------- #

##
# Add the attributes of the subgraph.
##
def subGraphHeader(buffer, subGraph):
	name = subGraph.name.replace(".", "_")
	buffer.write("subgraph cluster_" + name + " {\n")
	buffer.write("label = " + name + "\n")
	buffer.write("graph [pencolor = black, bgcolor = white]\n")

	label = '|'.join([
		"<I%d>%s" % (i, '*' if subGraph.entry[i].isBound() else '') for i in xrange(0,subGraph.args)])

	for i in xrange(0, len(subGraph.entry)):
		port = subGraph.entry[i]
		for target in port:
			if isinstance(target.node, graph.SubGraph):
				buffer.write("%s_in -> %s_out;\n" % (subGraph.name, subGraph.name))
			else:
				buffer.write("%s_in : I%d ->  %s : I%d;\n" % (
					subGraph.name, i, str(target.node.id), target.idx))



	buffer.write('%s_in[label="{%s_in|{%s}}"];\n' % (subGraph.name, subGraph.name, label))

## "close" the subgraph.
def subGraphFooter(buffer, subGraph):
	port = subGraph.exit
	if port.isBound():
		if port.hasLit():
			buffer.write('%s_out[label="{%s|%s_out}"];\n' % (subGraph.name, port.src.val, subGraph.name))
		else: buffer.write("%s_out;\n" % subGraph.name)
	buffer.write("}\n")

# ----- #
# Ports #
# ----- #

def portString(port):
	if port.hasLit(): return str(port.src.val)
	else: return "<I%d>%s" % (port.idx, '*' if port.isBound() else '')

def inputStr(node):
	str = '|'.join([portString(port) for port in node.ports])
	return "{%s}|" % str

def outputStr(node):
	target = '*' if node.out.targets else ''
	return "|{<O> %s}" % target

# ----- #
# Nodes #
# ----- #

## Add the label of the node to the buffer. 
def nodeLabel(buffer, node):
	buffer.write(str(node.id))
	buffer.write(' [')
	buffer.write('label="' + '{' + inputStr(node) + str(node) + outputStr(node) + '}"')
	if isinstance(node, graph.CompoundNode) : buffer.write("style = filled, fillcolor = lightgrey")
	if isinstance(node, graph.CallNode): buffer.write("style = dashed")
	buffer.write('];\n')

## Add all the outgoing edges of a node to the buffer.
def nodeLinks(buffer, node):
	for target in node.out:
		if isinstance(target.node, graph.SubGraph):
			buffer.write("%s -> %s_out;\n" % (str(node.id), node.sg.name))
		else:
			buffer.write("%s : O ->  %s : I%d;\n" % (
				str(node.id), str(target.node.id), target.idx))

def writeNode(buffer, node):
	nodeLabel(buffer, node)
	nodeLinks(buffer, node)

# --- #
# Dot #
# --- #

## Write general dot information
def dotHeader(buffer):
	buffer.write("digraph IGR {\n")
	buffer.write("graph [compound=true];\n")
	buffer.write("node [shape=record];\n")

## Close the dot graph
def dotFooter(buffer):
	buffer.write("}")

def dotLoop(gr, buf):
	for sg in gr:
		subGraphHeader(buf, sg)

		for node in sg:
			writeNode(buf, node)

			if isinstance(node, graph.CompoundNode):
				compoundHeader(buf, node)
				dotLoop(node, buf)
				compoundFooter(buf, node)

		subGraphFooter(buf, sg)


## Create the dot string
def getDot(graph, buffer = None):
	buffer = StringIO.StringIO()
	dotHeader(buffer)
	dotLoop(graph, buffer)
	dotFooter(buffer)
	str = buffer.getvalue()
	buffer.close()
	return str

##
# Get the dot representation and 
# write it to a file.
##
def dotToFile(path, graph):
	f = open(path, 'w')
	f.write(getDot(graph))
	f.close()

##
# Convert the IGR graph to dot, save it,
# and run dot on this file. 
#
# This function should be call with keyword arguments.
# The default arguments will cause the following behaviour:
# 		* dot is assumed to be in your PATH.
#		* the dot file will be saved in igr.dot
#		* the output will be in png format.
#		* dot will decide where to store the output.
#			With the default settings this would be in igr.dot.png
#
# \param dotpath
#		The path of the dot executable, in case it's not in your PATH
# \param path
#		The location where the dot file will be stored.
# \param format
#		The output format of the graph dot creates from the dot file.
# \param output
#		The location where we store the output of dot.
#		Leaving this blank will pass the -O option.
#		The -O option let's dot choose the path.
# \param other
#		Any other options you want to pass to doth.
#		These options should be passed as a list of strings.
# \param skipCompound 
#		True if you do not want to display the compound nodes.
##
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
