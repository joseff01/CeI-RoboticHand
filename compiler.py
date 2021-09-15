import ply.lex as lex
import re
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
t_LET = r'let'
t_OPERA = r'OPERA'


def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_BOOLEAN(t):
    r'True | False'
    t.type = 'BOOLEAN'
    return t

def t_VARIABLE(t):
    r'[a-zA-Z]{3,15}'
    t.type = 'VARIABLE'
    return t


def t_error(t):
    print("illegal character detected")
    t.lexer.skip(1)


def p_expression(p):
    '''
    expression: INT
              | BOOLEAN
    '''


def p_var_assign(p):
    '''
    var_assign: VARIABLE EQUALS expression PYC
              | VARIABLE EQUALS VARIABLE PYC
    '''


lexer = lex.lex()

lexer.input("False")

while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)