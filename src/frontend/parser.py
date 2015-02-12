# parser.py
# Mathijs Saey
# DLC

# The parser transforms a list of tokens into
# an intermediate graph representation.
# Once again, ply is utilized to do this.

# Besides the actual parsing, the parser 
# is responsible for:
#	- (limited) type checks
#	- let...in name resolving
#	- Semantic error reporting
#	- Correct creation of compounds

import ply.yacc
import natives
import lexer
import error
import IGR

# ------------ #
# Parser State #
# ------------ #

# Program and current subgraph
# ----------------------------

graph    = IGR.Graph()
subGraph = [None]

def setSg(sg):
	subGraph[-1] = sg

def getSg():
	return subGraph[-1]

# Standard scoping Rules
# ----------------------

scopes = [[]]

def newScope(): scopes[-1].append({})
def popScope(): scopes[-1].pop()

def addName(name, port): scopes[-1][-1].update({name : port})
def nameInScope(name):
	for scope in scopes:
		if name in scope[-1]: return True
	return False

def getLocalName(name, lvl):
	for scope in reversed(scopes[lvl]):
		if name in scope:
			return scope[name]

def getName(name, lvl = -1):
	res = getLocalName(name, lvl)
	if res: 
		return res
	elif lvl is - len(scopes): 
		return None

	# Recursively get the name from outside the
	# current compound scope
	# bind all the required compound nodes on the
	# way down
	compound     = subGraph[lvl].graph
	externalPort = getName(name, lvl - 1)

	# Ensure another subgraph of the compound did
	# not add this port yet.
	for port in compound.ports:
		if port.src is externalPort:
			return subGraph[lvl].entry[port.idx]

	# Add a new port, bind it to
	# the external name definition
	compound.addPort()
	externalPort.bind(compound[-1])
	return subGraph[lvl].entry[-1]

# Compound scoping Rules
# ----------------------

def scopeCompound():
	scopes.append([])

def popCompound():
	scopes.pop()

def scopeSg(sg):
	subGraph.append(sg)

def popSg():
	subGraph.pop()

def isCompound():
	return len(subGraph) > 1

# ----------- #
# Convenience #
# ----------- #

def checkTypes(p, idx, values, expected):
	for i in xrange(0, len(values)):
		if values[i].typ and expected[i] and values[i].typ is not expected[i]:
			error.wrongType(p, idx)

def matchTypes(p, idx, t1, t2, t3):
	if (t1.typ and t2.typ) and (t1.typ is not t2.typ):
		error.typeMismatch(p, idx)
	else:
		t3.typ = t1.typ

def create_binop(p, op, tIn, tOut):
	checkTypes(p, 2, (p[1], p[3]), (tIn, tIn))
	node = IGR.OperationNode(getSg(), op, 2)
	node.out.typ = tOut
	p[1].bind(node[0])
	p[3].bind(node[1])
	p[0] = node.out

def create_unop(p, op, tIn, tOut):
	checkTypes(p, 1, (p[2],), (tIn,))
	node = IGR.OperationNode(getSg(), op, 1)
	node.out.type = tOut
	p[0] = node.out
	p[2].bind(node[0])

def create_nativeop(p):
	nat = natives.get(p[1])
	lst = p[3]

	node = IGR.OperationNode(getSg(), nat.disName, len(lst))

	if len(lst) is not len(nat.inTypes): 
		error.wrongArgCount(p, 1)
	else:
		checkTypes(p, 1, lst, nat.inTypes)

	node.out.typ = nat.outType
	return node

def create_callNode(p):
	node   = IGR.CallNode(getSg(), p[1], len(p[3]))

	if p[1] not in graph:
		error.unknownFunc(p,1)
	elif graph[p[1]].args is not len(p[3]):
		error.wrongArgCount(p, 1)
	else: 
		node.out.typ = graph[p[1]].exit.typ

	return node

# ------ #
# Parser #
# ------ #

