# natives.py
# Mathijs Saey
# DLC

# This file defines a list of natives DIS functions.

__natives__ = {}

def isNative(name):
	return name in __natives__

def get(name):
	return __natives__[name]

class Native(object):
	def __init__(self, name, disName, inTypes, outType):
		super(Native, self).__init__()
		self.name    = name
		self.disName = disName
		self.inTypes = inTypes
		self.outType = outType
		self.addNative()

	def addNative(self):
		global __natives__
		__natives__.update({self.name : self})

Native( 'bool',          'bool',        (None,),           bool  )
Native( 'int',           'int',         (None,),           int   )
Native( 'flt',           'float',       (None,),           int   )
Native( 'str',           'string',      (None,),           str   )
Native( 'arr',           'array',       (None,),           list  )
Native( 'tup',           'tuple',       (None,),           tuple )
Native( 'floor',         'floor',       (None,),           int   )
Native( 'ceil',          'ceil',        (None,),           int   )
Native( 'min',           'min',         (None,),           None  )
Native( 'max',           'max',         (None,),           None  )
Native( 'str_contains',  'strContains', (str, str,),       bool  )
Native( 'str_find',      'strFind',     (str, str,),       int   )
Native( 'str_upperCase', 'strUpper',    (str,),            str   )
Native( 'str_lowerCase', 'strLower',    (str,),            str   )
Native( 'str_substring', 'strSub',      (str, int,),       str   )
Native( 'str_reverse',   'strRev',      (str,),            str   )
Native( 'str_append',    'strApp',      (list, list,),     list  ) 
Native( 'arr_empty',     'arrIsEmpty',  (list,),           bool  )
Native( 'arr_length',    'arrLen',      (list,),           int   )
Native( 'arr_create',    'arrCreate',   (int, None,),      list  )
Native( 'arr_concat',    'arrCat',      (list, list,),     list  )
Native( 'arr_subset',    'arrSub',      (list, int, int,), list  )
