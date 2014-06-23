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
func test(a): 5
func fac(n):
	if n > 0
		then n * fac(n - 1, 5)
		else 1

func main(a,b):
	let 
		fac    := 5
    	other  := (33 + 3) - 35 
    in
		fac * other < 4

func _for(a):
	for el in [0..a] do
		el
'''

print frontend.convert(test)