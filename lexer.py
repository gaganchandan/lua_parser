import ply.lex as lex

reserved = {
    'and': 'AND',
    'break': 'BREAK',
    'do': 'DO',
    'else': 'ELSE',
    'elseif': 'ELSEIF',
    'end': 'END',
    'false': 'FALSE',
    'for': 'FOR',
    'function': 'FUNCTION',
    'if': 'IF',
    'in': 'IN',
    'local': 'LOCAL',
    'nil': 'NIL',
    'not': 'NOT',
    'or': 'OR',
    'repeat': 'REPEAT',
    'return': 'RETURN',
    'then': 'THEN',
    'true': 'TRUE',
    'until': 'UNTIL',
    'while': 'WHILE'
}

tokens = ['NAME', 'NUMBER', 'STRING', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
          'MODULO', 'LEN', 'EXPONENT', 'EQ', 'NEQ', 'LTE', 'GTE', 'LT',
          'GT', 'ASSIGN', 'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE',
          'LBRACKET', 'RBRACKET', 'SEMICOLON', 'COLON', 'COMMA', 'DOT',
          'CONCAT', 'ELLIPSIS']
tokens += list(reserved.values())

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MODULO = r'%'
t_LEN = r'\#'
t_EXPONENT = r'\^'
t_EQ = r'=='
t_NEQ = r'~='
t_LTE = r'<='
t_GTE = r'>='
t_LT = r'<'
t_GT = r'>'
t_ASSIGN = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_SEMICOLON = r';'
t_COLON = r':'
t_COMMA = r','
t_DOT = r'\.'
t_CONCAT = r'\.\.'
t_ELLIPSIS = r'\.\.\.'


def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'NAME')
    return t


def t_NUMBER(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value)
    return t


def t_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"'
    t.value = t.value[1:-1]
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


t_ignore = ' \t'


t_ignore_COMMENT = r'--.*'


def t_error(t):
    global num_errors
    print("Ilegal character '%s' at line: %d" % (t.value[0], t.lexer.lineno))
    num_errors += 1
    t.lexer.skip(1)


lexer = lex.lex()
