# traverse.py
# Mathijs Saey
# DLC

# This module defines functionality to
# traverse the program graph.

def traverse(g, nProc, sgStart, sgStop, compStart, compStop, comp = True):
	for sg in g:
		sgStart(sg)

		for node in sg:

			nProc(node)
			if node.isCompound():
				compStart(node)
				if comp: traverse(
					node, nProc, sgStart, sgStop, compStart, compStop, comp)
				compStop(node)

		sgStop(sg)