# traverse.py
# Mathijs Saey
# DLC

# This module defines functionality to
# traverse the program graph.

def traverse(g, nodeF, sgStart, sgStop, compStart, compStop, comp = True):
	for sg in list(g):
		sgStart(sg)

		for node in sg:
			nodeF(node)
			if node.isCompound():
				compStart(node)
				if comp: traverse(
					node, nodeF, sgStart, sgStop, compStart, compStop, comp)
				compStop(node)

		sgStop(sg)