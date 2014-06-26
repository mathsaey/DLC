#!/usr/bin/env python

# run.py
# Mathijs Saey
# DLC

# This file compiles and runs the various example files

import unittest
import subprocess

DVM_PATH  = "dvm"
DLC_PATH = "../src/dlc.py"

class Test(unittest.TestCase):

	def compile(self, path, args = []):
		print "Compiling", path
		subprocess.check_call([DLC_PATH, path] + args)

	def runDvm(self, path, inputs):
		print "Running", path
		args = [DVM_PATH, path, '-ll', '40']

		for e in inputs:
			args.append("-i")
			args.append(str(e))

		return subprocess.check_output(args).strip()

	def abstract(self, name, inputs, expected, args = []):
		self.compile(name + '.dfl', args)
		res = self.runDvm(name + '.dis', inputs)
		self.assertEqual(res, expected)

	def test_cse(self): self.abstract('cse', ['4', '10'], '4900')
	def test_fac(self): self.abstract('factorial', ['5'], '120')
	def test_fib(self): self.abstract('fibonacci', ['10'], '55')
	def test_for(self): self.abstract('forin', ['1', '10', '3', '4'], '[15, 16, 17, 18, 19, 20, 21, 22, 23, 24]')

unittest.main()