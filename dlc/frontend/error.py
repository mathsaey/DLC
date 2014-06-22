# error.py
# Mathijs Saey
# DLC

# This module contains the errors that 
# the frontend may throw.

# ----------------- #
# Error Definitions #
# ----------------- #

class FrontEndError(Exception): pass

class TokenError(Exception): 
	def __init__(self, token, length, message):
		lines  = token.lexer.lexdata
		lexpos = token.lexpos

		startIdx = lines.rfind('\n', 0, lexpos) + 1
		stopIdx  = lines.find('\n', lexpos)

		if startIdx < 0 : startIdx = 0
		if stopIdx  < 0 : stopIdx  = len(lines)

		self.line     = lines[startIdx:stopIdx]
		self.lineno   = token.lineno
		self.colStart = (lexpos - startIdx) + 1
		self.length   = length
		self.message  = message

	def __repr__(self):
		return "(%d:%d): %s" (self.lineno, self.colStart, self.message)

	def __str__(self):
		# Error message
		error = "(%d:%d) Error: %s" % (self.lineno, self.colStart, self.message)

		# Line with Error
		line = "\t%s" % self.line

		markIdx  = self.colStart - 1
		tabs     = self.line[:markIdx].count('\t')
		spaces   = markIdx - tabs

		# Line which marks the error
		mark = "\t%s%s%s" % ("\t" * tabs, " " * spaces, "~" * self.length)

		return '%s\n%s\n%s' % (error, line, mark)

class IllegalCharError(TokenError):
	def __init__(self, token):
		super(IllegalCharError, self).__init__(
			token, 1, "Illegal character")

class SyntaxError(TokenError):
	def __init__(self, token):
		super(SyntaxError, self).__init__(
			token, len(token.value), "Syntax error")


# ---------- #
# Error Pool #
# ---------- #

__POOL__ = []

def add(err):
	__POOL__.append(err)

def verify():
	if __POOL__:
		for err in __POOL__:
			print err
		raise FrontEndError()