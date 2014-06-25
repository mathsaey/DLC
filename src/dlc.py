#!/usr/bin/env python

# dlc.py
# Mathijs Saey
# DLC

# This file is the entry point of the dlc compiler.
# It is responsible for parsing the command line parameters
# and invoking the various parts of the compiler.

import IGR
import argparse
import frontend
import fileinput


# ---------------------- #
# Command line arguments #
# ---------------------- #

argParser = argparse.ArgumentParser(description = "The DIS Compiler")

argParser.add_argument("path", help = "The path to the file you want to compile.")
argParser.add_argument("--dot", action = "store_true", help = "Generate a dot graph of the program")
argParser.add_argument("--dry_run", action = "store_true", help = "Don't compile the program but abort after parsing the input file.")

args = argParser.parse_args()

# ------------------- #
# Compilation Process #
# ------------------- #

for line in fileinput.input(args.path):
	frontend.read(line)

IGR.dot(frontend.get())


# fileName, fileExtension = os.path.splitext(args.path)

# frontEnd.setUp(fileExtension, args.frontEnd)
# frontEnd.fromFile(args.path)

# if args.dot: IGR.dot()

# if args.dry_run:
# 	sys.exit(0)

# backEnd.setUp(fileName, args.backEnd, args.output)
# backEnd.toFile()




def compile(str):
	pass

def compileFile(path, output = None):
	f = open(path, 'r')
	r = compile(f.read)
	return r


test = '''
func tmp(): true

func for_(a,b):
	for el in [a..b] do
		el + 1

func test(): 32
func fac(n):
	if n > 0
		then n * fac(n - 1)
		else 1

func main(a,b):
	let 
		fac    := 5
    	other  := (33 + 3) - 35 
    in
		fac * other < 4

#func _for(a):
#	for el in [0..a] do
#		el
'''

IGR.dot(frontend.convert(test))