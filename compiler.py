import ply.lex as lex
import ply.yacc as yacc
import sys
"""Define los tokens validos para el lexer"""
tokens = [
    'INT',
    'LET',
    'OPERA',
    'EXP',
    'BOOLEAN',
    'VARIABLE',
    'PLUS',
    'MINUS',
    'DIVIDE',
    'MULTIPLY',
    'EQUALS',
    'INT_DIV',
    'OPEN_P',
    'CLOSE_P',
    'COMMA',
    'EQUALS_EQUALS',
    'DISTINCT',
    'LESS_EQUAL',
    'MORE_EQUAL',
    'MORE_THAN',
    'LESS_THAN',
    'COMMENTARY',
    'PyC',
    'A1',
    'A2',
    'A3'
]
"""Le dice a lex como se ven los tokens definidos anteriormente"""

t_PLUS = r'\+'
t_MINUS = r'\-'
t_INT_DIV = r'\//'
t_DIVIDE = r'\/'
t_EXP = r'\*\*'
t_MULTIPLY = r'\*'
t_EQUALS_EQUALS = r'\=='
t_EQUALS = r'\='
t_OPEN_P = r'\('
t_CLOSE_P = r'\)'
t_COMMA = r'\,'
t_DISTINCT = r'\<>'
t_LESS_EQUAL = r'\<='
t_LESS_THAN = r'\<'
t_MORE_EQUAL = r'\>='
t_MORE_THAN = r'\>'
t_COMMENTARY = r'\@'
t_PyC = r'\;'
t_A1 = r'\#'
t_A2 = r'\?'
t_A3 = r'\_'

t_ignore = r' '

"""Definicion de algunos tokens como funciones(nota: definir palabras especificas antes de la definicion de variable)"""
def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_BOOLEAN(t):
    r'True | False'
    t.type = 'BOOLEAN'
    return t


def t_OPERA(t):
    r'OPERA'
    t.type = 'OPERA'
    return t


def t_LET(t):
    r'let'
    t.type = 'LET'
    return t


def t_VARIABLE(t):
    r'[a-zA-Z]{3,15}'
    t.type = 'VARIABLE'
    return t


def t_error(t):
    print("illegal character detected")
    t.lexer.skip(1)


lexer = lex.lex()

"""Definicion de funciones del parser"""


def p_calc(p):
    '''
    calc : expression
         | var_assign
        | empty
    '''
    print(p[1])


def p_var_assign(p):
    '''
    var_assign : LET VARIABLE EQUALS expression
              | LET VARIABLE EQUALS VARIABLE
    '''

    p[0] = ('=', p[2], p[4])


def p_empty(p):
    '''
    empty :
    '''
    p[0] = None


def p_expression(p):
    '''
    expression : OPERA OPEN_P expression PLUS expression CLOSE_P
          | OPERA OPEN_P expression MINUS expression CLOSE_P
          | OPERA OPEN_P expression INT_DIV expression CLOSE_P
          | OPERA OPEN_P expression DIVIDE expression CLOSE_P
          | OPERA OPEN_P expression EXP expression CLOSE_P
          | OPERA OPEN_P expression MULTIPLY expression CLOSE_P
    '''
    p[0] = (p[4], p[3], p[5])


def p_expression_int_boolean(p):
    '''
    expression : INT
              | BOOLEAN
    '''
    p[0] = p[1]

parser = yacc.yacc()

while True:
    try:
        s = input('')
    except EOFError:
        break
    parser.parse(s)