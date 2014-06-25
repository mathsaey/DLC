# traverse.py
# Mathijs Saey
# DLC

# This module defines functionality to
# traverse the program graph.

def traverse(graph, nodeFunc, sgStart, sgStop, compStart, compStop):
	for sg in list(graph):
		sgStart(sg)

		for node in sg:
			nodeFunc(node)
			if node.isCompound():
				compStart(node)
				traverse(node, nodeFunc, sgStart, sgStop, compStart, compStop)
				compStop(node)

		sgStop(sg)