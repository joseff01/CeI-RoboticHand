import ply.lex as lex
import ply.yacc as yacc
import sys
"""Define los tokens validos para el lexer"""
tokens = [
    'INT',
    'LET',
    'VARIABLE',
    'OPERA',
    'PLUS',
    'MINUS',
    'DIVIDE',
    'MULTIPLY',
    'EQUALS',
    'EXP',
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
    'COMMENTARY'
]
"""Le dice a lex como se ven los tokens definidos anteriormente"""
t_LET = r'\let'
t_PLUS = r'\+'
t_MINUS = r'\-'
t_OPERA = r'\OPERA'
t_INT_DIV = r'\//'
t_DIVIDE = r'\/'
t_EXP = r'\**'
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


def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_VARIABLE(t):
    r'[a-zA-Z][a-zA-Z_0-9]'
    t.type = 'VARIABLE'
    return t


def t_error(t):
    print("illegal character detected")
    t.lexer.skip(1)


lexer = lex.lex()
