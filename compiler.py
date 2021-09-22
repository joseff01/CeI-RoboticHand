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
    'FOR',
    'WHILE',
    'IN',
    'VARIABLE',
    'PLUS',
    'MINUS',
    'DIVIDE',
    'MULTIPLY',
    'EQUALS',
    'INT_DIV',
    'OPEN_P',
    'CLOSE_P',
    'SB1',
    'SB2',
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
    'A3',
    'dDOT_E',
    'dDOT'
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
t_dDOT_E = r'\.\.\='
t_dDOT = r'\.\.'

t_ignore = r' '

"""Definicion de algunos tokens como funciones(nota: definir palabras especificas antes de la definicion de variable)"""

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    print("line:",t.lexer.lineno)

def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_BOOLEAN(t):
    r'True | False'
    t.type = 'BOOLEAN'
    return t

def t_SB1(t):
    r'\{'
    t.type = 'SB1'
    return t

def t_SB2(t):
    r'\}'
    t.type = 'SB2'
    return t

def t_WHILE(t):
    r'while'
    t.type = 'WHILE'
    return t

def t_FOR(t):
    r'for'
    t.type = 'FOR'
    return t

def t_IN(t):
    r'in'
    t.type = 'IN'
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
    r'[a-zA-Z#_?][a-zA-Z0-9#_?]{2,14}'
    t.type = 'VARIABLE'
    return t


def t_error(t):
    print("illegal character detected")
    t.lexer.skip(1)


lexer = lex.lex()

"""Definicion de funciones del parser"""

def p_lines(p):
    '''
    algorithm : algorithm algorithm_line
            | empty
    '''
    p[0] = p[1]


def p_first_section(p):
    '''
    algorithm_line : expression PyC
                    | var_assign PyC
                    | for_loop PyC
                    | while_loop PyC
    '''
    p[0] = p[1]
    print(run(p[1]))

def p_operator(p):
    '''
    operator : PLUS
            | MINUS
            | INT_DIV
            | DIVIDE
            | EXP
            | MULTIPLY
    '''
    p[0] = p[1]

def p_expression_opera(p):
    '''
    expression : OPERA OPEN_P operator COMMA expression COMMA expression CLOSE_P
    '''
    p[0] = (p[3], p[5], p[7])


def p_var_assign(p):
    '''
    var_assign : LET VARIABLE EQUALS expression
    '''

    p[0] = ('=', p[2], p[4])


def p_for_loop(p):
    '''
    for_loop : FOR INT IN INT dDOT INT SB1 algorithm SB2
              | FOR VARIABLE IN INT dDOT INT SB1 algorithm SB2
              | FOR INT IN INT dDOT_E INT SB1 algorithm SB2
              | FOR VARIABLE IN INT dDOT_E INT SB1 algorithm SB2
    '''

    p[0] = ('for_loop', p[2], p[4], p[6], p[8], p[5])

def p_while_loop(p):
    '''
    while_loop : WHILE OPEN_P VARIABLE DISTINCT INT CLOSE_P SB1 expression SB2
               | WHILE OPEN_P VARIABLE DISTINCT VARIABLE CLOSE_P SB1 expression SB2
               | WHILE OPEN_P VARIABLE LESS_EQUAL INT CLOSE_P SB1 expression SB2
               | WHILE OPEN_P VARIABLE LESS_EQUAL VARIABLE CLOSE_P SB1 expression SB2
               | WHILE OPEN_P VARIABLE LESS_THAN INT CLOSE_P SB1 expression SB2
               | WHILE OPEN_P VARIABLE LESS_THAN VARIABLE CLOSE_P SB1 expression SB2
               | WHILE OPEN_P VARIABLE MORE_EQUAL INT CLOSE_P SB1 expression SB2
               | WHILE OPEN_P VARIABLE MORE_EQUAL VARIABLE CLOSE_P SB1 expression SB2
               | WHILE OPEN_P VARIABLE MORE_THAN INT CLOSE_P SB1 expression SB2
               | WHILE OPEN_P VARIABLE MORE_THAN VARIABLE CLOSE_P SB1 expression SB2
               | WHILE OPEN_P VARIABLE EQUALS_EQUALS INT CLOSE_P SB1 expression SB2
               | WHILE OPEN_P VARIABLE EQUALS_EQUALS VARIABLE CLOSE_P SB1 expression SB2
               | WHILE OPEN_P VARIABLE EQUALS INT CLOSE_P SB1 expression SB2
               | WHILE OPEN_P VARIABLE EQUALS VARIABLE CLOSE_P SB1 expression SB2
    '''
    p[0] = ('while_loop', p[3])

