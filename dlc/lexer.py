# lexer.py
# Mathijs Saey
# DLC

# The lexer is responsible for reading a stream of
# input signal after which it converts it into a token stream.
# We utilize ply (python Lex-Yacc) to achieve this.

import ply.lex
import error

# ----------------- #
# Token Definitions #
# ----------------- #

keywords = {
	'func' : 'FUNC',
	'if'   : 'IF',
	'then' : 'THEN',
	'else' : 'ELSE',
	'for'  : 'FOR',
	'in'   : 'IN',
}

tokens = [
	'PLUS', 'MIN', 'MUL', 'DIV',
	'LT', 'LTEQ', 'GT', 'GTEQ',
	'EQ', 'NOT', 'AND', 'OR',
	'LPAREN', 'RPAREN', 'LBRAC', 'RBRAC', 
	'NAME', 'NUM', 'BIND', 
] + list(keywords.values())

# ------------------ #
# Simple Token Rules #
# ------------------ #

t_PLUS   = r'\+'
t_MIN    = r'\-'
t_MUL    = r'\*'
t_DIV    = r'\\'

t_LT     = r'<'
t_LTEQ   = r'=<'
t_GT     = r'>'
t_GTEQ   = r'>='

t_EQ     = r'='
t_NOT    = r'!'
t_AND    = r'&&'
t_OR     = r'\|\|'

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRAC  = r'\['
t_RBRAC  = r'\]'

t_BIND   = r':='

t_ignore = ' \t'
t_ignore_COMMENT = r'\#.*'

# -------------------- #
# Function Token Rules #
# -------------------- #

def t_NAME(t):
	r'(\w|_)(\w|\d|!|\?|_|-)*'
	t.type = keywords.get(t.value,'NAME')
	return t

def t_NUM(t):
	r'\d+'
	t.value = int(t.value)
	return t

# ----------- #
# Other Rules #
# ----------- #

def t_newline(t):
	r'\n'
	t.lexer.lineno += len(t.value)

def t_error(t):
	lines = t.lexer.lexdata
	startIdx = lines.rfind('\n', 0, t.lexpos) + 1
	stopIdx  = lines.find('\n', t.lexpos)

	if startIdx < 0 : startIdx = 0
	if stopIdx  < 0 : stopIdx  = len(lines)

	column  = (t.lexpos - startIdx) + 1

	raise error.DLCError(
		lines[startIdx:stopIdx], t.lineno, 
		"Illegal character", column, column + 1)

	t.lexer.skip(1)

# ------------ #
# Lexer "main" #
# ------------ #

__lexer__ = ply.lex.lex()

def lex(input):
	__lexer__.input(input)
	return iter(__lexer__)
