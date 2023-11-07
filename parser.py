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
    | statlist laststat
    | statlist laststat SEMICOLON
    '''


def p_statlist(p):
    '''
    statlist : stat SEMICOLON statlist
    | stat statlist
    | empty
    '''


def p_block(p):
    '''block : chunk'''


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


def p_elseiflist(p):
    '''
    elseiflist : ELSEIF exp THEN block elseiflist
    | empty
    '''


def p_laststat(p):
    '''
    laststat : RETURN explist
    | RETURN
    | BREAK
    '''


def p_funcname(p):
    '''
    funcname : NAME dotnames
    | NAME dotnames COLON NAME
    '''


def p_dotnames(p):
    '''
    dotnames : DOT NAME dotnames
    | empty
    '''


def p_varlist(p):
    '''
    varlist : var COMMA varlist
    | var
    '''


def p_var(p):
    '''
    var : NAME
    | prefixexp LBRACKET exp RBRACKET
    | prefixexp DOT NAME
    '''


def p_namelist(p):
    '''
    namelist : NAME COMMA namelist
    | NAME
    '''


def p_explist(p):
    '''
    explist : exp COMMA explist
    | exp
    '''


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


def p_prefixexp(p):
    '''
    prefixexp : var
    | functioncall
    | LPAREN exp RPAREN
    '''


def p_functioncall(p):
    '''
    functioncall : prefixexp args
    | prefixexp COLON NAME args
    '''


def p_args(p):
    '''
    args : LPAREN explist RPAREN
    | LPAREN RPAREN
    | tableconstructor
    | STRING
    '''


def p_function(p):
    '''
    function : FUNCTION funcbody
    '''


def p_funcbody(p):
    '''
    funcbody : LPAREN parlist RPAREN block END
    | LPAREN RPAREN block END
    '''


def p_parlist(p):
    '''
    parlist : namelist COMMA ELLIPSIS
    | namelist
    | ELLIPSIS
    '''


def p_tableconstructor(p):
    '''
    tableconstructor : LBRACE fieldlist RBRACE
    | LBRACE RBRACE
    '''


def p_fieldlist(p):
    '''
    fieldlist : field fieldlist2 fieldsep
    | field fieldlist2
    '''


def p_fieldlist2(p):
    '''
    fieldlist2 : field fieldsep fieldlist2
    | empty
    '''


def p_field(p):
    '''
    field : LBRACKET exp RBRACKET ASSIGN exp
    | NAME ASSIGN exp
    | exp
    '''


def p_fieldsep(p):
    '''
    fieldsep : COMMA
    | SEMICOLON
    '''


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


parser = yacc.yacc(debug=True)