def p_empty(p):
    '''
    empty :
    '''
    p[0] = None


def p_expression_int_boolean(p):
    '''
    expression : INT
              | BOOLEAN
    '''
    p[0] = p[1]


def p_expression_var(p):
    '''
    expression : VARIABLE
    '''
    p[0] = ('var', p[1])


parser = yacc.yacc()


variables = {}


def run(p):
    global variables
    if type(p) == tuple:
        if p[0] == '+':
            return run(p[1]) + run(p[2])
        elif p[0] == '-':
            return run(p[1]) - run(p[2])
        elif p[0] == '//':
            return run(p[1]) // run(p[2])
        elif p[0] == '/':
            return int(run(p[1]) / run(p[2]))
        elif p[0] == '**':
            return run(p[1]) ** run(p[2])
        elif p[0] == '*':
            return run(p[1]) * run(p[2])

        elif p[0] == '=':
            if len(variables) > 0 and variables.get(p[1]) is not None and isinstance(variables[p[1]], int) is True and isinstance(run(p[2]), str) is True:
                print('Tipo incompatible')

            elif len(variables) > 0 and variables.get(p[1]) is not None and isinstance(variables[p[1]], str) is True and isinstance(run(p[2]), int) is True:
                print('Tipo incompatible')

            else:
                variables[p[1]] = run(p[2])
                print(variables)

        elif p[0] == 'var':
            return variables[p[1]]

        elif p[0] == 'for_loop':
            if len(variables) > 0 and variables.get(p[1]) is not None and isinstance(variables[p[1]], str) is True:
                print('No puede usar variables booleans en bucles for')

            elif p[2] >= p[3]:
                print('Ingrese un rango valido')

            elif len(variables) > 0 and variables.get(p[1]) is not None and (variables[p[1]] > p[3] or variables[p[1]] < p[4]):
                print('La condicion se sale del rango del For')

            elif len(variables) == 0 and (p[1] < p[2] or p[1] > p[3]):
                print('La condicion se sale del rango del For')

            else:
                if p[5] == '..' and isinstance(p[1], str) is True and variables.get(p[1]) is None:
                    print('Variable no definida')
                elif p[5] == '..' and isinstance(p[1], str) is True and variables.get(p[1]) is not None:
                    for variables[run(p[1])] in range(p[2], p[3]-1):
                        print(run(p[4]))
                    return p
                elif p[5] == '..' and isinstance(p[1], int) is True:
                    pointer = int(p[1])
                    for pointer in range(p[2], p[3]-1):
                        print(run(p[4]))
                    return p

                elif p[5] == '..=' and isinstance(p[1], str) is True and variables.get(p[1]) is None:
                    print('Variable no definida')
                elif p[5] == '..=' and isinstance(p[1], str) is True and variables.get(p[1]) is not None:
                    for variables[p[1]] in range(p[2], p[3]):
                        print(run(p[4]))
                    return p
                elif p[5] == '..=' and isinstance(p[1], int) is True:
                    pointer = int(p[1])
                    for pointer in range(p[2], p[3]):
                        print(run(p[4]))
                    return p
                
                else:
                    return p
        elif p[0] == 'while_loop':
            print('detected')
    else:
        return p


def clearAll():
    global variables
    variables = {}
    lexer.lineno = 1


def compile(text):
    print(lexer.lineno)
    print(text)
    parser.parse(text)
    clearAll()
