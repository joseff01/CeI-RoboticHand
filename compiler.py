import ply.lex as lex
import ply.yacc as yacc
import sys

reserved = {
    'let'	 : 'LET',
    'while'	 : 'WHILE',
    'for'	 : 'FOR',
    'if'	 : 'IF',
    'else'	 : 'ELSE',
    'in'	 : 'IN',
    'OPERA'	 : 'OPERA',
    'true'	 : 'BOOLEAN',
    'false'	 : 'BOOLEAN',
    'boolean': 'BOOLEAN_TXT',
    'integer': 'INTEGER_TXT',
    'fn'     : 'FUNCTION',
    'return' : 'RETURN',
    'Move'   : 'MOVE',
}
            
"""Define los tokens validos para el lexer"""
tokens = [
    'INT',
    'EXP',
    'THUMB',
    'INDEX',
    'MIDDLE',
    'ANULAR',
    'PINKY',
    'ALL',
    'ARROW',
    'PRINT',
    'STR',
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
    'SQ1',
    'SQ2',
    'COMMA',
    'EQUALS_EQUALS',
    'DISTINCT',
    'LESS_EQUAL',
    'MORE_EQUAL',
    'MORE_THAN',
    'LESS_THAN',
    'COMMENT',
    'PyC',
    'dDOT_E',
    'dDOT',
] + list(set(reserved.values())) # first turn into a set to remove duplicate BOOLEAN values
"""Le dice a lex como se ven los tokens definidos anteriormente"""

t_PLUS = r'\+'
t_ARROW = r'\->'
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
t_PyC = r'\;'
t_dDOT_E = r'\.\.\='
t_dDOT = r'\.\.'

t_ignore = r' '

"""Definicion de algunos tokens como funciones(nota: definir palabras especificas antes de la definicion de variable)"""


def t_THUMB(t):
    r'\"P\"'
    t.type = 'THUMB'
    return t
def t_INDEX(t):
    r'\"I\"'
    t.type = 'INDEX'
    return t
def t_MIDDLE(t):
    r'\"M\"'
    t.type = 'MIDDLE'
    return t
def t_ANULAR(t):
    r'\"A\"'
    t.type = 'ANULAR'
    return t
def t_PINKY(t):
    r'\"Q\"'
    t.type = 'PINKY'
    return t
def t_ALL(t):
    r'\"T\"'
    t.type = 'ALL'
    return t

def t_PRINT(t):
    r'println\!'
    t.type = 'PRINT'
    return t

def t_STR(t):
    r"\"[a-zA-Z ]+\""
    t.value = t.value[1:-1]
    t.type = 'STR'
    return t

def t_COMMENT(t):
    r'\@.*'
    pass

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    print("line:",t.lexer.lineno)

def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_SB1(t):
    r'\{'
    t.type = 'SB1'
    return t

def t_SB2(t):
    r'\}'
    t.type = 'SB2'
    return t

def t_SQ1(t):
    r'\['
    t.type = 'SQ1'
    return t

def t_SQ2(t):
    r'\]'
    t.type = 'SQ2'
    return t

def t_ID(t):
    r'[a-zA-Z#_?][a-zA-Z0-9#_?]{0,14}'
    t.type = reserved.get(t.value,'VARIABLE')    # Check for reserved words
    if t.value == 'true':
        t.value = True
    elif t.value == 'false':
        t.value = False
    if(t.type == 'VARIABLE' and len(t.value) < 3):
        return t_error(t)
    #print("Lexer info")
    #print(t.value)
    #print(t.type)
    return t

def t_error(t):
    print("illegal character detected: '" + t.value + "'")
    t.lexer.skip(1)

lexer = lex.lex()

"""Definicion de funciones del parser"""

def p_algorithm(p):
    '''
    algorithm : algorithm algorithm_function
            | empty
    '''
    if len(p) == 3:
        p[0] = p[2]
        print(p[0])
        print(run(p[0]))

def p_algorithm_function(p):
    '''
    algorithm_function : method_def
                        | function_def
    '''
    p[0] = p[1]

def p_var_type(p):
    '''
    var_type : BOOLEAN_TXT
            | INTEGER_TXT
    '''
    print("function hoo haa")
    p[0] = p[1]

def p_function_def(p):
    '''
    function_def : FUNCTION VARIABLE OPEN_P parameters CLOSE_P ARROW var_type SB1 statement SB2
    '''
    p[0] = ('function_def', p[2], p[4], p[9], p[7])

def p_method_def(p):
    '''
    method_def : FUNCTION VARIABLE OPEN_P parameters CLOSE_P SB1 statement SB2
    '''
    p[0] = ('method_def', p[2], p[4], p[7])

