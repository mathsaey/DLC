#!/usr/bin/env python

# dlc.py
# Mathijs Saey
# DLC

# This file is the entry point of the dlc compiler.
# It is responsible for parsing the command line parameters
# and invoking the various parts of the compiler.

import lexer

def compile(str):
	pass

def compileFile(path, output = None):
	f = open(path, 'r')
	r = compile(f.read)
	return r


test = '''
func : fac(n)
	if n > 0
		then n * main(n - 1)
		else 1

func main(n)
	fac    := fac(n)
    other  := (33 + 3) - 35 
	fac * other
'''


lex = lexer.lex(test)

try:
	for tok in lex:
		pass
except Exception, e:
	print e