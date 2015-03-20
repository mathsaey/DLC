# __init__.py
# Mathijs Saey
# DLC

# This package contains the backend,
# which generates DIS code from a valid
# IGR graph of the program

import dis
import IGR
import converter

from dvm import run

class NodeMap(object):
	def __init__(self):
		self.srcMap = {}
		self.dstMap = {}
		self.namMap = {}
		self.calMap = {}

	def add(self, key, src, dst):
		self.srcMap.update({key : src})
		self.dstMap.update({key : dst})

	def addName(self, name, dst):
		self.namMap.update({name : dst})
		if name in self.calMap:
			for f in self.calMap[name]:
				f(dst)
			del self.calMap[name]

	def addCall(self, name, f):
		if name in self.calMap:
			lst = self.calMap[name] + [f]
			self.calMap.update({name : lst})
		else:
			self.calMap.update({name : [f]})

	def getSrc(self,  key): return self.srcMap[key]
	def getDst(self,  key): return self.dstMap[key]
	def getName(self, key): return self.namMap[key]
	def namePresent(self, name): return name in self.namMap


def convert(graph, entry = 'main', linkTo = None):
	main = graph[entry]
	args = main.args if not linkTo else linkTo.args

	if args == 0: return "TRIV <= %s" % main.exit.src.val

	prog = dis.DIS(args)
	map  = NodeMap()
	converter.subGraphs(graph, prog, map)

	if linkTo:
		dstC, dstK = map.getDst(linkTo)
		srcC, srcK = map.getSrc(linkTo)
		prog.linkStart(dstC, dstK)
		prog.linkStop(srcC, srcK)
	else:
		prog.addCommentLine("Implicit call to main", 0)
		mainKey      = map.getName(entry)
		callC, callK = prog.addInstruction(0, 'CHN', [args, 1, mainKey[0], mainKey[1], 0, 1])
		prog.linkStart(callC, callK)

	return prog.generate()
