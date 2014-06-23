# error.py
# Mathijs Saey
# DLC

# This module contains the errors that 
# the frontend may throw.

# ----------------- #
# Error Definitions #
# ----------------- #

class FrontEndError(Exception): 
	def __init__(self):
		self.pool = []

	def add(self, error):
		self.pool.append(error)

	def show(self):
		for err in self.pool:
			print err

	def verify(self):
		if self.pool:
			self.show()
			raise self

class SourceError(Exception): 
	def __init__(self, src, lin, col, len, msg):
		self.src = src
		self.lin = lin
		self.col = col
		self.len = len
		self.msg = msg

	def __repr__(self):
		return "(%d:%d): %s" (self.lin, self.col, self.msg)

	def __str__(self):
		msg = "(%d:%d) %s" % (self.lin, self.col, self.msg)
		src = "\t%s" % self.src

		idx     = self.col - 1
		tabs    = self.src[:idx].count('\t')
		spaces  = idx - tabs

		# Line which marks the error
		mrk = "\t%s%s%s" % ("\t" * tabs, " " * spaces, "~" * self.len)

		return '%s\n%s\n%s' % (msg, src, mrk)

class EOFError(Exception):
	def __str__(self):
		return "End of file reached before parser finished."

# -------------- #
# Error Handling #
# -------------- #

def fromLines(lines, lineno, lexpos, length, msg):
	startIdx = lines.rfind('\n', 0, lexpos) + 1
	stopIdx  = lines.find('\n', lexpos)

	if startIdx < 0 : startIdx = 0
	if stopIdx  < 0 : stopIdx  = len(lines)

	return SourceError(
				lines[startIdx:stopIdx],
				lineno,
				(lexpos - startIdx) + 1,
				length,
				msg
			)

def fromToken(token, length, message):
		lines  = token.lexer.lexdata
		lexpos = token.lexpos

		return fromLines(
			lines,
			token.lineno,
			lexpos,
			length,
			message
		)

def fromProduction(production, idx, message):
	lines  = production.lexer.lexdata
	lexpos = production.lexpos(idx)
	lineno = production.lineno(idx)

	return fromLines(
		lines,
		lineno,
		lexpos,
		len(production[idx]),
		message
		)
	
# ---------- #
# Error Pool #
# ---------- #

__POOL__ = FrontEndError()
def add(err): __POOL__.add(err)
def verify(): __POOL__.verify()

# -------------- #
# Error creation #
# -------------- #

def illegalChar(token):
	add(fromToken(token, 1, "Illegal character"))

def syntax(token):
	try:
		add(fromToken(token, len(token.value), "Syntax error"))
	except TypeError:
		add(fromToken(token, 1, "Syntax error"))

def eof():
	add(EOFError())

def duplicateFunc(production, idx):
	add(fromProduction(production, idx, "Duplicate function name"))

def duplicateName(production, idx):
	add(fromProduction(production, idx, "Duplicate name encountered"))

def unknownFunc(production, idx):
	add(fromProduction(production, idx, "Unknown function name encountered"))

def unknownName(production, idx):
	add(fromProduction(production, idx, "Unknown name encountered"))

def wrongArgCount(production, idx):
	add(fromProduction(production, idx, "Function called with incorrect amount of arguments"))

def wrongType(production, idx):
	add(fromProduction(production, idx, "Incorrect type"))