tokens = lexer.tokens

precedence = [
	('nonassoc', 'LET'),
	('nonassoc', 'IN'),
	('nonassoc', 'FOR'),
	('nonassoc', 'DO'),
	('nonassoc', 'ELSE'),
	('nonassoc', 'THEN'),
	('left',     'LBRACK', 'RBRACK'),
	('nonassoc', 'AND', 'OR', 'NOT'),
	('nonassoc', 'EQ', 'NEQ'),
	('nonassoc', 'LT', 'LTEQ', 'GT', 'GTEQ'),
	('left',     'PLUS', 'MIN'),
	('left',     'MUL', 'DIV'),
	('nonassoc', 'UMIN'),

]

def p_program(p):
	'''program : function_list
	           |
	'''

def p_newScope(p):
	'''newscope : '''
	newScope()

# Functions 
# ---------

def p_funLst(p):
	''' function_list : function function_list
	                  | function
	'''

def p_function(p):
	''' function : signature COL expression'''
	p[3].bind(getSg().exit)
	setSg(None)
	popScope()

def p_signature(p):
	'''signature : FUNC NAME LPAREN startFunc parLst RPAREN'''
	if p[2] in graph: error.duplicateFunc(p,2)
	graph.addSubGraph(getSg(), p[2])
	getSg().name = p[2]

def p_startFunc(p):
	''' startFunc : newscope '''
	sg = IGR.SubGraph()
	setSg(sg)
	
def p_parLst(p):
	''' parLst : par SEP parLst
	           | par
	           |
	'''

def p_par(p):
	''' par : NAME '''
	if nameInScope(p[1]): error.duplicateName(p, 1)
	addName(p[1], getSg().addParSlot())

# Data
# ----

def p_name(p):
	''' expression : NAME'''
	res = getName(p[1])
	if res:
		p[0] = res
	else:
		error.unknownName(p, 1)
		p[0] = IGR.Literal(None, None)

def p_num(p):
	''' expression : NUM'''
	p[0] = IGR.Literal(p[1], int)

def p_true(p):
	''' expression : TRUE '''
	p[0] = IGR.Literal(True, bool)

def p_false(p):
	''' expression : FALSE '''
	p[0] = IGR.Literal(False, bool)


# Let ... in
# ----------

def p_letin(p):
	''' expression : LET newscope bindLst IN expression'''
	p[0] = p[5]
	popScope()

def p_bindLst(p):
	''' bindLst : bind bindLst
	            | bind
	'''

def p_bind(p):
	''' bind : NAME BIND expression '''
	if nameInScope(p[1]): error.duplicateName(p,1)
	addName(p[1], p[3])

# if then else
# ------------

def p_if_then_else(p):
	'''expression : IF expression THEN thenScope expression ELSE elseScope expression'''
	node = getSg().graph
	popCompound()
	popSg()

	p[0] = node.out

	toInt = IGR.OperationNode(getSg(), 'int', 1)
	p[2].bind(toInt[0])
	toInt.out.typ = int

	toInt.out.bind(node[0])
	p[5].bind(node.thn.exit)
	p[8].bind(node.els.exit)

	checkTypes(p, 1, (p[2],), (bool,))
	matchTypes(p, 1, node.thn.exit, node.els.exit, node.out)


def p_if_thenScope(p):
	''' thenScope : '''
	scopeCompound()
	ifNode = IGR.IfNode(getSg())
	thn = IGR.SubGraph()
	els = IGR.SubGraph()
	ifNode.bindThen(thn)
	ifNode.bindElse(els)
	scopeSg(thn)

def p_if_elseScope(p):
	''' elseScope : '''
	then = getSg()
	popSg()
	ifNode = then.graph
	els = ifNode.els
	scopeSg(els)

# for ... in ...
# --------------

