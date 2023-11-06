import ply.yacc as yacc
from lexer import tokens

num_errors = 0
num_lines = 0

precedence = (
    ('nonassoc', 'AND', 'OR'),
    ('nonassoc', 'EQ', 'NEQ'),
    ('nonassoc', 'LTE', 'GTE', 'LT', 'GT'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'NOT')
)


def p_chunk(p):
    '''chunk : statlist
    | statlist laststat SEMICOLON
    '''
    if (len(p) == 2):
        p[0] = p[1]
    elif (len(p) == 4):
        p[0] = p[1] + [p[2]]


def p_statlist(p):
    '''
    statlist : stat SEMICOLON statlist
    | stat statlist
    | empty
    '''
    if len(p) == 4:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = []


def p_block(p):
    '''block : chunk'''
    p[0] = p[1]


def p_stat(p):
    '''
    stat : varlist ASSIGN explist
    | functioncall
    | DO block END
    | WHILE exp DO block END
    | REPEAT block UNTIL exp
    | IF exp THEN block elseiflist END
    | IF exp THEN block elseiflist ELSE block END
    | FOR NAME ASSIGN exp COMMA exp COMMA exp DO block END
    | FOR NAME ASSIGN exp COMMA exp DO block END
    | FOR namelist IN explist DO block END
    | FUNCTION funcname funcbody
    | LOCAL FUNCTION NAME funcbody
    | LOCAL namelist
    | LOCAL namelist ASSIGN explist
    '''
    if (len(p) == 2):
        p[0] = ("function-call", p[1])
    elif (len(p) == 3):
        p[0] = ("local-list", p[2])
    elif (len(p) == 4):
        if p[2] == "=":
            p[0] = ("assign", p[1], p[3])
        elif p[1] == "do":
            p[0] = ("do", p[2])
        elif p[1] == "function":
            p[0] = ("function", p[2], p[3])
    elif (len(p) == 5):
        if p[1] == "repeat":
            p[0] = ("repeat", p[2], p[4])
        elif (p[2] == "function"):
            p[0] = ("local-function", p[2], p[4])
        elif (p[3] == "assign"):
            p[0] = ("local-assign", p[2], p[4])
    elif (len(p) == 6):
        if p[1] == "while":
            p[0] = ("while", p[2], p[4])
    elif (len(p) == 7):
        if p[1] == "if":
            p[0] = ("if", p[2], p[4], p[5])
    elif (len(p) == 8):
        if (p[1] == "for"):
            p[0] = ("for-list", p[2], p[4], p[6])
    elif (len(p) == 9):
        if (p[1] == "if"):
            p[0] = ("if - else", p[2], p[4], p[5], p[7])
    elif (len(p) == 10):
        if (p[1] == "for"):
            p[0] = ("for2", p[2], p[4], p[6], p[8])
    elif len(p) == 12:
        if (p[1] == "for"):
            p[0] = ("for2", p[2], p[4], p[6], p[8], p[10])


def p_elseiflist(p):
    '''
    elseiflist : ELSEIF exp THEN block elseiflist
    | empty
    '''
    if len(p) == 6:
        p[0] = [("elseif", p[2], p[4])] + p[5]
    else:
        p[0] = []


def p_laststat(p):
    '''
    laststat : RETURN explist
    | RETURN
    | BREAK
    '''
    if len(p) == 3:
        p[0] = ("return", p[2])
    elif len(p) == 2:
        p[0] = ("return", [])
    else:
        p[0] = ("break", [])


def p_funcname(p):
    '''
    funcname : NAME dotnames
    | NAME dotnames COLON NAME
    '''
    if len(p) == 3:
        p[0] = ("funcname", p[1] + p[2])
    elif len(p) == 5:
        p[0] = ("funcname", p[1] + p[2], p[4])


def p_dotnames(p):
    '''
    dotnames : DOT NAME dotnames
    | empty
    '''
    if len(p) == 4:
        p[0] = [p[2]] + p[3]
    elif len(p) == 2:
        p[0] = []


def p_varlist(p):
    '''
    varlist : var COMMA varlist
    | var
    '''
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]


def p_var(p):
    '''
    var : NAME
    | prefixexp LBRACKET exp RBRACKET
    | prefixexp DOT NAME
    '''
    if len(p) == 2:
        p[0] = ("var", p[1])
    elif len(p) == 5:
        p[0] = ("var", p[1], p[3])
    elif len(p) == 4:
        p[0] = ("var", p[1], p[3])


