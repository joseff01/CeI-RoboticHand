
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'A1 A2 A3 BOOLEAN CLOSE_P COMMA COMMENTARY DISTINCT DIVIDE EQUALS EQUALS_EQUALS EXP INT INT_DIV LESS_EQUAL LESS_THAN LET MINUS MORE_EQUAL MORE_THAN MULTIPLY OPEN_P OPERA PLUS PyC VARIABLE\n    calc : expression\n         | var_assign\n        | empty\n    \n    var_assign : LET VARIABLE EQUALS expression PyC\n              | LET VARIABLE EQUALS VARIABLE\n    \n    empty :\n    \n    expression : OPERA OPEN_P PLUS COMMA expression COMMA expression CLOSE_P\n          | OPERA OPEN_P MINUS COMMA expression COMMA expression CLOSE_P\n          | OPERA OPEN_P INT_DIV COMMA expression COMMA expression CLOSE_P\n          | OPERA OPEN_P DIVIDE COMMA expression COMMA expression CLOSE_P\n          | OPERA OPEN_P EXP COMMA expression COMMA expression CLOSE_P\n          | OPERA OPEN_P MULTIPLY COMMA expression COMMA expression CLOSE_P\n    \n    expression : INT\n              | BOOLEAN\n    '
    
_lr_action_items = {'OPERA':([0,17,18,19,20,21,22,23,33,34,35,36,37,38,],[5,5,5,5,5,5,5,5,5,5,5,5,5,5,]),'INT':([0,17,18,19,20,21,22,23,33,34,35,36,37,38,],[6,6,6,6,6,6,6,6,6,6,6,6,6,6,]),'BOOLEAN':([0,17,18,19,20,21,22,23,33,34,35,36,37,38,],[7,7,7,7,7,7,7,7,7,7,7,7,7,7,]),'LET':([0,],[8,]),'$end':([0,1,2,3,4,6,7,24,32,45,46,47,48,49,50,],[-6,0,-1,-2,-3,-13,-14,-5,-4,-7,-8,-9,-10,-11,-12,]),'OPEN_P':([5,],[9,]),'PyC':([6,7,25,45,46,47,48,49,50,],[-13,-14,32,-7,-8,-9,-10,-11,-12,]),'COMMA':([6,7,11,12,13,14,15,16,26,27,28,29,30,31,45,46,47,48,49,50,],[-13,-14,18,19,20,21,22,23,33,34,35,36,37,38,-7,-8,-9,-10,-11,-12,]),'CLOSE_P':([6,7,39,40,41,42,43,44,45,46,47,48,49,50,],[-13,-14,45,46,47,48,49,50,-7,-8,-9,-10,-11,-12,]),'VARIABLE':([8,17,],[10,24,]),'PLUS':([9,],[11,]),'MINUS':([9,],[12,]),'INT_DIV':([9,],[13,]),'DIVIDE':([9,],[14,]),'EXP':([9,],[15,]),'MULTIPLY':([9,],[16,]),'EQUALS':([10,],[17,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'calc':([0,],[1,]),'expression':([0,17,18,19,20,21,22,23,33,34,35,36,37,38,],[2,25,26,27,28,29,30,31,39,40,41,42,43,44,]),'var_assign':([0,],[3,]),'empty':([0,],[4,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> calc","S'",1,None,None,None),
  ('calc -> expression','calc',1,'p_calc','compiler.py',102),
  ('calc -> var_assign','calc',1,'p_calc','compiler.py',103),
  ('calc -> empty','calc',1,'p_calc','compiler.py',104),
  ('var_assign -> LET VARIABLE EQUALS expression PyC','var_assign',5,'p_var_assign','compiler.py',111),
  ('var_assign -> LET VARIABLE EQUALS VARIABLE','var_assign',4,'p_var_assign','compiler.py',112),
  ('empty -> <empty>','empty',0,'p_empty','compiler.py',120),
  ('expression -> OPERA OPEN_P PLUS COMMA expression COMMA expression CLOSE_P','expression',8,'p_expression','compiler.py',127),
  ('expression -> OPERA OPEN_P MINUS COMMA expression COMMA expression CLOSE_P','expression',8,'p_expression','compiler.py',128),
  ('expression -> OPERA OPEN_P INT_DIV COMMA expression COMMA expression CLOSE_P','expression',8,'p_expression','compiler.py',129),
  ('expression -> OPERA OPEN_P DIVIDE COMMA expression COMMA expression CLOSE_P','expression',8,'p_expression','compiler.py',130),
  ('expression -> OPERA OPEN_P EXP COMMA expression COMMA expression CLOSE_P','expression',8,'p_expression','compiler.py',131),
  ('expression -> OPERA OPEN_P MULTIPLY COMMA expression COMMA expression CLOSE_P','expression',8,'p_expression','compiler.py',132),
  ('expression -> INT','expression',1,'p_expression_int_boolean','compiler.py',139),
  ('expression -> BOOLEAN','expression',1,'p_expression_int_boolean','compiler.py',140),
]
