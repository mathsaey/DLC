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
func tmp(a, b): 
	if 5 < 4
	then a
	else if true then a else b

#func normal(a):
#	if true
#	then a
#	else 0

func fuu(a,b): let c := 5 d := c + 1 in -a + b

#
#func for_(a,b):
#	for el in [a..b] do
#		el + 1
#
#func test(): 32
#func fac(n):
#	if n > 0
#		then n * fac(n - 1)
#		else 1
#
#func main(a,b):
#	let 
#		fac    := 5
#    	other  := (33 + 3) - 35 
#    in
#		fac * other < 4
'''


#if args.path is '-': file = sys.stdin
#else: file = open(args.path, 'r')

frontend.read(test)
IGR.dot(frontend.get())


# fileName, fileExtension = os.path.splitext(args.path)

# frontEnd.setUp(fileExtension, args.frontEnd)
# frontEnd.fromFile(args.path)

# if args.dot: IGR.dot()

# if args.dry_run:
# 	sys.exit(0)

# backEnd.setUp(fileName, args.backEnd, args.output)
# backEnd.toFile()
