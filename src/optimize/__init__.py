# __init__.py
# Mathijs Saey
# DLC

# This package contains the optimizations 

import cse   as _cse
import prune as _prune
import constants

def run(graph, inline = True, prune = True, cse = True):
	constants.remove(graph)

	if cse:    _cse.eliminate(graph)
	if prune:  _prune.prune(graph)
