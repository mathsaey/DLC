# dvm.py
# Mathijs Saey
# DLC

# This module is responsible for the interaction
# with DVM

import sys
import subprocess

def run(inputs, dis):
	args = ['dvm', "-"]

	for e in inputs:
		args.append("-i")
		args.append(str(e))

	dvm = subprocess.Popen(args, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
	res = dvm.communicate(dis)
	ret = dvm.returncode

	if ret:
		print >> sys.stderr, "DVM returned non-zero return code", ret
	return res[0].strip()