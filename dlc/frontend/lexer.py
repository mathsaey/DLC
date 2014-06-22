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
	'let'  : 'LET',
	'in'   : 'IN',
	'do'   : 'DO'
}

tokens = [
	'PLUS', 'MIN', 'MUL', 'DIV',
	'LT', 'LTEQ', 'GT', 'GTEQ',
	'EQ', 'NOT', 'AND', 'OR',
	'LPAREN', 'RPAREN', 
	'LBRACK', 'RBRACK', 
	'NAME', 'NUM', 'BIND', 
	'SEP', 'COL', 'DOT'
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
t_LBRACK = r'\['
t_RBRACK = r'\]'

t_BIND   = r':='
t_SEP    = r','
t_COL    = r':'
t_DOT    = r'\.'

t_ignore = ' \t'
t_ignore_COMMENT = r'\#.*'

# -------------------- #
# Function Token Rules #
# -------------------- #

def t_NAME(t):
	r'([a-zA-Z]|_)(\w|!|\?|-)*'
	t.type = keywords.get(t.value,'NAME')
	return t

def t_NUM(t):
	r'\d+'
	t.value = int(t.value)
	return t

def t_newline(t):
	r'\n'
	t.lexer.lineno += len(t.value)

def t_error(t):
	error.add(error.IllegalCharError(t))
	t.lexer.skip(1)

# ------------ #
# Lexer "main" #
# ------------ #

__lexer__ = ply.lex.lex()

def lex(input):
	__lexer__.input(input)
	return iter(__lexer__)
