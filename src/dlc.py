#!/usr/bin/env python

# dlc.py
# Mathijs Saey
# DLC

# This file is the entry point of the dlc compiler.
# It is responsible for parsing the command line parameters
# and invoking the various parts of the compiler.

import os
import IGR
import sys
import backend
import argparse
import frontend
import optimize

# ---------------------- #
# Command line arguments #
# ---------------------- #

argParser = argparse.ArgumentParser(description = "The DFL Compiler")
argParser.add_argument("path", nargs = '?', default = '-', help = "The path to the file you want to compile.")
argParser.add_argument("--dot", action = "store_true", help = "Generate a dot graph of the program")
args = argParser.parse_args()

# ------------------- #
# Compilation Process #
# ------------------- #

if args.path is '-':
	file = sys.stdin
else: 
	file = open(args.path, 'r')
	fileName, fileExtension = os.path.splitext(args.path)

frontend.read(file.read())

try:
	graph = frontend.get()
except frontend.Error:
	print >> sys.stderr, "There are errors in your program."
	sys.exit(1)

if args.dot: IGR.dot(graph, path = "pre.dot")
optimize.run(graph)
if args.dot: IGR.dot(graph, path = "post.dot")

dis = backend.convert(graph)
if args.path is '-': 
	print dis
else:
	file = open('%s.%s' % (fileName, 'dis'), 'w')
	file.write(dis)