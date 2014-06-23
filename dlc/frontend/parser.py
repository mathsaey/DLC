# parser.py
# Mathijs Saey
# DLC

# The parser transforms a list of tokens into
# a valid syntax tree.
# Once again, ply is utilized to do this.

import ply.yacc
import lexer
import error

# ----------#
# AST Types #
# ----------#

class PNode(object): pass

# Functions
# ---------

class PFunc(PNode):
	def __init__(self, name, args, body):
		self.name = name
		self.args = args
		self.body = body

	def __repr__(self):
		return "func %s%s{%s}" % (self.name, self.args, self.body)

class PParam(PNode):
	def __init__(self, name):
		self.name  = name

	def __repr__(self):
		return self.name

class PCall(PNode):
	def __init__(self, name, args):
		self.name = name
		self.args = args

	def __repr__(self):
		return "%s%s" % (self.name, self.args)

# Compound structures
# -------------------

class PITL(PNode):
	def __init__(self, cond, true, false):
		self.cond  = cond
		self.true  = true
		self.false = false

	def __repr__(self):
		return "if (%s) then {%s} else {%s}" % (self.cond, self.true, self.false)

class PFor(PNode):
	def __init__(self, name, gen, bod):
		self.name = name
		self.gen  = gen
		self.bod  = bod

	def __repr__(self):
		return "for %s in %s do %s" % (self.name, self.gen, self.bod)

class PLet(PNode):
	def __init__(self, binds, expr):
		self.binds = binds
		self.expr  = expr

	def __repr__(self):
		return "let %s in %s" % (self.binds, self.expr)

class PBind(PNode):
	def __init__(self, name, value):
		self.value = value
		self.name = name

	def __repr__(self):
		return "%s := %s" % (self.name, self.value)

# Operations
# ----------

class POp(PNode):
	def __init__(self, op, args):
		self.op = op
		self.args = args

	def __repr__(self):
		return "%s(%s)" % (self.op, self.args)

class BinOp(POp):
	def __init__(self, op, l, r):
		super(BinOp, self).__init__(op, [l,r])

class UnOp(POp):
	def __init__(self, op, x):
		super(UnOp, self).__init__(op, x)
		self.typ = x.typ

# Terminals
# ---------

class PNameRef(PNode):
	def __init__(self, name):
		self.name = name

	def __repr__(self):
		return self.name

class PData(PNode): 
	def __init__(self, val, typ):
		self.typ = type
		self.val = val

	def __repr__(self):
		return str(self.val)

# -------------- #
# Semantic State #
# -------------- #

# Function Tracking
# -----------------

class SemanticError(Exception): pass

# Keep track of the defined
# function names
funLst = {}

def addFunc(name, args):
	if name in funLst:
		raise SemanticError()
	else:
		funLst.update({name : args})

def funcArgs(name):
	try: return funLst[name]
	except KeyError: raise SemanticError

# Scope naming
# ------------

# Keep track of the variables
# in the current scope
scopes = [[]]

def newScope():
	scopes.append([])

def popScope():
	scopes.pop()

def addName(name):
	if name in scopes[-1]:
		raise SemanticError()
	else:
		scopes[-1].append(name)

def nameDefined(name):
	for scope in scopes:
		if name in scope:
			return True
	return False

# ------ #
# Parser #
# ------ #

tokens = lexer.tokens

def p_program(p):
	'''program : function_list
	           |
	'''
	if len(p) == 1: p[0] = []
	else: p[0] = p[1]

# Functions 
# ---------

def p_funLst(p):
	''' function_list : function function_list
	                  | function
	'''
	if   len(p) == 3: p[0] = [p[1]] + p[2]
	elif len(p) == 2: p[0] = [p[1]]

def p_function(p):
	''' function : newscope signature COL expression'''
	p[0] = PFunc(p[2][0], p[2][1], p[4])
	popScope()

def p_signature(p):
	'''signature : FUNC NAME LPAREN parLst RPAREN'''
	p[0] = (p[2], p[4])
	try:
		addFunc(p[2], len(p[4]))
	except SemanticError:
		error.duplicateFunc(p,2)

def p_parLst(p):
	'''parLst : NAME SEP parLst
	          | NAME
	          |
	'''
	if   len(p) == 1: p[0] = []
	elif len(p) == 2: p[0] = [PParam(p[1])]
	else:             p[0] = [PParam(p[1])] + p[3]

	if len(p) > 1:
		try: addName(p[1])
		except SemanticError: error.duplicateName(p, 1)

def p_newScope(p):
	'''newscope : '''
	newScope()

# Expressions
# -----------

def p_expression(p):
	''' expression : letin
	               | ifthenelse
	               | forin
	               | call
	               | range
	               | array
	               | ops
	'''
	p[0] = p[1]

def p_name(p):
	''' expression : NAME'''
	name = p[1]
	if nameDefined(name):
		p[0] = PNameRef(p[1])
	else:
		error.unknownName(p, 1)

def p_num(p):
	''' expression : NUM'''
	p[0] = PData(p[1], int)

def p_bool(p):
	''' expression : TRUE
	               | FALSE
	'''
	p[0] = PData(p[1], bool)


# Let ... in
# ----------

def p_letin(p):
	''' letin : LET newscope bindLst IN expression'''
	p[0] = PLet(p[3], p[5])
	popScope()

def p_bindLst(p):
	''' bindLst : bind bindLst
	            | bind
	'''
	if   len(p) == 3: p[0] = [p[1]] + p[2]
	elif len(p) == 2: p[0] = [p[1]]

def p_bind(p):
	''' bind : NAME BIND expression '''
	p[0] = PBind(p[1], p[3])
	try:
		addName(p[1])
	except SemanticError:
		error.duplicateName(p,1)

# if then else
# ------------

def p_if_then_else(p):
	'''ifthenelse : IF expression THEN expression ELSE expression'''
	p[0] = PITL(p[2], p[4], p[6])

# for ... in ...
# --------------

def p_for_in(p):
	''' forin : FOR addname IN expression DO expression'''
	p[0] = PFor(p[2], p[4], p[6])
	popScope()

def p_addName(p):
	'''addname : NAME'''
	newScope()
	addName(p[1])
	p[0] = p[1]

# call
# ----

def p_call(p):
	''' call : NAME LPAREN argLst RPAREN'''
	p[0] = PCall(p[1], p[3])

	try: 
		if funcArgs(p[1]) is not len(p[3]):
			error.wrongArgCount(p, 1)
	except SemanticError:
		error.unknownFunc(p,1)

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
	op = POp('ARRAY', p[2])
	op.typ = 'arr'
	p[0] = op

def p_range(p):
	''' range : LBRACK expression DOT DOT expression RBRACK'''
	op = BinOp('RANGE', p[2], p[5])
	op.typ = 'range'
	p[0] = op

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
	p[0] = BinOp(p[2], p[1], p[3])

def p_unops(p):
	''' ops : NOT expression
			| MIN expression            %prec UMIN
	        | LPAREN expression RPAREN
	'''
	if len(p) == 3: p[0] = UnOp(p[1], p[2])
	else : p[0] = p[2]

# ------- #
# General #
# ------- #

def p_error(t):
	error.syntax(t)
	ply.yacc.errok()

__parser__ = ply.yacc.yacc()

def parse(input):
	return __parser__.parse(input)