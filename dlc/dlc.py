#!/usr/bin/env python

# dlc.py
# Mathijs Saey
# DLC

# This file is the entry point of the dlc compiler.
# It is responsible for parsing the command line parameters
# and invoking the various parts of the compiler.

import frontend

def compile(str):
	pass

def compileFile(path, output = None):
	f = open(path, 'r')
	r = compile(f.read)
	return r


test = '''
func fac(n)
#	if n > 0
#		then n * main(n - 1)
#		else 1

func main(a,b)
#	fac    := 5
#    other  := (33 + 3) - 35 
#	fac * other
'''

test = '''
func test():
	4 < 4 < 4
'''

print frontend.convert(test)
