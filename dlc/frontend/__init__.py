# __init__.py
# Mathijs Saey
# DLC

# This package contains the frontend of
# dlc, it is responsible for accepting an
# input language and trasforming it into 
# a valid intermediate graph representation.

import lexer
import parser
import error

def convert(string):
	res = parser.parser.parse(string)
	error.verify()
	return res