def p_parameters(p):
    '''
        parameters : parameters COMMA parameters
                    | VARIABLE
                    | empty
    '''
    print("parameters hoo haa")
    if len(p) == 4:
        p[0] = (p[1],p[3])
    else:
        p[0] = p[1]

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

def p_fingers(p):
    '''
    fingers : THUMB
            | INDEX
            | MIDDLE
            | ANULAR
            | PINKY
            | ALL
    '''
    p[0] = (p[1])

def p_finger_list_A(p):
    '''
    fingerL_A : SQ1 fingers COMMA fingerL_B
    '''
    p[0] = (p[2], p[4])

def p_finger_list_B(p):
    '''
    fingerL_B : fingers COMMA fingerL_B
              | fingerL_C
    '''
    if len(p) > 2:
        p[0] = (p[1], p[3])
    else:
        p[0] = p[1]

def p_finger_list_C(p):
    '''
    fingerL_C : fingers SQ2
              | empty
    '''
    p[0] = p[1]

def p_hand_control(p):
    '''
    hand : fingerL_A fingerL_B fingerL_C
    '''
    p[0] = (p[1], p[2], p[3])

def p_function_move(p):
    '''
    function_move : MOVE OPEN_P fingers COMMA BOOLEAN CLOSE_P
                  | MOVE OPEN_P hand COMMA BOOLEAN CLOSE_P
    '''
    p[0] = ('Move', p[3], p[5])

def p_string_list_A(p):
    '''
    stringL_A : STR COMMA stringL_B
              | VARIABLE COMMA stringL_B
              | BOOLEAN COMMA stringL_B
              | INT COMMA stringL_B
    '''
    p[0] = (p[1], p[3])

def p_string_list_B(p):
    '''
    stringL_B : STR COMMA stringL_B
              | VARIABLE COMMA stringL_B
              | INT COMMA stringL_B
              | BOOLEAN COMMA stringL_B
              | stringL_C
    '''
    if len(p) > 2:
        p[0] = (p[1], p[3])
    else:
        p[0] = p[1]

def p_string_list_C(p):
    '''
    stringL_C : STR
              | VARIABLE
              | BOOLEAN
              | INT
              | empty
    '''
    p[0] = p[1]

def p_string_creator(p):
    '''
    Cstring : stringL_A stringL_B stringL_C
    '''
    p[0] = (p[1], p[2], p[3])

def p_function_print(p):
    '''
    function_print : PRINT OPEN_P STR CLOSE_P
                   | PRINT OPEN_P VARIABLE CLOSE_P
                   | PRINT OPEN_P BOOLEAN CLOSE_P
                   | PRINT OPEN_P INT CLOSE_P
                   | PRINT OPEN_P Cstring CLOSE_P
    '''

    p[0] = ('print', p[3])

def p_expression_opera(p):
    '''
    expression : OPERA OPEN_P operator COMMA expression COMMA expression CLOSE_P
    '''
    p[0] = (p[3], p[5], p[7])

def p_bool_operator(p):
    '''
        bool_operator : EQUALS_EQUALS
                    | DISTINCT
                    | LESS_EQUAL
                    | MORE_EQUAL
                    | MORE_THAN
                    | LESS_THAN
    '''
    p[0] = p[1]


def p_expression_bool(p):
    '''
    expression : expression bool_operator expression
    '''
    p[0] = (p[2], p[1], p[3])

def p_var_assign(p):
    '''
    var_assign : LET VARIABLE EQUALS expression
    '''

    p[0] = ('=', p[2], p[4])


def p_for_loop(p):
    '''
    for_loop : FOR INT IN INT dDOT INT SB1 statement SB2
              | FOR VARIABLE IN INT dDOT INT SB1 statement SB2
              | FOR INT IN INT dDOT_E INT SB1 statement SB2
              | FOR VARIABLE IN INT dDOT_E INT SB1 statement SB2
    '''

    p[0] = ('for_loop', p[2], p[4], p[6], p[8], p[5])

def p_if_else(p):
    '''
        if_else : IF expression SB1 statement SB2 else_if
    '''
    print("if-else processing...")
    print(len(p))
    p[0] = ('if_else', p[2], p[4], p[6])

def p_else_if(p):
    '''
        else_if : ELSE IF expression SB1 statement SB2 else_if
                | else_exp
    '''
    print("else_if processing...")
    print(len(p))
    if len(p) > 2:
        p[0] = ('if_else', p[3], p[5], p[7])
    else:
        p[0] = p[1]

