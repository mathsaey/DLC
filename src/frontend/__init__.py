# __init__.py
# Mathijs Saey
# DLC

# This package contains the frontend of
# dlc, it is responsible for accepting an
# input language and trasforming it into 
# a valid intermediate graph representation.

from error import FrontEndError as Error

import parser
import error

def convert(input):
	tree = parser.parse(input)
	error.verify()
	return tree

def read(input):
	parser.parse(input)

def get():
	error.verify()
	return parser.get()