def p_namelist(p):
    '''
    namelist : NAME COMMA namelist
    | NAME
    '''
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]


def p_explist(p):
    '''
    explist : exp COMMA explist
    | exp
    '''
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]


def p_exp(p):
    '''
    exp : NIL
    | TRUE
    | FALSE
    | NUMBER
    | STRING
    | ELLIPSIS
    | function
    | prefixexp
    | tableconstructor
    | exp binop exp
    | unop exp
    '''
    if len(p) == 2:
        p[0] = ("exp", p[1])
    elif len(p) == 4:
        p[0] = ("binop", p[2], p[1], p[3])
    elif len(p) == 3:
        p[0] = ("unop", p[1], p[2])


def p_prefixexp(p):
    '''
    prefixexp : var
    | functioncall
    | LPAREN exp RPAREN
    '''
    if len(p) == 2:
        p[0] = ("prefixexp", p[1])
    elif len(p) == 4:
        p[0] = p[2]


def p_functioncall(p):
    '''
    functioncall : prefixexp args
    | prefixexp COLON NAME args
    '''
    if len(p) == 3:
        p[0] = ("functioncall", p[1], p[2])
    elif len(p) == 5:
        p[0] = ("functioncall", p[1], p[3], p[4])


def p_args(p):
    '''
    args : LPAREN explist RPAREN
    | LPAREN RPAREN
    | tableconstructor
    | STRING
    '''
    if len(p) == 4:
        p[0] = ("args", p[2])
    elif len(p) == 3:
        p[0] = ("args", [])
    elif len(p) == 2:
        p[0] = ("args", p[1])


def p_function(p):
    '''
    function : FUNCTION funcbody
    '''
    p[0] = ("function", p[2])


def p_funcbody(p):
    '''
    funcbody : LPAREN parlist RPAREN block END
    | LPAREN RPAREN block END
    '''
    if len(p) == 6:
        p[0] = ("funcbody", p[2], p[4])
    elif len(p) == 5:
        p[0] = ("funcbody", [], p[3])


def p_parlist(p):
    '''
    parlist : namelist COMMA ELLIPSIS
    | namelist
    | ELLIPSIS
    '''
    if len(p) == 4:
        p[0] = ("parlist", p[1], True)
    elif len(p) == 2:
        if (p[1] == "..."):
            p[0] = ("parlist", [], True)
        else:
            p[0] = ("parlist", p[1], False)


def p_tableconstructor(p):
    '''
    tableconstructor : LBRACE fieldlist RBRACE
    | LBRACE RBRACE
    '''
    if len(p) == 4:
        p[0] = ("tableconstructor", p[2])
    elif len(p) == 3:
        p[0] = ("tableconstructor", [])


def p_fieldlist(p):
    '''
    fieldlist : field fieldlist2 fieldsep
    | field fieldlist2
    '''
    if len(p) == 4:
        p[0] = [p[1]] + p[2]
    elif len(p) == 3:
        p[0] = [p[1]] + p[2]


def p_fieldlist2(p):
    '''
    fieldlist2 : field fieldsep fieldlist2
    | empty
    '''
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    elif len(p) == 2:
        p[0] = []


def p_field(p):
    '''
    field : LBRACKET exp RBRACKET ASSIGN exp
    | NAME ASSIGN exp
    | exp
    '''
    if len(p) == 6:
        p[0] = ("field", p[2], p[5])
    elif len(p) == 4:
        p[0] = ("field", p[1], p[3])
    elif len(p) == 2:
        p[0] = ("field", p[1])


def p_fieldsep(p):
    '''
    fieldsep : COMMA
    | SEMICOLON
    '''
    p[0] = p[1]


def p_binop(p):
    '''
    binop : PLUS
    | MINUS
    | TIMES
    | DIVIDE
    | MODULO
    | EXPONENT
    | CONCAT
    | EQ
    | NEQ
    | LT
    | GT
    | LTE
    | GTE
    | AND
    | OR
    '''
    p[0] = p[1]


def p_unop(p):
    '''
    unop : MINUS
    | NOT
    | LEN
    '''


def p_empty(p):
    'empty :'
    pass


def p_error(p):
    print("The input is syntactically incorrect")
    exit(1)


parser = yacc.yacc()