def p_else_exp(p):
    '''
        else_exp : ELSE SB1 statement SB2
                | empty
    '''
    print("else processing...")
    print(len(p))
    if len(p) > 2:
        p[0] = p[3]
    else:
        p[0] = p[1]


def p_statement(p):
    '''
    statement : statement statement_line
            | empty
    '''
    if len(p) == 3:
        p[0] = ('statement', p[1], p[2])

def p_statement_line(p):
    '''
    statement_line : if_else
                    | expression PyC
                    | var_assign PyC
                    | for_loop
                    | while_loop
                    | function_move PyC
                    | function_print PyC
    '''
    p[0] = p[1]

def p_statement_line_return(p):
    '''
    statement_line : RETURN expression PyC
    '''
    p[0] = ('return', p[2])

def p_while_loop(p):
    '''
    while_loop : WHILE OPEN_P expression CLOSE_P SB1 statement SB2
    '''
    p[0] = ('while_loop', p[3], p[6])

def p_empty(p):
    '''
    empty :
    '''
    p[0] = None


def p_expression_int_boolean(p):
    '''
    expression : INT
              | BOOLEAN
              | function_call
    '''
    p[0] = p[1]


def p_expression_var(p):
    '''
    expression : VARIABLE
    '''
    p[0] = ('var', p[1])

def p_function_call(p):
    '''
    function_call : VARIABLE OPEN_P param_expressions CLOSE_P
    '''
    p[0] = ('fn', p[1], p[3])

def p_param_expresions(p):
    '''
    param_expressions : param_expressions COMMA param_expressions
                    | expression
                    | empty
    '''
    if len(p) == 4:
        p[0] = (p[1], p[3])
        print("parameters:", p[0])
    else:
        p[0] = p[1]


parser = yacc.yacc()

variables = {}

functions_methods = {}

tuple_elements = []

phrase = []

def length_variables(variable_list):
    if isinstance(variable_list,tuple):
        return 1 + length_variables(variable_list[1])
    elif (isinstance(variable_list, str)) or (isinstance(variable_list, bool)) or (isinstance(variable_list, int)):
        return 1
    elif variable_list is None:
        return 0


def add_parameter_variables(parametersTuple, parameterNames):
    if isinstance(parametersTuple,tuple):
        variables[parameterNames[0]] = run(parametersTuple[0])
        add_parameter_variables(parametersTuple[1], parameterNames[1])
    elif (isinstance(parametersTuple, int)) or (isinstance(parametersTuple, bool)):
        variables[parameterNames] = run(parametersTuple)
    elif parametersTuple is None:
        return


