#!/usr/bin/env python

# dlc.py
# Mathijs Saey
# DLC

# This file is the entry point of the dlc compiler.
# It is responsible for parsing the command line parameters
# and invoking the various parts of the compiler.

import IGR
import sys
import argparse
import frontend
import optimize

# ---------------------- #
# Command line arguments #
# ---------------------- #

argParser = argparse.ArgumentParser(description = "The DIS Compiler")

#argParser.add_argument("path", help = "The path to the file you want to compile.")
argParser.add_argument("--dot", action = "store_true", help = "Generate a dot graph of the program")
argParser.add_argument("--dry_run", action = "store_true", help = "Don't compile the program but abort after parsing the input file.")

args = argParser.parse_args()

# ------------------- #
# Compilation Process #
# ------------------- #

test = '''
func constant(): 93
func notCalled(): notCalled()

func cse(a):
	let
		one := a + 5 + 3
		two := a + 5 + 3
	in
		one + two

#
#func for_(a,b):
#	for el in [a..b] do
#		el + 1
#
func test(a): a + 5

func fac(n):
	if n > 0
		then n * fac(n - 1)
		else 1

func kek(n): fac(n)

func main(a,b):
	let 
		none   := [1,2,3]
		fac    := fac(constant())
    	other  := (33 + 3) - 35 
    in
		cse(5) + test(2)
'''


#if args.path is '-': file = sys.stdin
#else: file = open(args.path, 'r')

frontend.read(test)
graph = frontend.get()
optimize.prune(graph)
optimize.inline(graph)

IGR.dot(graph)


# fileName, fileExtension = os.path.splitext(args.path)

# frontEnd.setUp(fileExtension, args.frontEnd)
# frontEnd.fromFile(args.path)

# if args.dot: IGR.dot()

# if args.dry_run:
# 	sys.exit(0)

# backEnd.setUp(fileName, args.backEnd, args.output)
# backEnd.toFile()
