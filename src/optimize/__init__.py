# __init__.py
# Mathijs Saey
# DLC

# This package contains a few optimizations

import prune as p
import autoinline
import constants

def run(graph, inline = True, prune = True):
	constants.remove(graph)

	if prune:  p.prune(graph)
	if inline: autoinline.inline(graph, 0)