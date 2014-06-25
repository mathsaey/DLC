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
		sg.func  = sg

	def delSubGraph(self, name):
		sg = self[name]
		del self.functions[name]
		self.subGraphs.remove(sg)

	def getId(self):
		self.currentid += 1
		return self.currentid - 1

# --------- #
# Subgraphs #
# --------- #

class SubGraph(object):
	def __init__(self):
		self.isRec = False
		self.graph = None
		self.nodes = []
		self.entry = []
		self.exit  = InPort(self, 0)
		self.args  = 0
		self.name  = ''
		self.func  = None

	def addParSlot(self):
		port = OutPort(self, self.args)
		self.entry.append(port)
		self.args += 1
		return port

	def delNode(self, node):
		self.nodes.remove(node)

	def getId(self):
		return self.graph.getId()

	def isFunc(self):
		return isinstance(self.graph, Graph)

	def getFunc(self):
		if self.isFunc(): return self
		else: return self.graph.sg.getFunc()

	def __iter__(self):
		return iter(self.nodes)

	def __iadd__(self, node):
		self.nodes.append(node)
		return self

	def __contains__(self, item):
		print item
		return item in self.nodes

# ----- #
# Nodes #
# ----- #

class Node(object):
	def __init__(self, sg, args):
		self.id    = sg.getId()
		self.sg    = sg
		self.args  = args
		self.out   = OutPort(self, 0)
		self.ports = [InPort(self,i) for i in xrange(0, args)]
		self.sg    += self

	def remove(self): self.sg.delNode(self)
	def isCompound(self): return False
	def isCall(self): return False
	def isOp(self): return False

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

	def isOp(self): return True

class CallNode(Node):
	def __init__(self, sg, name, args):
		super(CallNode, self).__init__(sg, args)
		self.isRec = sg.func.name == name
		if self.isRec: self.sg.func.isRec = True
		self.name  = name
		self.args  = args

	def __str__(self):
		return "CallNode '%s' %s" % (self.id, self.name)

	def isCall(self): return True

class CompoundNode(Node):
	def __init__(self, sg, args):
		super(CompoundNode, self).__init__(sg, args)

	def __iter__(self):
		raise NotImplementedError

	def isCompound(self): return True

	def addPort(self):
		for sg in self: sg.addParSlot()
		self.ports.append(InPort(self, self.args))
		self.args += 1

	def getId(self): return self.sg.getId()

	def bind(self, sg):
		for i in xrange(0, self.args): sg.addParSlot()
		sg.func  = self.sg.func
		sg.graph = self


class IfNode(CompoundNode):
	def __init__(self, sg):
		super(IfNode, self).__init__(sg, 1)
		self.thn = None
		self.els = None

	def bindThen(self, sg):
		self.bind(sg)
		self.thn = sg
		sg.name  = "cmp_if_thn_%d" % self.id

	def bindElse(self, sg):
		self.bind(sg)
		self.els = sg
		sg.name  = "cmp_if_els_%d" % self.id

	def __iter__(self):
		return iter((self.thn, self.els))

class ForNode(CompoundNode):
	def __init__(self, sg):
		super(ForNode, self).__init__(sg, 1)
		self.body = None

	def bindBody(self, body):
		self.bind(body)
		self.body  = body
		body.name  = "cmp_forin_%d" % self.id

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

	def bindMany(self, lst):
		for el in lst:
			self.bind(el)

	def isBound(self, target):
		raise NotImplementedError

	def removeBound(self, target):
		raise NotImplementedError

	def isLit(self): return False

class Port(BindAble): 
	def __init__(self, node, idx):
		super(Port, self).__init__()
		self.node = node
		self.idx  = idx

class InPort(Port):
	def __init__(self, node, idx):
		super(InPort, self).__init__(node, idx)
		self.src = None

	def bind(self, src):
		self.src = src

	def isBound(self):
		return self.src is not None

	def hasLit(self):
		return self.isBound() and self.src.isLit()

class OutPort(Port):
	def __init__(self, node, idx):
		super(OutPort, self).__init__(node, idx)
		self.targets = []

	def bind(self, target):
		self.targets.append(target)
		target.typ = self.typ
		target.bind(self)

	def isBound(self):
		return self.targets != []

	def removeBound(self, target):
		self.targets.remove(target)

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
			l = Literal(self.val, self.typ)
			l.bind(target)
		else:
			self.dst = target
			target.src = self
			target.typ = self.typ

	def isBound(self):
		return self.dst is not None

	def removeBound(self, target):
		self.dst.src = None
		self.dst = None