def remove_parameter_variables(parametersTuple, parameterNames):
    if isinstance(parametersTuple,tuple):
        variables.pop(parameterNames[0])
        remove_parameter_variables(parametersTuple[1], parameterNames[1])
    elif (isinstance(parametersTuple, int)) or (isinstance(parametersTuple, bool)):
        variables.pop(parameterNames)
    elif parametersTuple is None:
        return


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
        elif p[0] == 'var':
            return variables[p[1]]

        elif p[0] == '==':
            if (isinstance(p[1], int) is False and variables.get(p[1][1]) is None) or (isinstance(p[2], int) is False and variables.get(p[2][1]) is None):
                print('Error: Variable no definida')
            else:
                print(p[1], run(p[2]))
                return run(p[1]) == run(p[2])

        elif p[0] == '<>':
            if (isinstance(p[1], int) is False and variables.get(p[1][1]) is None) or (isinstance(p[2], int) is False and variables.get(p[2][1]) is None):
                print('Error: Variable no definida')
            else:
                print(p[1], run(p[2]))
                return run(p[1]) != run(p[2])

        elif p[0] == '<=':
            if (isinstance(p[1], int) is False and variables.get(p[1][1]) is None) or (isinstance(p[2], int) is False and variables.get(p[2][1]) is None):
                print('Error: Variable no definida')
            else:
                print(p[1], run(p[2]))
                return run(p[1]) <= run(p[2])

        elif p[0] == '>=':
            if (isinstance(p[1], int) is False and variables.get(p[1][1]) is None) or (isinstance(p[2], int) is False and variables.get(p[2][1]) is None):
                print('Error: Variable no definida')
            else:
                print(p[1], run(p[2]))
                return run(p[1]) >= run(p[2])

        elif p[0] == '>':
            if (isinstance(p[1], int) is False and variables.get(p[1][1]) is None) or (isinstance(p[2], int) is False and variables.get(p[2][1]) is None):
                print('Error: Variable no definida')
            else:
                print(p[1], run(p[2]))
                return run(p[1]) > run(p[2])

        elif p[0] == '<':
            if (isinstance(p[1], int) is False and variables.get(p[1][1]) is None) or (isinstance(p[2], int) is False and variables.get(p[2][1]) is None):
                print('Error: Variable no definida')
            else:
                print(p[1], run(p[2]))
                return run(p[1]) < run(p[2])

        elif p[0] == '=':
            if len(variables) > 0 and variables.get(p[1]) is not None and isinstance(variables[p[1]], int) is True and isinstance(run(p[2]), bool) is True:
                print('Tipo incompatible')

            elif len(variables) > 0 and variables.get(p[1]) is not None and isinstance(variables[p[1]], bool) is True and isinstance(run(p[2]), int) is True:
                print('Tipo incompatible')

            else:
                variables[p[1]] = run(p[2])
                print("Variables:")
                print(variables, '\n')

        elif p[0] == 'var':
            return variables[p[1]]

        elif p[0] == 'statement':
            result1 = run(p[1])
            if p[1] is None:
                result2 = run(p[2])
                if isinstance(result2,tuple):
                    return result2
            elif isinstance(result1,tuple):
                print("SCUBIDIBAPMBADOP  1:", p)
                return result1
            else:
                result2 = run(p[2])
                if isinstance(result2, tuple):
                    return result2

        elif p[0] == 'for_loop':
            if len(variables) > 0 and variables.get(p[1]) is not None and isinstance(variables[p[1]], bool) is True:
                print('No puede usar variables booleans en bucles for')

            elif p[2] >= p[3]:
                print('Ingrese un rango valido')

            elif len(variables) > 0 and variables.get(p[1]) is not None and (variables[p[1]] > p[3] or variables[p[1]] < p[2]):
                print('La condicion se sale del rango del For')

            elif len(variables) == 0 and (p[1] < p[2] or p[1] > p[3]):
                print('La condicion se sale del rango del For')
            else:
                if p[5] == '..' and isinstance(p[1], str) is True and variables.get(p[1]) is None:
                    print('Variable no definida')
                elif p[5] == '..' and isinstance(p[1], str) is True and variables.get(p[1]) is not None:
                    for variables[run(p[1])] in range(p[2], p[3]-1):
                        result = run(p[4])
                        print(p[4], result)
                        if isinstance(result, tuple):
                            print("mean_for")
                            return result
                elif p[5] == '..' and isinstance(p[1], int) is True:
                    pointer = int(p[1])
                    for pointer in range(p[2], p[3]-1):
                        result = run(p[4])
                        print(p[4], result)
                        if isinstance(result, tuple):
                            print("mean_for")
                            return result

                elif p[5] == '..=' and isinstance(p[1], str) is True and variables.get(p[1]) is None:
                    print('Variable no definida')
                elif p[5] == '..=' and isinstance(p[1], str) is True and variables.get(p[1]) is not None:
                    for variables[p[1]] in range(p[2], p[3]):
                        result = run(p[4])
                        print(p[4], result)
                        if isinstance(result, tuple):
                            print("mean_for")
                            return result

                elif p[5] == '..=' and isinstance(p[1], int) is True:
                    pointer = int(p[1])
                    for pointer in range(p[2], p[3]):
                        result = run(p[4])
                        print(p[4], result)
                        if isinstance(result, tuple):
                            print("mean_for")
                            return result

                else:
                    return p

        elif p[0] == 'if_else':
            print("if pepesilvia")
            if run(p[1]):
                result = run(p[2])
                print(p[2], result)
                if isinstance(result, tuple):
                    print("if pepesilvia1")
                    return result
            else:
                result = run(p[3])
                if isinstance(result, tuple):
                    print("if pepesilvia2")
                    return result

        elif p[0] == 'while_loop':
            while run(p[1]):
                result = run(p[2])
                print(p[2], result)
                if isinstance(result, tuple):
                    print("meanwhile")
                    return result

        elif p[0] == 'return':
            return (True, run(p[1]))

        elif p[0] == 'function_def':
            if (p[1],length_variables(p[2])) in functions_methods:
                print("ERROR: Function", p[1], "already exist with the same name and number of inputs")
                return
            functions_methods[(p[1],length_variables(p[2]))] = (p[2], p[3], p[4])
            print("Functions/Methods:")
            print(functions_methods, '\n')
        elif p[0] == 'method_def':
            if (p[1],length_variables(p[2])) in functions_methods:
                print("ERROR: Method", p[1], "already exist with the same name and number of inputs")
                return
            functions_methods[(p[1], length_variables(p[2]))] = (p[2], p[3])
            print("Functions/Methods:")
            print(functions_methods, '\n')
        elif p[0] == 'fn':
            print((p[1],length_variables(p[2])))
            if (p[1],length_variables(p[2])) in functions_methods:
                ParameterNames = functions_methods[(p[1], length_variables(p[2]))][0]
                print(ParameterNames)
                print(p[2])
                add_parameter_variables(p[2], ParameterNames)
                print("New Variables:", variables)
                result = run(functions_methods[(p[1],length_variables(p[2]))][1])
                print("Resultbsjdakdas: ", functions_methods[(p[1],length_variables(p[2]))][1])
                print("Result: ", result)
                print("Func or Method?: ", len(functions_methods[(p[1], length_variables(p[2]))]))
                print("result is None:", (result is None))
                print("result is tuple:", isinstance(result,tuple))
                if (result is None) and (len(functions_methods[(p[1],length_variables(p[2]))]) == 2):
                    remove_parameter_variables(p[2], ParameterNames)
                    print("Variables Hoo Haa1:", variables)
                    return 0
                elif (result is None) and (len(functions_methods[(p[1],length_variables(p[2]))]) == 3):
                    #ERROR CASE, FUNCTION MUST HAVE A RETURN CODE SHOULD STOP READING
                    print("ERROR: Function ", p[1], "must have a return" )
                elif (isinstance(result,tuple)) and (len(functions_methods[(p[1],length_variables(p[2]))]) == 2):
                    print("WARNING: Method ", p[1], "must not have a return, returning 0 ")
                    remove_parameter_variables(p[2], ParameterNames)
                    return 0
                elif (isinstance(result,tuple)) and (len(functions_methods[(p[1],length_variables(p[2]))]) == 3):
                    if functions_methods[(p[1],length_variables(p[2]))][2] == "boolean":
                        print(result[1])
                        if isinstance(result[1],bool):
                            remove_parameter_variables(p[2], ParameterNames)
                            return result[1]
                        else:
                            #ERROR CASE, RETURN INCORRECT TYPE
                            print("ERROR: Incorrect return type, must be boolean")
                            remove_parameter_variables(p[2], ParameterNames)
                            return 0
                    elif functions_methods[(p[1],length_variables(p[2]))][2] == "integer":
                        print(result[1])
                        if isinstance(result[1],bool):
                            # ERROR CASE, RETURN INCORRECT TYPE
                            print("ERROR: Incorrect return type, must be integer")
                            remove_parameter_variables(p[2], ParameterNames)
                            return 0
                        else:
                            remove_parameter_variables(p[2], ParameterNames)
                            return result[1]
                else:
                    print("THIS SHOULD NOT HAPPEN")

            else:
                return

        elif p[0] == 'Move':
            if isinstance(p[1], tuple) is True:
                untuple(p[1])
                print(tuple_elements)
                j = len(tuple_elements)
                for i in range(j):
                    if run(p[2]):
                        print('mano arriba')
                        print(tuple_elements[i])
                    else:
                        print('Mano abajo')
                        print(tuple_elements[i])
            elif isinstance(p[1], tuple) is False:
                if run(p[2]):
                    print('mano arriba')
                    print(p[1])
                else:
                    print('Mano abajo')
                    print(p[1])

        elif p[0] == 'finger':
            print(p[1])

        elif p[0] == 'print':
            if isinstance(p[1], tuple) is True:
                printable = ""
                untupleS(p[1])
                print(phrase)
                j = len(phrase)
                for i in range(j):
                    if variables.get(phrase[i]) is not None:
                        printable = printable + " " + str(variables[phrase[1]])
                    elif variables.get(phrase[i]) is None:
                        printable = printable + " " + str(phrase[i])
                print(printable)
            elif isinstance(p[1], tuple) is False:
                print(p[1])
    else:
        return p


def untuple(p):
    j = len(p)
    for i in range(j):
        if p[i] is None:
            pass
        elif isinstance(p[i], tuple) is False:
            tuple_elements.append(p[i])
        elif isinstance(p[i], tuple) is True:
            untuple(p[i])


def untupleS(p):
    j = len(p)
    for i in range(j):
        if p[i] is None:
            pass
        elif isinstance(p[i], tuple) is False:
            phrase.append(p[i])
        elif isinstance(p[i], tuple) is True:
            untupleS(p[i])


def run_main():
    if ('main',0) in functions_methods:
        print('main found')
        run(functions_methods[('main',0)][1])
    else:
        print('ERROR: main not found')

def clearAll():
    global variables, functions_methods
    variables = {}
    functions_methods = {}
    lexer.lineno = 1
    print("\n")

def compile(text):
    parser.parse(text)
    print(variables)
    print(functions_methods)
    run_main()

    clearAll()
