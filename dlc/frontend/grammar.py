# grammer.py
# Mathijs Saey
# DLC

# This module has no practical use
# It merely exists to summarize the dl grammar 
# All of the implementation specific rules are
# removed from this grammar.

'''
 S'             : program
 program        : function_list
                | <empty>

 function_list  : function function_list
                | function

 function       : signature COL expression

 signature      : FUNC NAME LPAREN parLst RPAREN

 parLst         : NAME SEP parLst
                | NAME
                | <empty>

 expression     : NAME
                | NUM
                | TRUE
                | FALSE
                | array
                | range
                | arrAccess
                | call
                | letin
                | forin
                | ifthenelse
                | operation

 letin          : LET bindLst IN expression
 bindLst        : bind bindLst
                | bind
 bind           : NAME BIND expression

 ifthenelse     : IF expression THEN expression ELSE expression

 forin          : FOR NAME IN DO expression

 call           : NAME LPAREN argLst RPAREN

 argLst         : expression SEP argLst
                | expression
                | <empty>

 array          : LBRACK argLst RBRACK
 arrAccess      : expression LBRACK expression RBRACK
 range          : LBRACK expression DOT DOT expression RBRACK

operation       : expression PLUS expression
                | expression MIN expression
                | expression MUL expression
                | expression DIV expression
                | expression LT expression
                | expression LTEQ expression
                | expression GT expression
                | expression GTEQ expression
                | expression EQ expression
                | expression AND expression
                | expression OR expression
                | LPAREN expression RPAREN
                | NOT expression
                | MIN expression
'''