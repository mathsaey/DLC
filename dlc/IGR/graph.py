# graph.py
# Mathijs Saey
# DLC

# This module contains the graph representation
# of a DFL program.
# The intermediate representation does not check for 
# errors while being created.

class Graph(object):
	def __init__(self):
		self.subGraphs = []
		self.functions = {}
		self.currentid = 1

	def __getitem__(self, key):
		if type(key) is int:
			return self.subGraphs[key]
		elif type(key) is str:
			return self.functions[key]
		else: raise TypeError()

	def __contains__(self, item):
		return item in self.functions

	def __iter__(self):
		return iter(self.subGraphs)

	def addSubGraph(self, sg, name):
		self.functions.update({name : sg})
		self.subGraphs.append(sg)
		sg.graph = self

	def getId(self):
		self.currentid += 1
		return self.currentid - 1

# --------- #
# Subgraphs #
# --------- #

class SubGraph(object):
	def __init__(self):
		self.graph = None
		self.nodes = []
		self.entry = []
		self.exit  = InPort(self, 0)
		self.args  = 0
		self.name  = ''

	def addParSlot(self):
		self.args += 1
		port = OutPort(self)
		self.entry.append(port)
		return port

	def getId(self):
		return self.graph.getId()

	def __iter__(self):
		return iter(self.nodes)

	def __iadd__(self, node):
		self.nodes.append(node)
		return self

# ----- #
# Nodes #
# ----- #

class Node(object):
	def __init__(self, sg, args):
		self.id    = sg.getId()
		self.sg    = sg
		self.args  = args
		self.out   = OutPort(self)
		self.ports = [InPort(self,i) for i in xrange(0, args)]
		self.sg    += self

	def __getitem__(self, key):
			return self.ports[key]

	def __str__(self):
		return "Node '%s'" % self.id

class OperationNode(Node):
	def __init__(self, sg, op, args):
		super(OperationNode, self).__init__(sg, args)
		self.op   = op

	def __str__(self):
		return "OpNode '%s' %s" % (self.id, self.op)

class CallNode(Node):
	def __init__(self, sg, name, args):
		super(CallNode, self).__init__(sg, args)
		self.name = name
		self.args = args

	def __str__(self):
		return "CallNode '%s' %s" % (self.id, self.name)

class CompoundNode(Node):
	def __init__(self, sg, args):
		super(CompoundNode, self).__init__(sg, args)

	def __iter__(self):
		raise NotImplementedError

	def addPort(self):
		for sg in self: sg.addParSlot()
		self.ports.append(InPort(self, self.args))
		self.args += 1

	def getId(self):
		return self.sg.getId()

class IfNode(CompoundNode):
	def __init__(self, sg):
		super(IfNode, self).__init__(sg, 1)
		self.thn = None
		self.els = None

	def bindThen(self, sg):
		self.thn = sg
		sg.graph = self
		sg.name  = "cmp_if_thn_%d" % self.id
		for i in xrange(0, self.args): sg.addParSlot()

	def bindElse(self, sg):
		self.els = sg
		sg.graph = self
		sg.name  = "cmp_if_els_%d" % self.id
		for i in xrange(0, self.args): sg.addParSlot()

	def __iter__(self):
		return iter((self.thn, self.els))

class ForNode(CompoundNode):
	def __init__(self, sg):
		super(ForNode, self).__init__(sg, 1)
		self.body = None

	def bindBody(self, body):
		self.body  = body
		body.graph = self
		body.name  = "cmp_forin_%d" % self.id
		for i in xrange(0, self.args): body.addParSlot()

	def __iter__(self):
		return iter((self.body,))

# ---------------- #
# Ports & Literals #
# ---------------- #

class BindAble(object):
	def __init__(self):
		self.typ = None
		
	def bind(self, target):
		raise NotImplementedError

	def isBound(self, target):
		raise NotImplementedError

	def isLit(self): return False

class Port(BindAble): 
	def __init__(self, node):
		super(Port, self).__init__()
		self.node = node

class InPort(Port):
	def __init__(self, node, idx):
		super(InPort, self).__init__(node)
		self.idx = idx
		self.src = None

	def bind(self, src):
		self.src = src

	def isBound(self):
		return self.src is not None

	def hasLit(self):
		return self.isBound() and self.src.isLit()

class OutPort(Port):
	def __init__(self, node):
		super(OutPort, self).__init__(node)
		self.targets = []

	def bind(self, target):
		self.targets.append(target)
		target.typ = self.typ
		target.bind(self)

	def isBound(self):
		return self.targets != []

	def __iter__(self):
		return iter(self.targets)

class Literal(BindAble):
	def __init__(self, value, typ):
		self.val = value
		self.dst = None
		self.typ = typ

	def isLit(self): return True

	def bind(self, target):
		if self.isBound():
			l = Literal(self.val)
			l.bind(target)
		else:
			self.dst = target
			target.src = self
			target.typ = self.typ

	def isBound(self):
		return self.dst is not None