def p_for_in(p):
	''' expression : FOR forGenerator DO expression'''

	node = getSg().graph
	node.out.typ = list
	p[4].bind(node.body.exit)
	p[2].bind(node[0])
	p[0] = node.out

	popCompound()
	popSg()

def p_for_gen(p):
	''' forGenerator : NAME IN expression'''
	p[0] = p[3]

	forNode = IGR.ForNode(getSg())
	body    = IGR.SubGraph()
	forNode.bindBody(body)

	scopeCompound()
	scopeSg(body)

	newScope()
	addName(p[1], body.entry[0])

# call
# ----

def p_call(p):
	''' expression : NAME LPAREN argLst RPAREN'''
	node = None
	if natives.isNative(p[1]):
		node = create_nativeop(p)
	else:
		node = create_callNode(p)

	p[0] = node.out
	for i in xrange(0, len(p[3])):
		p[3][i].bind(node[i])


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
	''' expression : array
	               | range
	               | arrAccess
	'''
	p[0] = p[1]

def p_array_create(p):
	''' array : LBRACK argLst RBRACK'''
	node = IGR.OperationNode(getSg(), 'array', len(p[2]))
	node.out.typ = list
	for i in xrange(0, len(p[2])):
		el = p[2][i]
		el.bind(node[i])

	p[0] = node.out

def p_array_access(p):
	''' arrAccess : expression LBRACK expression RBRACK '''
	node = IGR.OperationNode(getSg(), 'arrGet', 2)
	p[0] = node.out
	p[1].bind(node[0])
	p[3].bind(node[1])

def p_range(p):
	''' range : LBRACK expression DOT DOT expression RBRACK'''
	node = IGR.OperationNode(getSg(), 'range', 2)
	node.out.typ = list
	p[0] = node.out
	p[2].bind(node[0])
	p[5].bind(node[1])

# Operations
# ----------

def p_ops(p):
	''' expression : ops '''
	p[0] = p[1]
def p_binops_plus(p):
	''' ops : expression PLUS expression'''
	create_binop(p, 'add', int, int)
def p_binops_mim(p):
	''' ops : expression MIN  expression '''
	create_binop(p, 'sub', int, int)
def p_binops_mul(p):
	''' ops : expression MUL  expression '''
	create_binop(p, 'mul', int, int)
def p_binops_div(p):
	''' ops : expression DIV  expression '''
	create_binop(p, 'div', int, int)
def p_binops_lt(p):
	''' ops : expression LT   expression '''
	create_binop(p, 'less',   int, bool)
def p_binops_lteq(p):
	''' ops : expression LTEQ expression '''
	create_binop(p, 'lessEq', int, bool)
def p_binops_gt(p):
	''' ops : expression GT   expression '''
	create_binop(p, 'more',   int, bool)
def p_binops_gteq(p): 
	''' ops : expression GTEQ expression '''
	create_binop(p, 'moreEq', int, bool)
def p_binops_eq(p):
	''' ops : expression EQ   expression '''
	create_binop(p, 'equals', None, bool)
def p_binops_neq(p):
	''' ops : expression NEQ   expression '''
	create_binop(p, 'notEq', None, bool)
def p_binops_and(p):
	''' ops : expression AND expression '''
	create_binop(p, 'and', bool, bool)
def p_binops_or(p):
	''' ops : expression OR  expression '''
	create_binop(p, 'or', bool, bool)
def p_unops_not(p):
	''' ops : NOT expression'''
	create_unop(p, 'not', bool, bool)
def p_unops_min(p):
	'''	ops	: MIN expression %prec UMIN'''
	create_unop(p, 'neg', int, int)
def p_unops_paren(p):
	''' ops : LPAREN expression RPAREN'''
	p[0] = p[2]

# ------- #
# General #
# ------- #

def p_error(t):
	if t:
		error.syntax(t)
		ply.yacc.errok()
	else:
		error.eof()

__parser__ = ply.yacc.yacc()

def parse(input):
	__parser__.parse(input)

def get():
	return graph