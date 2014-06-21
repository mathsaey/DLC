# error.py
# Mathijs Saey
# DLC

# This module contains the definitions of 
# some custom errors.

class DLCError(Exception):
	def __init__(self, line, lineno, message, colStart, colStop):
		self.line = line
		self.lineno = lineno
		self.message = message

		self.colStart = colStart
		self.colStop  = colStop

	def __str__(self):
		mrkStart = self.colStart - 1
		mrkStop  = self.colStop - self.colStart

		err = "(%d:%d) Error: %s" % (self.lineno, self.colStart, self.message)
		lin = "\t%s" % self.line
		mrk = "\t%s%s" % (" " * mrkStart, "~" * mrkStop)
		return '%s\n%s\n%s' % (err, lin, mrk)