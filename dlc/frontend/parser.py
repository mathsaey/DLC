# parser.py
# Mathijs Saey
# DLC

# The parser transforms a list of tokens into
# a valid syntax tree.
# Once again, ply is utilized to do this.

import ply.yacc
import lexer
import error

tokens = lexer.tokens

# ------ #
# Basics #
# ------ #

def p_program(p):
	'''program : function_list
	           |
	'''
	if len(p) == 1: p[0] = ('program', [])
	else: p[0] = ('program', p[1])

# --------- #
# Functions #
# --------- #

def p_funLst(p):
	''' function_list : function function_list
	                  | function
	'''
	if   len(p) == 3: p[0] = [('function', p[1])] + p[2]
	elif len(p) == 2: p[0] = [('function', p[1])]

def p_function(p):
	''' function : signature COL expression'''
	p[0] = {"signature": p[1], "body": p[3]}

def p_signature(p):
	'''signature : FUNC NAME LPAREN parLst RPAREN'''
	p[0] = {'name': p[2], 'args': p[4]}

def p_parLst(p):
	'''parLst : NAME SEP parLst
	          | NAME
	          |
	'''
	if   len(p) == 1: p[0] = []
	elif len(p) == 2: p[0] = [p[1]]
	else:             p[0] = [p[1]] + p[3]

# ----------- #
# Expressions #
# ----------- #

def p_expression(p):
	''' expression : letin
	               | ifthenelse
	               | forin
	               | call
	               | range
	               | array
	               | ops
	'''
	p[0] = ('expression', p[1])

def p_name(p):
	''' expression : NAME'''
	p[0] = ('name', p[1])

def p_num(p):
	''' expression : NUM'''
	p[0] = ('num', p[1])

# Let ... in
# ----------

def p_letin(p):
	''' letin : LET bindLst IN expression'''
	p[0] = ('let', {'binds':p[2], 'expression':p[4]})

def p_bindLst(p):
	''' bindLst : bind bindLst
	            | bind
	'''
	if   len(p) == 3: p[0] = [p[1]] + p[2]
	elif len(p) == 2: p[0] = [p[1]]

def p_bind(p):
	''' bind : NAME BIND expression '''
	p[0] = {'name': p[1], 'expression': p[3]}

# if then else
# ------------

def p_if_then_else(p):
	'''ifthenelse : IF expression THEN expression ELSE expression'''
	p[0] = ('if_then_else', {'cond': p[2], 'then': p[4], 'else': p[6]})

# for ... in ...
# --------------

def p_for_in(p):
	''' forin : FOR NAME IN expression DO expression'''
	p[0] = ('forin', {'name': p[2], 'generator': p[4], 'body': p[6]})

# call
# ----

def p_call(p):
	''' call : NAME LPAREN argLst RPAREN'''
	p[0] = ('call', {'name': p[1], 'args': p[3]})

def p_argLst(p):
	'''argLst : expression SEP argLst
	          | expression
	          |
	'''
	if   len(p) == 1: p[0] = []
	elif len(p) == 2: p[0] = [p[1]]
	else:             p[0] = [p[1]] + p[3]

# arrays
# ------

def p_array(p):
	''' array : LBRACK argLst RBRACK'''
	p[0] = ('array', {'args': p[2]})

def p_range(p):
	''' range : LBRACK NUM DOT DOT NUM RBRACK'''
	p[0] = ('range', {'from': p[2], 'to': p[5]})

# calculations
# ------------

precedence = [
	('nonassoc', 'AND', 'OR', 'NOT'),
	('nonassoc', 'EQ'),
	('nonassoc', 'LT', 'LTEQ', 'GT', 'GTEQ'),
	('left', 'PLUS', 'MIN'),
	('left', 'MUL', 'DIV'),
	('right', 'UMIN')
]

def p_binops(p):
	''' ops : expression PLUS expression
	        | expression MIN  expression
	        | expression MUL  expression
	        | expression DIV  expression
	        | expression LT   expression
	        | expression LTEQ expression
	        | expression GT   expression
	        | expression GTEQ expression
	        | expression AND  expression
	        | expression OR   expression
	        | expression EQ   expression
	'''
	p[0] = ('binop', {'op': p[2], 'left': p[1], 'right': p[3]})

def p_unops(p):
	''' ops : NOT expression
			| MIN expression            %prec UMIN
	        | LPAREN expression RPAREN
	'''
	if len(p) == 3: p[0] = ('unop', {'op': p[1], 'expression': p[2]})
	else : p[0] = p[2]

# ------- #
# General #
# ------- #

def p_error(t):
	error.add(error.SyntaxError(t))


parser = ply.yacc.yacc()